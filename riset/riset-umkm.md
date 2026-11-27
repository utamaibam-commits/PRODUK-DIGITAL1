# Riset Masalah UMKM & Penentuan Ide Tools

Tanggal riset: 27 November 2026 · Target: pelaku UMKM Indonesia (warung, kuliner rumahan, fashion/olshop, reseller, jasa kecil) · Harga jual target: Rp49.000 – Rp79.000 di Lynk.id

---

## 1. Ringkasan temuan

| # | Masalah | Bukti / sumber | Seberapa sering terasa | Bisa diselesaikan app offline 1 file? |
|---|---|---|---|---|
| 1 | **Uang usaha & uang pribadi campur**, tidak tahu sebenarnya untung atau tidak | Riset OCBC × NielsenIQ (Business Fitness Index 2024): hanya **46%** UMKM yang sepenuhnya memisahkan keuangan bisnis dan personal ([Pasardana](https://pasardana.id/news/2024/9/6/riset-hanya-46-umkm-yang-sepenuhnya-pisahkan-keuangan-bisnis-dan-personal), [PR Newswire](https://prnewswire.com/apac/news-releases/only-46-of-msmes-fully-separate-their-business-and-personal-finances-ocbc-simplifies-the-process-for-entrepreneurs-to-open-a-business-checking-account-100-digital-302240246.html), [Investortrust](https://investortrust.id/financial/37652/riset-ocbc-dan-niq-mayoritas-umkm-belum-pisahkan-keuangan-bisnis-dan-personal)) | Setiap hari | Ya, sangat cocok |
| 2 | **Pencatatan arus kas harian berantakan** (nota hilang, catat di buku/ingatan, lupa pengeluaran kecil) | Artikel & jurnal: kesalahan umum mencatat keuangan UMKM ([RRI](https://rri.co.id/makassar/ekonomi/umkm/2041728/kesalahan-pelaku-umkm-saat-mencatat-keuangan), [Pegadaian](https://pegadaian.co.id/artikel/inspirasi/7-masalah-keuangan-umkm-yang-sering-dijumpai-plus-solusi), [Binus](https://binus.ac.id/bekasi/2025/03/pentingnya-memisahkan-keuangan-pribadi-dan-bisnis-untuk-umkm/)) | Setiap hari | Ya |
| 3 | **Laba tergerus biaya marketplace** — potongan admin, layanan, pemrosesan pesanan di Shopee/TikTok Shop dkk. bisa tembus **~30%** dari harga jual; seller mulai pindah jualan via WA/IG/website sendiri | [Katadata: biaya marketplace bisa tembus 30%](https://katadata.co.id/digital/e-commerce/6a0448d937533/biaya-di-marketplace-bisa-tembus-30-seller-umkm-keluhkan-margin-kian-tipis), [Katadata: untung makin tipis](https://katadata.co.id/indepth/telaah/6a0cb36301a00/untung-makin-tipis-seller-online-terimpit-biaya-berlapis-di-marketplace), [Bisnis.com: migrasi UMKM dari TikTok Shop-Shopee](https://ekonomi.bisnis.com/read/20260512/12/1972990/di-balik-fenomena-migrasi-umkm-dari-tiktok-shop-shopee-cs), [Bisnis.com: biaya Rp1.250/pesanan](https://teknologi.bisnis.com/read/20250812/266/1901402/biaya-rp1250-per-pesanan-berisiko-tekan-jumlah-transaksi-shopee-dan-tokopedia) | Setiap transaksi online | Ya (hitung potongan per kanal) |
| 4 | **Stok tidak terpantau** — barang habis tanpa sadar, atau modal mengendap | Masalah klasik di jurnal manajemen UMKM; muncul di daftar masalah keuangan Pegadaian | Mingguan | Ya |
| 5 | **Salah hitung HPP** | Sudah diselesaikan produk lama: *Kalkulator HPP UMKM* | Saat menentukan harga | Sudah ada produknya |
| 6 | **Kasbon / piutang pelanggan** lupa ditagih | Umum di warung & usaha jasa | Mingguan | Ya, fitur tambahan |

## 2. Analisis

Masalah 1–4 saling terhubung dan muncul di **satu momen yang sama: saat terjadi transaksi**. Pemilik UMKM menjual lewat banyak kanal (offline, WhatsApp, Shopee, TikTok Shop), uang masuk ke dompet/rekening pribadi, lalu di akhir bulan tidak bisa menjawab pertanyaan paling dasar: *"Bulan ini sebenarnya untung berapa, dan lewat kanal mana?"*

Kalkulator HPP (produk lama) menjawab "harga jual saya harus berapa?" **sebelum** berjualan. Masalah yang belum terjawab adalah **pencatatan harian setelah berjualan**. Karena itu produk baru ini sengaja **tidak mengulang** kalkulator HPP. Ia melengkapinya: pembeli kalkulator HPP adalah calon pembeli produk ini (peluang *bundling* / *upsell*).

Kenapa cocok untuk web app offline Rp49rb–79rb:
- Aplikasi pembukuan populer berbasis langganan/online; banyak UMKM keberatan dengan biaya bulanan, sinyal tidak stabil, atau khawatir data diunggah ke server. Produk sekali bayar + offline + data hanya di HP sendiri menjawab tiga keberatan itu sekaligus.
- Satu file HTML mudah dikirim lewat Lynk.id dan dibuka di Android, iPhone, dan laptop.

## 3. Masalah yang dipilih

> **"Uang masuk-keluar tercampur dan tidak tercatat, sehingga UMKM tidak tahu laba bersih sebenarnya, apalagi setelah dipotong biaya marketplace."**

## 4. Ide produk: **KasRapi — Buku Kas, Stok & Laba Bersih UMKM**

Nama file wajib: `Aplikasi-UMKM.html` · Harga rekomendasi: **Rp59.000** (sekali bayar)

Janji utama: *Catat penjualan 5 detik, langsung tahu laba bersih setelah potongan Shopee/TikTok Shop, stok berkurang otomatis, dan uang pribadi terpisah dari uang usaha. 100% offline.*

### Spesifikasi fitur

**A. Beranda (Dashboard)**
- Kartu saldo kas usaha, omzet, laba bersih, dan pengeluaran bulan ini.
- Grafik batang SVG 7 hari terakhir (pemasukan vs pengeluaran).
- Grafik donat SVG omzet per kanal penjualan (Offline, WhatsApp, Shopee, TikTok Shop, dll).
- *Progress bar* target omzet bulanan.
- Peringatan stok menipis dan piutang/kasbon belum lunas.

**B. Catat Transaksi**
- Tiga jenis: **Penjualan**, **Pengeluaran Usaha**, **Ambil Uang Pribadi (Prive)**.
- Penjualan: pilih produk (harga & modal terisi otomatis), jumlah, kanal penjualan. Potongan kanal (persen + biaya tetap per pesanan) dihitung otomatis lalu ditampilkan *laba bersih transaksi* sebelum disimpan.
- Status **Lunas / Kasbon (piutang)** dengan nama pelanggan.
- Riwayat transaksi dengan pencarian dan filter, bisa dihapus.

**C. Produk & Stok**
- Daftar produk: nama, harga jual, modal (HPP) per unit, stok, batas stok minimum.
- Stok berkurang otomatis saat penjualan; tombol tambah stok (restock).
- Lencana merah "Stok menipis".

**D. Laporan**
- Laporan laba rugi bulan berjalan / pilih bulan: omzet, potongan marketplace, HPP terjual, pengeluaran, **laba bersih**, prive.
- Tabel laba per kanal (ketahuan kanal mana yang paling "menggerus" untung).
- Produk terlaris.
- Daftar kasbon dengan tombol "Tandai lunas".
- **Cetak / Simpan PDF** (CSS print khusus).
- **Kirim ringkasan ke WhatsApp** (teks rapi via `wa.me` / share).

**E. Pengaturan**
- Nama usaha, target omzet bulanan.
- Atur persentase & biaya tetap potongan tiap kanal (nilai awal hanya contoh, wajib dicek sendiri karena tarif marketplace berubah).
- Mode Gelap.
- **Backup (Export JSON)** & **Restore (Import JSON)**.
- **Isi Data Contoh** (satu klik) dan Hapus Semua Data.

**F. Bantuan**
- Tombol **Pengguna Android** / **Pengguna iPhone (iOS)** dengan langkah membuka file dan menambah ke Layar Utama.
- Tips menjaga data (backup rutin, jangan hapus data browser).

### Syarat teknis
- 1 file HTML, tanpa CDN, font sistem, ikon SVG inline, grafik SVG murni.
- `localStorage` otomatis tiap perubahan.
- Mobile-first: *bottom navigation* di HP, *sidebar* di layar ≥ 900px.
- Animasi transisi tab, toast, `font-variant-numeric: tabular-nums`.
- Format Rupiah `id-ID`.

### Batasan jujur (untuk copywriting)
- Data hanya ada di perangkat & browser yang dipakai; ganti HP perlu Backup/Restore.
- Tarif potongan marketplace diisi/diubah sendiri oleh pengguna; aplikasi tidak mengambil tarif resmi secara otomatis (karena offline).
- Di iPhone, `localStorage` untuk file lokal bergantung pada cara membuka; panduan menyarankan membuka lewat browser dan rutin backup.
