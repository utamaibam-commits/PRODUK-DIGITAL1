"""Membuat musik latar & sound effect KasRapi secara sintetis (100% buatan sendiri,
bebas hak cipta, aman dari klaim Content ID TikTok).

Jalankan:  python3 scripts/buat-audio.py
Hasil:     public/audio/music.wav, public/audio/sfx/*.wav
Butuh:     Python 3 + numpy
"""
import os
import wave

import numpy as np

SR = 44100
ROOT = os.path.join(os.path.dirname(__file__), '..', 'public', 'audio')
rng = np.random.default_rng(7)


def save(name, x, stereo_width=0.0):
    x = np.asarray(x, dtype=np.float64)
    peak = np.max(np.abs(x)) or 1.0
    x = x / peak * 0.89
    if stereo_width:
        d = int(SR * 0.012)
        r = np.concatenate([np.zeros(d), x[:-d]])
        l, r = x, x * (1 - stereo_width) + r * stereo_width
    else:
        l = r = x
    data = (np.stack([l, r], axis=1) * 32767).astype(np.int16)
    path = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print('ok', path, f'{len(x) / SR:.2f}s')


def t_(dur):
    return np.arange(int(SR * dur)) / SR


def env(n, a=0.005, d=0.2, s=0.0, r=0.05, sus=None):
    """ADSR sederhana, n sampel."""
    out = np.zeros(n)
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    S = max(n - A - D - R, 0) if sus is None else int(sus * SR)
    seg = [np.linspace(0, 1, max(A, 1)), np.linspace(1, s, max(D, 1)), np.full(S, s), np.linspace(s, 0, max(R, 1))]
    e = np.concatenate(seg)[:n]
    out[: len(e)] = e
    return out


def lowpass(x, k=0.15):
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc)
        y[i] = acc
    return y


def note(f):
    return 440.0 * 2 ** ((f - 69) / 12)


# ----------------------------------------------------------------- MUSIK
BPM = 112
BEAT = 60 / BPM
DUR = 28.0
N = int(SR * DUR)
mix = np.zeros(N)


def put(buf, start_s, x, gain=1.0):
    i = int(start_s * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i] * gain


def kick():
    t = t_(0.35)
    f = 50 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def hat(open_=False):
    t = t_(0.18 if open_ else 0.05)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 0.5)
    return n * np.exp(-t * (18 if open_ else 70))


def clap():
    t = t_(0.2)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 0.12)
    e = np.exp(-t * 22) + 0.6 * np.exp(-np.maximum(t - 0.012, 0) * 30) * (t > 0.012)
    return n * e


def pluck(m, dur=0.32):
    t = t_(dur)
    f = note(m)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t))
    return x * np.exp(-t * 9)


def pad(ms, dur):
    t = t_(dur)
    x = np.zeros(len(t))
    for m in ms:
        f = note(m)
        for det in (-0.12, 0.0, 0.12):
            ff = f * 2 ** (det / 12)
            x += np.sign(np.sin(2 * np.pi * ff * t)) * 0.15 + np.sin(2 * np.pi * ff * t)
    x = lowpass(x, 0.06)
    return x * env(len(t), a=0.25, d=0.2, s=0.8, r=0.4)


def bass(m, dur):
    t = t_(dur)
    f = note(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return x * env(len(t), a=0.005, d=0.15, s=0.6, r=0.05)


# Progresi Am - F - C - G (vibe positif, "naik")
CHORDS = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]
BAR = BEAT * 4
bars = int(DUR / BAR) + 1
pads = np.zeros(N)
drums = np.zeros(N)
lead = np.zeros(N)
bassb = np.zeros(N)
for b in range(bars):
    root, ch = CHORDS[b % 4]
    t0 = b * BAR
    put(pads, t0, pad(ch, BAR + 0.3), 0.18)
    for k in range(8):  # bass 8th note
        put(bassb, t0 + k * BEAT / 2, bass(root - 12 if k % 2 == 0 else root, BEAT / 2 * 0.9), 0.5)
    arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]
    for k, m in enumerate(arp):
        put(lead, t0 + k * BEAT / 2, pluck(m), 0.22)
    intro = t0 < 3.0  # 3 detik pertama lebih tipis agar hook terdengar
    for k in range(4):
        put(drums, t0 + k * BEAT, kick(), 0.9 if not intro else 0.6)
        if not intro:
            put(drums, t0 + k * BEAT + BEAT / 2, hat(k % 2 == 1), 0.25)
            put(drums, t0 + k * BEAT + BEAT / 4, hat(), 0.12)
            put(drums, t0 + k * BEAT + 3 * BEAT / 4, hat(), 0.12)
        if k in (1, 3) and not intro:
            put(drums, t0 + k * BEAT, clap(), 0.35)

# sidechain "pumping" dari kick
pump = np.ones(N)
for b in range(int(DUR / BEAT) + 1):
    i = int(b * BEAT * SR)
    L = int(0.22 * SR)
    seg = 1 - 0.55 * np.exp(-np.arange(L) / (0.06 * SR))
    j = min(N, i + L)
    if i < N:
        pump[i:j] = np.minimum(pump[i:j], seg[: j - i])
music = drums + (pads + lead + bassb) * pump
fade = np.ones(N)
fade[: int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
save('music.wav', music * fade, stereo_width=0.35)

# ----------------------------------------------------------------- SFX


def whoosh(dur=0.55, up=True):
    t = t_(dur)
    n = rng.standard_normal(len(t))
    k = np.linspace(0.02, 0.35, len(t)) if up else np.linspace(0.35, 0.02, len(t))
    y = np.zeros_like(n)
    acc = 0.0
    for i, v in enumerate(n):
        acc += k[i] * (v - acc)
        y[i] = acc
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return y * e


def pop():
    t = t_(0.14)
    f = 300 + 900 * np.exp(-t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)


def tap():
    t = t_(0.06)
    return (np.sin(2 * np.pi * 1800 * t) * 0.6 + rng.standard_normal(len(t)) * 0.4) * np.exp(-t * 90)


def ding():
    t = t_(1.1)
    x = np.zeros(len(t))
    for f, a in ((1318.5, 1.0), (1975.5, 0.6), (2637, 0.35)):
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * 4)
    x += 0.8 * np.sin(2 * np.pi * 987.8 * t) * np.exp(-t * 6) * (t < 0.12)
    return x


def coin_drop():
    """Bunyi 'minus' turun (uang terpotong)."""
    t = t_(0.28)
    f = 700 * np.exp(-t * 5)
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    return lowpass(sq, 0.25) * np.exp(-t * 9)


def impact():
    t = t_(0.9)
    f = 40 + 80 * np.exp(-t * 12)
    b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)
    n = rng.standard_normal(len(t))
    return b + lowpass(n, 0.08) * np.exp(-t * 10) * 0.8


def riser(dur=1.2):
    t = t_(dur)
    f = 200 * 2 ** (t / dur * 3)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3
    n = rng.standard_normal(len(t)) * 0.5
    return (tone + n - lowpass(n, 0.3)) * (t / dur) ** 2


def check():
    t = t_(0.35)
    a = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 14) * (t < 0.12)
    b = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-np.maximum(t - 0.08, 0) * 12) * (t >= 0.08)
    return a + b


def swipe():
    return whoosh(0.3, up=False)


save('sfx/whoosh.wav', whoosh())
save('sfx/swipe.wav', swipe())
save('sfx/pop.wav', pop())
save('sfx/tap.wav', tap())
save('sfx/ding.wav', ding())
save('sfx/minus.wav', coin_drop())
save('sfx/impact.wav', impact())
save('sfx/riser.wav', riser())
save('sfx/check.wav', check())
