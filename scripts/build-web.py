"""Bangun versi link (web app / PWA) KasRapi ke folder docs/ untuk GitHub Pages.

Jalankan dari root repo:  python3 scripts/build-web.py
Sumber tetap satu: tools/Aplikasi-UMKM.html. Ikon dibuat dengan Pillow.
"""
import json
import os
import shutil

from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'tools', 'Aplikasi-UMKM.html')
OUT = os.path.join(ROOT, 'docs', 'kasrapi')
VERSION = 'kasrapi-v1.1'
TEAL = (15, 118, 110)

os.makedirs(os.path.join(OUT, 'icons'), exist_ok=True)


def icon(size, pad=0.0, rounded=False):
    S = size * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S // 4, fill=TEAL)
    else:
        d.rectangle([0, 0, S, S], fill=TEAL)
    # garis grafik naik (sama dengan ikon di aplikasi: 50,112 76,84 96,101 130,61 pada kanvas 180)
    pts = [(50, 112), (76, 84), (96, 101), (130, 61)]
    k = S / 180
    c = S / 2
    sc = 1 - pad
    pts = [(c + (x * k - c) * sc, c + (y * k - c) * sc) for x, y in pts]
    w = int(14 * k * sc)
    d.line(pts, fill='white', width=w, joint='curve')
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill='white')
    return im.resize((size, size), Image.LANCZOS)


icon(192).save(os.path.join(OUT, 'icons', 'icon-192.png'))
icon(512).save(os.path.join(OUT, 'icons', 'icon-512.png'))
icon(512, pad=0.2).save(os.path.join(OUT, 'icons', 'maskable-512.png'))
icon(180).convert('RGB').save(os.path.join(OUT, 'icons', 'apple-touch-icon.png'))
icon(64, rounded=True).save(os.path.join(OUT, 'icons', 'favicon-64.png'))

html = open(SRC, encoding='utf-8').read()
start = html.index('<link rel="apple-touch-icon"')
end = html.index('>', start) + 1
html = html[:start] + (
    '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
    '<link rel="manifest" href="manifest.webmanifest">'
) + html[end:]
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)

manifest = {
    'name': 'KasRapi — Buku Kas, Stok & Laba UMKM',
    'short_name': 'KasRapi',
    'description': 'Buku kas, stok & laba bersih UMKM. Jalan offline, data hanya di perangkat Anda.',
    'lang': 'id',
    'start_url': './',
    'scope': './',
    'display': 'standalone',
    'orientation': 'any',
    'background_color': '#0f766e',
    'theme_color': '#0f766e',
    'icons': [
        {'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'icons/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}
json.dump(manifest, open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

sw = """// Service worker KasRapi: simpan aplikasi di perangkat agar jalan tanpa internet.
const CACHE = '%s';
const FILES = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png',
  './icons/maskable-512.png', './icons/apple-touch-icon.png', './icons/favicon-64.png'];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
// Cache dulu (instan & offline), lalu perbarui diam-diam bila ada internet.
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(caches.open(CACHE).then(async (c) => {
    const hit = await c.match(req, {ignoreSearch: true});
    const net = fetch(req).then((res) => { if (res.ok) c.put(req, res.clone()); return res; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    const res = await net;
    return res || (req.mode === 'navigate' ? c.match('./index.html') : Response.error());
  }));
});
""" % VERSION
open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write(sw)

landing = """<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>KasRapi</title>
<link rel="icon" href="kasrapi/icons/favicon-64.png">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;font-family:system-ui,sans-serif;background:#0f766e;color:#fff;text-align:center;padding:24px}
a{display:inline-block;margin-top:18px;background:#fff;color:#0f766e;font-weight:800;padding:14px 22px;border-radius:14px;text-decoration:none}</style></head>
<body><main><h1>KasRapi</h1><p>Buku kas, stok &amp; laba bersih untuk UMKM.</p>
<a href="https://lynk.id/ibam2178">Dapatkan di Lynk.id</a></main></body></html>
"""
open(os.path.join(ROOT, 'docs', 'index.html'), 'w', encoding='utf-8').write(landing)
open(os.path.join(ROOT, 'docs', '.nojekyll'), 'w').close()
print('ok ->', os.path.relpath(OUT, ROOT))
