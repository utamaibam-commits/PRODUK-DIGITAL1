"""Musik latar & sound effect KasRapi gaya motion graphic TikTok (energik, Gen Z).
100% disintesis sendiri dengan numpy, bebas hak cipta, aman dari klaim Content ID.

Jalankan:  python3 scripts/buat-audio.py
Hasil:     public/audio/music.wav, public/audio/sfx/*.wav
Butuh:     Python 3 + numpy
"""
import os
import wave

import numpy as np

SR = 44100
ROOT = os.path.join(os.path.dirname(__file__), '..', 'public', 'audio')
rng = np.random.default_rng(11)


# ------------------------------------------------------------------ util
def save(name, x, width=0.0, peak=0.89):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        if width:
            d = int(SR * 0.011)
            r = np.concatenate([np.zeros(d), x[:-d]])
            x = np.stack([x, x * (1 - width) + r * width], 1)
        else:
            x = np.stack([x, x], 1)
    x = np.tanh(x / (np.max(np.abs(x)) or 1) * 1.2) / np.tanh(1.2)  # soft clip = lebih "padat"
    x = x / np.max(np.abs(x)) * peak
    path = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    print('ok', name, f'{len(x) / SR:.2f}s')


def t_(d):
    return np.arange(int(SR * d)) / SR


def noise(d):
    return rng.standard_normal(int(SR * d))


def fft_filter(x, lo=None, hi=None):
    """Filter pita statis via FFT (cepat, tanpa scipy)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def svf_sweep(x, fc, q=0.7):
    """State-variable band-pass dengan cutoff berubah per sampel (untuk whoosh)."""
    lp = bp = 0.0
    y = np.zeros_like(x)
    damp = 1 / q
    for i, v in enumerate(x):
        f = 2 * np.sin(np.pi * min(fc[i], SR / 6) / SR)
        hp = v - lp - damp * bp
        bp += f * hp
        lp += f * bp
        y[i] = bp
    return y


def sine_sweep(f):
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def reverb(x, mix=0.25, d=0.9):
    """Reverb ringan: noise meluruh dikonvolusi via FFT."""
    ir_t = t_(d)
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 6)
    ir = fft_filter(ir, hi=6000)
    n = len(x) + len(ir)
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[: len(x) + len(ir) - 1]
    wet = wet / (np.max(np.abs(wet)) or 1) * np.max(np.abs(x))
    out = np.zeros(len(wet))
    out[: len(x)] += x
    return out + wet * mix


def fit(x, n):
    return np.pad(x, (0, max(0, n - len(x))))[:n]


# ------------------------------------------------------------------ SFX
def whoosh(d=0.6, up=True):
    t = t_(d)
    p = t / d
    fc = 300 * (14 ** p) if up else 4200 * (14 ** -p)
    y = svf_sweep(noise(d), fc, q=1.4)
    env = (p ** 1.6) * np.exp(-((p - 0.85) * 6) ** 2 * (p > 0.85)) if up else np.exp(-p * 5) * np.minimum(p * 30, 1)
    return y * env


def swoosh_short():
    return whoosh(0.28, up=False)


def boom():
    """Sub drop + klik transien (hentakan saat teks muncul)."""
    t = t_(1.0)
    f = 42 + 140 * np.exp(-t * 22)
    sub = sine_sweep(f) * np.exp(-t * 3.2)
    click = fft_filter(noise(1.0), lo=2500) * np.exp(-t * 220) * 0.6
    body = fft_filter(noise(1.0), hi=900) * np.exp(-t * 18) * 0.35
    return reverb(sub + click + body, 0.12, 0.6)


def thump():
    t = t_(0.35)
    f = 55 + 95 * np.exp(-t * 35)
    return sine_sweep(f) * np.exp(-t * 11) + fft_filter(noise(0.35), lo=3000) * np.exp(-t * 300) * 0.4


def pop():
    t = t_(0.12)
    f = 520 + 1400 * np.exp(-t * 55)
    return sine_sweep(f) * np.exp(-t * 38) * np.minimum(t * 2000, 1)


def tick():
    t = t_(0.05)
    x = np.sin(2 * np.pi * 3200 * t) * 0.5 + fft_filter(noise(0.05), lo=4000) * 0.6
    return x * np.exp(-t * 160)


def glitch():
    """Stutter digital: potongan buzz & noise acak (saat uang 'dipotong')."""
    d = 0.32
    out = np.zeros(int(SR * d))
    pos = 0
    while pos < len(out):
        L = int(SR * rng.uniform(0.012, 0.04))
        tt = np.arange(L) / SR
        kind = rng.integers(0, 3)
        if kind == 0:
            seg = np.sign(np.sin(2 * np.pi * rng.uniform(90, 400) * tt))
        elif kind == 1:
            seg = fft_filter(rng.standard_normal(L), lo=1500) * 1.4
        else:
            seg = np.sin(2 * np.pi * rng.uniform(800, 2400) * tt)
        seg *= rng.uniform(0.4, 1.0)
        out[pos: pos + L] = seg[: len(out) - pos]
        pos += L + int(SR * rng.uniform(0, 0.01))
    t = t_(d)
    return fft_filter(out, hi=7000) * np.exp(-t * 4) + fit(thump(), len(out)) * 0.5


def err():
    t = t_(0.3)
    x = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 147 * t)) * 0.5
    return fft_filter(x, hi=2200) * np.exp(-t * 8) * (np.minimum(t * 400, 1))


def cash():
    """Ka-ching: klik laci + dua lonceng terang."""
    t = t_(1.2)
    x = fft_filter(noise(1.2), lo=1800) * np.exp(-t * 90) * 0.7
    for start, base in ((0.05, 2093.0), (0.13, 2637.0)):
        tt = np.maximum(t - start, 0)
        on = t >= start
        for k, a in ((1, 1.0), (2.76, 0.45), (5.4, 0.25)):
            x += on * a * np.sin(2 * np.pi * base * k * tt) * np.exp(-tt * (5 + k))
    return reverb(x, 0.2, 0.7)


def ding():
    t = t_(1.0)
    x = np.zeros(len(t))
    for f, a in ((1568.0, 1.0), (2349.3, 0.5), (3136.0, 0.25)):
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * 5)
    return reverb(x * np.minimum(t * 3000, 1), 0.2, 0.6)


def check():
    """Notif sukses: dua nada naik, bulat."""
    t = t_(0.45)
    a = np.sin(2 * np.pi * 1046.5 * t) * np.exp(-t * 18)
    tb = np.maximum(t - 0.07, 0)
    b = (t >= 0.07) * np.sin(2 * np.pi * 1568 * tb) * np.exp(-tb * 10)
    return (a + b) * np.minimum(t * 3000, 1)


def riser(d=1.3):
    t = t_(d)
    p = t / d
    y = svf_sweep(noise(d), 400 * (20 ** p), q=2.5)
    tone = sine_sweep(220 * 2 ** (p * 3)) * 0.25
    return (y + tone) * p ** 2.2


SFX = {
    'whoosh': whoosh(), 'swipe': swoosh_short(), 'boom': boom(), 'thump': thump(),
    'pop': pop(), 'tick': tick(), 'glitch': glitch(), 'err': err(), 'cash': cash(),
    'ding': ding(), 'check': check(), 'riser': riser(),
}
for k, v in SFX.items():
    save(f'sfx/{k}.wav', v, width=0.25 if k in ('whoosh', 'swipe', 'riser') else 0.0)

# ------------------------------------------------------------------ MUSIK
# Beat energik 150 BPM (half-time feel), progresi minor Fm-Db-Ab-Eb ala konten kreator.
BPM = 150
B = 60 / BPM
DUR = 28.0
N = int(SR * DUR)


def put(buf, s, x, g=1.0):
    i = int(s * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i] * g


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def kick():
    t = t_(0.4)
    f = 48 + 170 * np.exp(-t * 30)
    return sine_sweep(f) * np.exp(-t * 7) + fft_filter(noise(0.4), lo=3000) * np.exp(-t * 400) * 0.5


def snare():
    t = t_(0.35)
    body = sine_sweep(200 + 60 * np.exp(-t * 40)) * np.exp(-t * 25)
    n = fft_filter(noise(0.35), lo=1200, hi=9000) * np.exp(-t * 14)
    return reverb(body * 0.6 + n, 0.2, 0.5)


def hat(open_=False):
    d = 0.2 if open_ else 0.05
    t = t_(d)
    return fft_filter(noise(d), lo=7000) * np.exp(-t * (14 if open_ else 90))


def sub808(m, d):
    t = t_(d)
    f = note(m) * (1 + 0.6 * np.exp(-t * 30))
    x = sine_sweep(f)
    x = np.tanh(x * 1.8)
    return x * np.minimum(t * 300, 1) * np.exp(-t * 1.2) * np.minimum((d - t) * 60, 1)


def pluck(m, d=0.28):
    t = t_(d)
    f = note(m)
    x = np.zeros(len(t))
    for det in (-0.08, 0.08):
        ph = 2 * np.pi * f * 2 ** (det / 12) * t
        x += 2 * ((ph / (2 * np.pi)) % 1) - 1  # saw
    return fft_filter(x, hi=3800) * np.exp(-t * 11)


def pad(ms, d):
    t = t_(d)
    x = np.zeros(len(t))
    for m in ms:
        for det in (-0.12, 0, 0.12):
            ph = 2 * np.pi * note(m) * 2 ** (det / 12) * t
            x += 2 * ((ph / (2 * np.pi)) % 1) - 1
    x = fft_filter(x, hi=1600)
    return x * np.minimum(t / 0.2, 1) * np.minimum((d - t) / 0.3, 1)


CH = [(41, [65, 68, 72]), (37, [65, 68, 73]), (44, [63, 68, 72]), (39, [63, 67, 70])]
BAR = B * 4
drums = np.zeros(N)
bass = np.zeros(N)
syn = np.zeros(N)
pads = np.zeros(N)
nb = int(DUR / BAR) + 1
for b in range(nb):
    t0 = b * BAR
    root, ch = CH[b % 4]
    intro = t0 < 1.5
    put(pads, t0, pad(ch, BAR + 0.2), 0.12)
    if not intro:
        put(bass, t0, sub808(root - 12, B * 2.5), 0.8)
        put(bass, t0 + B * 2.75, sub808(root - 12 + (3 if b % 2 else 0), B * 1.2), 0.7)
    seq = [ch[0], ch[2], ch[1] + 12, ch[2], ch[0] + 12, ch[2], ch[1], ch[2] + 12]
    for k, m in enumerate(seq):
        put(syn, t0 + k * B / 2, pluck(m), 0.22 if k % 2 == 0 else 0.15)
    # kick pola trap: 1, 2&, (4& variasi)
    for kk in ((0,), (1.5,), (3.5,) if b % 2 else ()):
        for s in kk:
            put(drums, t0 + s * B, kick(), 0.95 if not intro else 0.5)
    if not intro:
        put(drums, t0 + 2 * B, snare(), 0.55)
        for k in range(8):
            put(drums, t0 + k * B / 2, hat(), 0.18 if k % 2 else 0.25)
        if b % 2 == 1:  # roll hi-hat ala trap di akhir bar
            for k in range(6):
                put(drums, t0 + 3 * B + k * B / 6, hat(), 0.14 + 0.02 * k)
        put(drums, t0 + 3.5 * B, hat(True), 0.12)

pump = np.ones(N)
for k in range(int(DUR / B) + 1):
    i = int(k * B * SR)
    L = int(0.2 * SR)
    seg = 1 - 0.5 * np.exp(-np.arange(L) / (0.05 * SR))
    j = min(N, i + L)
    if i < N:
        pump[i:j] = np.minimum(pump[i:j], seg[: j - i])
music = drums + bass * 0.9 + (syn + pads) * pump
music = fft_filter(music, lo=30)
fade = np.ones(N)
fade[: int(0.03 * SR)] = np.linspace(0, 1, int(0.03 * SR))
fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
save('music.wav', music * fade, width=0.3)
