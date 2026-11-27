# Video Promosi TikTok KasRapi (Remotion, 9:16)

- Ukuran: **1080×1920**, **30 fps**, durasi **28 detik** (840 frame)
- 3 komposisi = 3 variasi hook (lihat `HOOK-DAN-SCRIPT.md`):
  - `KasRapi-V1-UangKemana`
  - `KasRapi-V2-PotonganShopee`
  - `KasRapi-V3-UangDapur`
- Adegan: Hook (3 dtk) → Masalah: potongan Shopee & modal (5 dtk) → Perkenalan + demo aplikasi di bingkai HP (11 dtk) → Offline di Android, iPhone, Laptop (5 dtk) → CTA "Link di bio" (4 dtk)
- Tampilan aplikasi di dalam HP adalah tiruan setia `tools/Aplikasi-UMKM.html` dengan angka dari tombol "Isi Data Contoh".

## Struktur
```
src/
  Root.tsx              3 komposisi + teks hook (ubah di sini / di Studio)
  KasRapiPromo.tsx      urutan adegan & durasi
  theme.ts              warna, font Plus Jakarta Sans, format Rupiah
  scenes/               Hook, Problem, AppDemo, Offline, CTA
  components/           Phone (mockup), AppScreen (UI KasRapi), Background, Icons, Text
```

## Sebelum render
1. Link toko sudah diisi `lynk.id/ibam2178` di `src/Root.tsx` (ubah di sana atau di panel Props Remotion Studio bila berganti).
2. Pastikan internet menyala saat render pertama (font Plus Jakarta Sans diunduh dari Google Fonts).

## Perintah terminal untuk merender MP4 di komputer Anda

Butuh **Node.js 18+** (cek: `node -v`). FFmpeg tidak wajib, Remotion sudah membawanya sendiri.

```bash
# 1. Ambil kode (sekali saja)
git clone https://github.com/utamaibam-commits/PRODUK-DIGITAL1.git
cd PRODUK-DIGITAL1
git checkout claude/project-thread-bebutu   # lewati jika PR sudah di-merge ke main
cd tiktok-motion

# 2. Pasang dependency (sekali saja)
npm install

# 3. (Opsional) Lihat & edit video di browser sebelum render
npx remotion studio

# 4. Render ketiga variasi menjadi MP4 (hasil di folder tiktok-motion/out/)
npx remotion render KasRapi-V1-UangKemana out/KasRapi-V1-UangKemana.mp4
npx remotion render KasRapi-V2-PotonganShopee out/KasRapi-V2-PotonganShopee.mp4
npx remotion render KasRapi-V3-UangDapur out/KasRapi-V3-UangDapur.mp4

# atau sekaligus:
npm run render:all

# 5. (Opsional) Gambar sampul/cover untuk Lynk.id atau TikTok
npx remotion still KasRapi-V1-UangKemana out/cover.png --frame=420
```

Windows: jalankan perintah di atas lewat **PowerShell** atau **Command Prompt**; sama persis.

Laptop lambat? Tambahkan `--concurrency=2` di akhir perintah render.

## Audio: musik, sound effect & voiceover (sudah terpasang)
Ketiga video sudah lengkap dengan audio, jadi tidak perlu tambah musik lagi di TikTok.
- **Musik latar & sound effect**: dibuat sendiri secara sintetis oleh `scripts/buat-audio.py` (bebas hak cipta, aman dari klaim Content ID). Hasil: `public/audio/music.wav` dan `public/audio/sfx/*.wav`. Buat ulang dengan `python3 scripts/buat-audio.py` (butuh numpy).
- **Voiceover**: suara pria Bahasa Indonesia dari Speko (provider Cartesia), satu file per video: `public/audio/vo-v1.wav`, `vo-v2.wav`, `vo-v3.wav`. Tiap kalimat sudah disinkronkan ke adegannya.
- **Pengaturan mix**: `src/SoundTrack.tsx` (daftar SFX per frame, volume musik otomatis turun saat ada voiceover).
- Ganti voiceover: timpa file `public/audio/vo-vN.wav` dengan rekaman sendiri (durasi maks 28 detik), lalu render ulang. Kosongkan prop `voiceover` di `src/Root.tsx` untuk versi tanpa suara narator.

## Lisensi Remotion
Gratis untuk perorangan dan perusahaan dengan maksimal 3 karyawan. Perusahaan lebih besar butuh lisensi (lihat https://remotion.dev/license).
