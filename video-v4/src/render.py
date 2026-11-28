import sys, math, os, subprocess
sys.path.insert(0, '/tmp/claude-0/kr/build')
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import tl

W, H, FPS = 1080, 1920, 30
R = '/tmp/claude-0/kr/'
FD = '/usr/share/fonts/opentype/inter/'
def F(sz, w='Black'): return ImageFont.truetype(FD + f'Inter-{w}.otf', sz)

INK = (17, 17, 17)
WHITE = (255, 255, 255)
COL = {1: (255, 214, 10), 2: (255, 93, 162), 3: (61, 123, 255), 4: (182, 242, 60),
       5: (255, 138, 43), 6: (169, 139, 255), 7: (255, 214, 10)}
TEAL = (15, 118, 110)
GREEN = (22, 163, 74)
RED = (235, 51, 51)

# ---------- easing ----------
def spring(t):
    if t <= 0: return 0.0
    return 1 - math.exp(-7 * t) * math.cos(12 * t)
def eout(t):
    t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def clamp(x, a=0, b=1): return max(a, min(b, x))

# ---------- sprites ----------
def round_mask(w, h, r):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m

def sticker(path, width, crop=None, border=7, r=26, pad=0):
    im = Image.open(R + path).convert('RGB')
    if crop: im = im.crop(crop)
    h = int(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    Wb, Hb = width + 2 * border, h + 2 * border
    out = Image.new('RGBA', (Wb, Hb), INK + (0,))
    ImageDraw.Draw(out).rounded_rectangle([0, 0, Wb - 1, Hb - 1], r + border, fill=INK + (255,))
    inner = im.convert('RGBA'); inner.putalpha(round_mask(width, h, r))
    out.alpha_composite(inner, (border, border))
    out.info['scale'] = width / Image.open(R + path).width if not crop else width / (crop[2] - crop[0])
    out.info['b'] = border
    return out

def phone(path, height):
    im = Image.open(R + path).convert('RGB')
    w = int(im.width * height / im.height)
    im = im.resize((w, height), Image.LANCZOS)
    b = 16
    out = Image.new('RGBA', (w + 2 * b, height + 2 * b), INK + (0,))
    ImageDraw.Draw(out).rounded_rectangle([0, 0, w + 2 * b - 1, height + 2 * b - 1], 64, fill=INK + (255,))
    inner = im.convert('RGBA'); inner.putalpha(round_mask(w, height, 50))
    out.alpha_composite(inner, (b, b))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([out.width // 2 - 70, b + 8, out.width // 2 + 70, b + 36], 14, fill=INK + (255,))
    out.info['s'] = height / Image.open(R + path).height; out.info['b'] = b
    return out

def box(text, size, fg=INK, bg=WHITE, pad=(30, 16), border=7, weight='Black', r=18):
    f = F(size, weight)
    bb = f.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w, h = tw + 2 * pad[0] + 2 * border, th + 2 * pad[1] + 2 * border
    out = Image.new('RGBA', (w, h), INK + (0,))
    d = ImageDraw.Draw(out)
    if bg is not None:
        d.rounded_rectangle([0, 0, w - 1, h - 1], r + border, fill=INK + (255,))
        d.rounded_rectangle([border, border, w - 1 - border, h - 1 - border], r, fill=bg + (255,))
    d.text((border + pad[0] - bb[0], border + pad[1] - bb[1]), text, font=f, fill=fg + (255,))
    return out

def outline_text(text, size, fg=WHITE, stroke=10):
    f = F(size)
    bb = f.getbbox(text, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
    out = Image.new('RGBA', (w, h), fg + (0,))
    ImageDraw.Draw(out).text((-bb[0] + 2, -bb[1] + 2), text, font=f, fill=fg + (255,), stroke_width=stroke, stroke_fill=INK + (255,))
    return out

def check_icon(sz, col=GREEN):
    out = Image.new('RGBA', (sz, sz), INK + (0,))
    d = ImageDraw.Draw(out)
    d.ellipse([0, 0, sz - 1, sz - 1], fill=INK + (255,)); d.ellipse([7, 7, sz - 8, sz - 8], fill=col + (255,))
    d.line([(sz * .28, sz * .52), (sz * .44, sz * .68), (sz * .74, sz * .34)], fill=WHITE + (255,), width=int(sz * .12), joint='curve')
    return out

def cross_icon(sz, col=RED):
    out = Image.new('RGBA', (sz, sz), INK + (0,))
    d = ImageDraw.Draw(out)
    d.ellipse([0, 0, sz - 1, sz - 1], fill=INK + (255,)); d.ellipse([7, 7, sz - 8, sz - 8], fill=col + (255,))
    a, b = sz * .32, sz * .68
    d.line([(a, a), (b, b)], fill=WHITE + (255,), width=int(sz * .12)); d.line([(a, b), (b, a)], fill=WHITE + (255,), width=int(sz * .12))
    return out

def arrow_down(sz):
    out = Image.new('RGBA', (sz, int(sz * 1.1)), INK + (0,))
    d = ImageDraw.Draw(out)
    pts = [(sz * .3, 0), (sz * .7, 0), (sz * .7, sz * .5), (sz * .95, sz * .5), (sz * .5, sz * 1.05), (sz * .05, sz * .5), (sz * .3, sz * .5)]
    d.polygon(pts, fill=INK + (255,))
    inner = [(sz * .38, sz * .08), (sz * .62, sz * .08), (sz * .62, sz * .58), (sz * .8, sz * .58), (sz * .5, sz * .92), (sz * .2, sz * .58), (sz * .38, sz * .58)]
    d.polygon(inner, fill=WHITE + (255,))
    return out

# ---------- compositor ----------
SH = (14, 14)
def put(canvas, spr, cx, cy, scale=1.0, rot=0.0, alpha=1.0, shadow=True):
    if alpha <= 0.01 or scale <= 0.01: return
    s = spr
    if abs(scale - 1) > 0.003:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        s = s.rotate(rot, Image.BICUBIC, expand=True)
    a = s.getchannel('A')
    if alpha < 1: a = a.point(lambda v: int(v * alpha))
    x, y = int(cx - s.width / 2), int(cy - s.height / 2)
    if shadow:
        canvas.paste(INK, (x + int(SH[0] * scale), y + int(SH[1] * scale)), a)
    canvas.paste(s.convert('RGB'), (x, y), a)

def pop(t, t0, kind='pop'):
    """returns scale, alpha"""
    u = t - t0
    if u < 0: return 0, 0
    if kind == 'slam':
        return 1.9 - 0.9 * spring(u * 1.2), clamp(u / 0.08)
    return 0.2 + 0.8 * spring(u), clamp(u / 0.08)

def slide(t, t0, dist, dur=0.45):
    return dist * (1 - eout((t - t0) / dur)) if t >= t0 else dist

# ---------- precomputed sprites ----------
SP = {}
def S(): pass

def build():
    SP['wm'] = box('@klisacom', 30, fg=INK, bg=WHITE, pad=(18, 10), border=5, weight='ExtraBold', r=12)
    SP['badge'] = box('KasRapi · isi aplikasi asli', 30, fg=WHITE, bg=INK, pad=(18, 10), border=5, weight='ExtraBold', r=12)
    for k in range(1, 6):
        SP[f'chip{k}'] = box(f'FITUR #{k}', 40, fg=WHITE, bg=INK, pad=(22, 12), border=6, weight='Black', r=14)
    # s1
    SP['c_shopee'] = box('Shopee', 88, fg=WHITE, bg=(238, 77, 45))
    SP['c_tiktok'] = box('TikTok Shop', 88, fg=WHITE, bg=INK)
    SP['c_wa'] = box('WhatsApp', 88, fg=WHITE, bg=(37, 190, 90))
    SP['h1a'] = outline_text('UNTUNG', 150, WHITE, 12)
    SP['h1b'] = outline_text('BERSIHNYA', 130, WHITE, 12)
    SP['q'] = outline_text('?', 330, (255, 93, 162), 14)
    SP['gaktau'] = box('GAK TAU, ANJIR!', 100, fg=WHITE, bg=RED, r=10)
    SP['x'] = cross_icon(170)
    SP['tenang'] = box('tenang, ada…', 56, fg=INK, bg=WHITE, weight='ExtraBold')
    SP['logo'] = box('KasRapi', 170, fg=WHITE, bg=TEAL, pad=(46, 26), border=9, r=30)
    SP['ph_beranda'] = phone('v_beranda.png', 860)
    # s2
    SP['h2a'] = box('CATAT CUMA', 84, fg=INK, bg=WHITE)
    SP['h2b'] = box('5 DETIK!', 110, fg=WHITE, bg=INK)
    SP['ph_form'] = phone('v_form.png', 900)
    SP['calc'] = sticker('c_calc.png', 640)
    SP['lbl_kanal'] = box('pilih kanal', 54, fg=INK, bg=(255, 214, 10), weight='ExtraBold')
    SP['lbl_auto'] = box('potongan otomatis', 50, fg=WHITE, bg=INK, weight='ExtraBold')
    SP['laba'] = box('LABA BERSIH: Rp14.350', 70, fg=WHITE, bg=GREEN)
    # s3
    SP['h3a'] = box('SEMUA', 96, fg=INK, bg=WHITE)
    SP['h3b'] = box('LANGSUNG KELIHATAN', 70, fg=WHITE, bg=INK)
    SP['ph_beranda2'] = phone('v_beranda.png', 860)
    SP['hero'] = sticker('v_beranda.png', 720, crop=(48, 204, 1122, 750))
    SP['omzet'] = sticker('c_beranda_0.png', 440)
    SP['lbl_saldo'] = box('saldo kas', 50, fg=INK, bg=(255, 214, 10), weight='ExtraBold')
    # s4
    SP['h4a'] = box('KANAL MANA', 84, fg=INK, bg=WHITE)
    SP['h4b'] = box('PALING CUAN?', 96, fg=WHITE, bg=INK)
    SP['donut'] = sticker('c_beranda_6.png', 800)
    SP['perkanal'] = sticker('c_laporan_2.png', 600)
    SP['anjay'] = box('ANJAY!', 150, fg=INK, bg=(255, 214, 10), r=12)
    # s5
    SP['h5a'] = box('STOK & KASBON', 84, fg=INK, bg=WHITE)
    SP['h5b'] = box('KEPANTAU', 100, fg=WHITE, bg=INK)
    SP['stok'] = sticker('c_stok_4.png', 600, crop=(0, 0, 1074, 1060))
    SP['kasbon'] = sticker('c_laporan_4.png', 560)
    SP['lupa'] = box('GAK LUPA LAGI!', 84, fg=WHITE, bg=INK, r=10)
    SP['ok'] = check_icon(150)
    # s6
    SP['h6a'] = box('LAPORAN LABA RUGI', 74, fg=INK, bg=WHITE)
    SP['h6b'] = box('SEBULAN BERES', 92, fg=WHITE, bg=INK)
    SP['rugi'] = sticker('c_laporan_1.png', 640)
    SP['share'] = sticker('c_laporan_0.png', 680)
    SP['lbl_wa'] = box('kirim ke WhatsApp', 52, fg=WHITE, bg=(37, 190, 90), weight='ExtraBold')
    SP['lbl_pdf'] = box('atau simpan PDF', 52, fg=INK, bg=WHITE, weight='ExtraBold')
    # s7
    SP['p1'] = box('Data aman di HP sendiri', 62, fg=INK, bg=WHITE, weight='ExtraBold')
    SP['p2'] = box('Sekali bayar', 62, fg=INK, bg=WHITE, weight='ExtraBold')
    SP['p3'] = box('Tanpa langganan', 62, fg=INK, bg=WHITE, weight='ExtraBold')
    SP['ok2'] = check_icon(86)
    SP['logo2'] = box('KasRapi', 130, fg=WHITE, bg=TEAL, pad=(40, 20), border=9, r=26)
    SP['cek'] = box('CEK LINK DI BIO', 104, fg=WHITE, bg=INK, r=14)
    SP['link'] = box('lynk.id/ibam2178', 78, fg=INK, bg=WHITE, weight='ExtraBold')
    SP['arrow'] = arrow_down(130)
    # bg stripes per scene
    for s, c in COL.items():
        dark = tuple(int(v * 0.9) for v in c)
        bg = Image.new('RGB', (W + 120, H), c)
        d = ImageDraw.Draw(bg)
        for x in range(-H, W + 120, 120):
            d.polygon([(x, H), (x + 40, H), (x + 40 + H, 0), (x + H, 0)], fill=dark)
        # halftone dots corner
        for yy in range(0, 520, 34):
            for xx in range(0, 520, 34):
                rr = 12 * (1 - math.hypot(xx, yy) / 560)
                if rr > 1.5:
                    for (px, py) in [(W + 120 - 20 - xx, 20 + yy), (20 + xx, H - 20 - yy)]:
                        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=tuple(int(v * 0.78) for v in c))
        SP[f'bg{s}'] = bg

# ---------- scene drawers (u = time in scene, b = beats) ----------
HY1, HY2 = 330, 440  # headline rows

def chip(c, k, u):
    sc, al = pop(u, 0.05)
    put(c, SP[f'chip{k}'], 200 + 10, 250, sc, -3, al)

def headline(c, u, a, b, t0=0.1, t1=0.35):
    sc, al = pop(u, t0, 'slam'); put(c, SP[a], W / 2, HY1 + 10, sc, -2, al)
    sc, al = pop(u, t1, 'slam'); put(c, SP[b], W / 2, HY2 + 20, sc, 2, al)

def s1(c, u, b):
    out = clamp((u - b[3] + 0.05) / 0.25)  # exit progress at beat 3
    ys = [640, 840, 1040]; rots = [-6, 4, -3]
    for k, key in enumerate(['c_shopee', 'c_tiktok', 'c_wa']):
        t0 = b[0] + 0.05 + k * 0.42
        sc, al = pop(u, t0, 'slam')
        jit = math.sin(u * 40 + k) * 4 if b[2] <= u < b[3] else 0
        x = W / 2 + (k - 1) * 60 + slide(u, t0, 0) - out * (1400 if k % 2 else -1400)
        put(c, SP[key], x + jit, ys[k] + jit, sc, rots[k], al)
    if u >= b[1] - 0.05:
        uu = u - b[1]
        sc, al = pop(uu, 0, 'slam'); yo = -out * 900
        put(c, SP['h1a'], W / 2 - 60, 300 + yo, sc, -3, al)
        sc2, al2 = pop(uu, 0.25, 'slam')
        put(c, SP['h1b'], W / 2 - 60, 440 + yo, sc2, 2, al2)
        sc3, al3 = pop(uu, 0.5)
        put(c, SP['q'], 900, 380 + yo, sc3, 12 + 8 * math.sin(u * 7), al3)
    if b[2] <= u < b[3] + 0.3:
        uu = u - b[2]
        sc, al = pop(uu, 0, 'slam')
        put(c, SP['gaktau'], W / 2, 1240 + out * 900, sc, -7, al)
        sc, al = pop(uu, 0.2)
        put(c, SP['x'], 920, 1110 + out * 900, sc, 0, al)
    if u >= b[3]:
        uu = u - b[3]
        sc, al = pop(uu, 0.0)
        put(c, SP['tenang'], W / 2, 330, sc, -3, al)
        sc, al = pop(uu, 0.25, 'slam')
        put(c, SP['logo'], W / 2, 500, sc, 2, al)
        py = 1190 + slide(u, b[3] + 0.3, 900, 0.6)
        put(c, SP['ph_beranda'], W / 2, py, 1.0, -4, 1)

def s2(c, u, b):
    chip(c, 1, u); headline(c, u, 'h2a', 'h2b')
    ph = SP['ph_form']; px, py = 330, 970 + slide(u, 0.2, 1200, 0.5)
    put(c, ph, px, py, 1, 0, 1)
    s, bb = ph.info['s'], ph.info['b']
    ox, oy = px - ph.width / 2 + bb, py - ph.height / 2 + bb
    if u >= b[1]:
        uu = u - b[1]
        d = ImageDraw.Draw(c)
        x0, y0, x1, y1 = ox + 54 * s - 10, oy + 1268 * s - 10, ox + 1114 * s + 10, oy + 1412 * s + 10
        p = eout(uu / 0.25); g = 6 + 4 * math.sin(uu * 14) * (1 - clamp(uu / 1.2))
        d.rounded_rectangle([x0 - g, y0 - g, x0 + (x1 - x0) * p + g, y1 + g], 26, outline=(255, 214, 10), width=12)
        sc, al = pop(uu, 0.1)
        if u < b[2]: put(c, SP['lbl_kanal'], 800, oy + 1150 * s, sc, 4, al)
    if u >= b[2]:
        uu = u - b[2]
        sc, al = pop(uu, 0)
        cal = SP['calc']; cx, cy = 680, 1090
        put(c, cal, cx, cy, sc, 3, al)
        if False:
            # marker under potongan row (red rows y 137-164 in calc coords)
            k = cal.info['scale']; bo = cal.info['b']
            d = ImageDraw.Draw(c)
            p = eout((uu - 0.35) / 0.3)
            lx0 = cx - cal.width / 2 + bo + 30 * k; lx1 = cx + cal.width / 2 - bo - 20 * k
            ly = cy - cal.height / 2 + bo + 175 * k + (lx0 - cx) * math.tan(math.radians(-3)) * 0
            d.line([(lx0, ly + 6), (lx0 + (lx1 - lx0) * p, ly + 6 - 18 * p * 0)], fill=RED, width=10)
        sc, al = pop(uu, 0.3)
        put(c, SP['lbl_auto'], 700, 830, sc, -3, al)
    if u >= b[3]:
        uu = u - b[3]
        sc, al = pop(uu, 0, 'slam')
        put(c, SP['laba'], W / 2, 1330, sc, -4, al)

def s3(c, u, b):
    chip(c, 2, u); headline(c, u, 'h3a', 'h3b')
    put(c, SP['ph_beranda2'], 300, 1000 + slide(u, 0.15, 1200, 0.5), 1, 0, 1)
    if u >= b[1]:
        uu = u - b[1]; sc, al = pop(uu, 0)
        hx, hy = 640, 800
        put(c, SP['hero'], hx, hy, sc, 3, al)
        sc, al = pop(uu, 0.15)
        put(c, SP['lbl_saldo'], 820, 620, sc, -4, al)
        if u >= b[3] + 0.1:
            # circle on margin 24% (crop coords 552..1014, 309..489)
            hs = SP['hero']; k = 720 / 1074; bo = hs.info['b']
            x0 = hx - hs.width / 2 + bo + 552 * k; y0 = hy - hs.height / 2 + bo + 309 * k
            x1 = hx - hs.width / 2 + bo + 1014 * k; y1 = hy - hs.height / 2 + bo + 489 * k
            p = eout((u - b[3] - 0.1) / 0.35)
            ImageDraw.Draw(c).arc([x0 - 16, y0 - 16, x1 + 16, y1 + 16], -90, -90 + 360 * p, fill=(255, 214, 10), width=12)
    if u >= b[2]:
        uu = u - b[2]; sc, al = pop(uu, 0)
        put(c, SP['omzet'], 760, 1180, sc, -4, al)

def s4(c, u, b):
    chip(c, 3, u); headline(c, u, 'h4a', 'h4b')
    if u >= b[1] - 0.2:
        uu = u - (b[1] - 0.2); sc, al = pop(uu, 0)
        put(c, SP['donut'], W / 2, 790, sc, -2, al)
    if u >= b[1] + 0.7:
        uu = u - (b[1] + 0.7); sc, al = pop(uu, 0)
        put(c, SP['perkanal'], 650, 1130 + slide(u, b[1] + 0.7, 300, 0.4), sc, 3, al)
    if u >= b[2]:
        uu = u - b[2]; sc, al = pop(uu, 0, 'slam')
        put(c, SP['anjay'], 330, 1250, sc, -10 + 3 * math.sin(uu * 9), al)

def s5(c, u, b):
    chip(c, 4, u); headline(c, u, 'h5a', 'h5b')
    sc, al = pop(u, 0.4)
    put(c, SP['stok'], 360, 930, sc, -3, al)
    if u >= b[1]:
        uu = u - b[1]; sc, al = pop(uu, 0)
        put(c, SP['kasbon'], 720, 1060, sc, 4, al)
    if u >= b[2]:
        uu = u - b[2]; sc, al = pop(uu, 0, 'slam')
        put(c, SP['lupa'], W / 2, 1320, sc, -3, al)
        sc, al = pop(uu, 0.2)
        put(c, SP['ok'], 940, 1240, sc, 0, al)

def s6(c, u, b):
    chip(c, 5, u); headline(c, u, 'h6a', 'h6b')
    sc, al = pop(u, 0.45)
    rg = SP['rugi']; rx, ry = W / 2, 885
    put(c, rg, rx, ry, sc, -2, al)
    if u > 1.3:
        k = rg.info['scale']; bo = rg.info['b']
        x0 = rx - rg.width / 2 + bo + 10 * k; x1 = rx + rg.width / 2 - bo - 10 * k
        y0 = ry - rg.height / 2 + bo + 770 * k; y1 = ry - rg.height / 2 + bo + 850 * k
        p = eout((u - 1.3) / 0.3)
        ImageDraw.Draw(c).rounded_rectangle([x0, y0, x0 + (x1 - x0) * p, y1], 14, outline=(255, 214, 10), width=10)
    if u >= b[1]:
        uu = u - b[1]; sc, al = pop(uu, 0)
        sh = SP['share']; sx, sy = W / 2, 1320
        put(c, sh, sx, sy, sc, 2, al)
        sc, al = pop(uu, 0.25)
        put(c, SP['lbl_wa'], 790, 1140, sc, -4, al)
        sc, al = pop(uu, 0.75)
        put(c, SP['lbl_pdf'], 270, 1150, sc, 3, al)

def s7(c, u, b):
    ys = [300, 430, 560]
    for k, key in enumerate(['p1', 'p2', 'p3']):
        t0 = [b[0] + 0.05, b[1], b[1] + 0.55][k]
        sc, al = pop(u, t0, 'slam')
        put(c, SP[key], W / 2 + 40, ys[k], sc, [-2, 2, -1][k], al)
        sc, al = pop(u, t0 + 0.15)
        put(c, SP['ok2'], W / 2 - SP[key].width / 2 - 20, ys[k], sc, 0, al)
    sc, al = pop(u, 0.6)
    put(c, SP['logo2'], W / 2, 790, sc, -3, al)
    if u >= b[2]:
        uu = u - b[2]
        sc, al = pop(uu, 0, 'slam')
        put(c, SP['cek'], W / 2, 1010, sc, 2, al)
        sc, al = pop(uu, 0.3, 'slam')
        put(c, SP['link'], W / 2, 1170, sc * (1 + 0.04 * math.sin(uu * 8)), -2, al)
        sc, al = pop(uu, 0.5)
        put(c, SP['arrow'], W / 2, 1340 + 22 * abs(math.sin(uu * 5)), sc, 0, al, shadow=True)

DRAW = {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7}
CAPS = tl.caps()
CAPF = F(52, 'ExtraBold')
KEY = {'KasRapi!', 'cuan?', 'anjir.', 'Anjay!', 'bersih', 'bersihnya', 'otomatis', 'Shopee', 'WhatsApp,', 'PDF.', 'bio', '5', 'beres.', 'margin,', 'kasbon', 'Kasbon', 'langganan.', 'aman'}

def caption(c, t):
    for a, bnd, txt in CAPS:
        if a <= t < bnd:
            words = txt.split()
            sp = CAPF.getlength(' ')
            ws = [CAPF.getlength(w) for w in words]
            tw = sum(ws) + sp * (len(words) - 1)
            x0 = W / 2 - tw / 2; y = 1470
            d = ImageDraw.Draw(c)
            d.rounded_rectangle([x0 - 26, y - 14, x0 + tw + 26, y + 70], 16, fill=INK)
            x = x0
            for w, wl in zip(words, ws):
                col = (255, 214, 10) if w in KEY else WHITE
                d.text((x, y), w, font=CAPF, fill=col); x += wl + sp
            return

def frame(t):
    sc = [s for s in tl.SC if s['start'] <= t][-1]
    u = t - sc['start']; i = sc['i']
    bg = SP[f'bg{i}']
    off = int((t * 70) % 120)
    c = bg.crop((off, 0, off + W, H)).copy()
    DRAW[i](c, u, sc['beats'])
    # global
    put(c, SP['wm'], 160, 165, 1, 0, 1, shadow=False)
    put(c, SP['badge'], W - 230, 165, 1, 0, 1, shadow=False)
    caption(c, t)
    # progress bar
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([60, 1572, W - 60, 1586], 7, fill=INK)
    d.rounded_rectangle([62, 1574, 62 + (W - 124) * t / tl.TOTAL, 1584], 5, fill=WHITE)
    # camera punch/shake on slams
    punch = 0
    for k, bt in enumerate(sc['beats']):
        uu = u - bt
        if 0 <= uu < 0.25: punch = max(punch, (1 - uu / 0.25))
    if u < 0.2 and i > 1: punch = max(punch, 1 - u / 0.2)
    if punch > 0:
        z = 1 + 0.035 * punch
        sx = math.sin(t * 90) * 10 * punch; sy = math.cos(t * 77) * 10 * punch
        bw, bh = W / z, H / z
        x0 = clamp((W - bw) / 2 + sx, 0, W - bw); y0 = clamp((H - bh) / 2 + sy, 0, H - bh)
        c = c.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + bw, y0 + bh))
    # wipe at end of scene
    rem = sc['dur'] - u
    if i < 7 and rem < 0.28:
        p = 1 - rem / 0.28
        nxt = COL[i + 1]
        d = ImageDraw.Draw(c)
        edge = -400 + (W + 800) * eout(p)
        poly = [(edge + 400, 0), (W + 600, 0), (W + 600, H), (edge - 400, H)]
        # block slides from right to left: covered region x > edge
        cov = [(W + 600 - (W + 1000) * eout(p), 0), (W + 600, 0), (W + 600, H), (W + 200 - (W + 1000) * eout(p) - 400, H)]
        d.polygon([(cov[0][0] - 30, 0), cov[1], cov[2], (cov[3][0] - 30, H)], fill=INK)
        d.polygon(cov, fill=nxt)
    return c

def render_range(args):
    a, bnd, path = args
    build()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for n in range(a, bnd):
        p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        build()
        ts = [float(x) for x in sys.argv[2].split(',')]
        ims = [frame(t).resize((360, 640)) for t in ts]
        cols = 6; rows = (len(ims) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * 370, rows * 670), 'gray')
        d = ImageDraw.Draw(sheet)
        for k, im in enumerate(ims):
            x, y = (k % cols) * 370, (k // cols) * 670
            sheet.paste(im, (x, y)); d.text((x + 5, y + 645), f't={ts[k]:.2f}', fill='white')
        sheet.save(sys.argv[3], quality=85)
    elif mode == 'full':
        from multiprocessing import Pool
        N = int(tl.TOTAL * FPS); parts = 4
        rng = [(N * k // parts, N * (k + 1) // parts, f'/tmp/claude-0/kr/build/part{k}.mp4') for k in range(parts)]
        with Pool(parts) as pool: pool.map(render_range, rng)
        with open('/tmp/claude-0/kr/build/list.txt', 'w') as f:
            for r in rng: f.write(f"file '{r[2]}'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', '/tmp/claude-0/kr/build/list.txt', '-c', 'copy', '/tmp/claude-0/kr/build/video.mp4'])
        print('done', N)
