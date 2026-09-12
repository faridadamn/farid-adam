# Farid Adamn - Portal Aplikasi

Halaman depan `faridadamn.my.id`: satu pintu masuk ke semua aplikasi yang **sudah live dan dipakai**.

- Live: `https://faridadamn.my.id/`
- Repo ini sumber versi live-nya. Deploy = copy `index.html` ke `/var/www/faridadamn-landing/index.html` di VPS.

## Isi portal

12 pintu dalam 4 kelompok:

- **Produk & bisnis**: Payu (`/payu/`), ApotekKilat, WMS Gudang (`/wms/`), FA Business OS
- **Kerja & belajar**: Daily Planner (`/planner/`), FA Reader, Pelajari (`/pelajari/`), Temanulis (`/temanulis/`)
- **Uang & mobilitas**: UangKu, Orderan
- **Infrastruktur**: Ngobrol (`/ngobrol/`), 9Router (`/9router/`)

Kerja.id belum punya URL live, jadi ditandai apa adanya (bukan link palsu), arahnya ke repo GitHub.

## Cara kerja

Single-file static HTML, tanpa dependency dan tanpa build step.

- **Tema**: terang dan gelap, pilihan disimpan di localStorage. Kalau user belum pernah memilih, ikut preferensi sistem.
- **Tombol Cek semua**: menembak tiap aplikasi dengan fetch mode no-cors. Mode itu sengaja dipakai karena hasilnya cuma bisa dibaca sebagai server menjawab atau tidak menjawab (respons opaque), jadi label yang dipakai terjangkau, bukan klaim kode HTTP tertentu.
- **Dot status**: kosong sebelum dicek, tidak ada state palsu di render awal.

## Aturan yang dipegang

- Tidak ada angka karangan. Angka yang tampil (12 pintu, 35 repo publik) dihitung dari sumber nyata.
- Tidak ada link mati. Kerja.id ditulis apa adanya sebagai belum live.
- Kontras teks minimal 4.5:1 di kedua tema. Accent untuk teks dipisah dari accent visual (accent-text) supaya teks 11px tetap lolos.
- Tap target kontrol minimal 44px, tanpa overflow horizontal di 390px.

## Verifikasi

node verify-portal.js (Playwright) mengecek 18 poin: jumlah baris, link mati, toggle tema, kontras terhitung, tombol cek, keyboard, overflow desktop dan mobile, tap target, dan error JS. Terakhir dijalankan 12 Sep 2026: 18/18 PASS.

## Catatan pindah dari portofolio lama

Sampai 12 Sep 2026 halaman ini adalah living portfolio (hero profil, ROI calculator, showcase, paket harga, build log Notion). Portal menggantikannya karena domain sekarang dipakai sebagai pintu masuk aplikasi.

- `ARCHIVE_portofolio_lama_20260912.html`: salinan utuh portofolio lama.
- Script `farid_build_log.py` (append build log mingguan) dipensiunkan ke `_retired/` di VPS karena targetnya halaman lama.
