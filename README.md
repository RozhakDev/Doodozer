# Doodozer CLI - Pengunduh Video DoodStream Cepat & Bersih via Command-Line.

![Dood-NG Logo](https://github.com/user-attachments/assets/c7b3cc44-c0bd-48c2-b0ce-4dc69bc97195)
<p align="left">
    <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python 3.8+">
    <img src="https://img.shields.io/badge/Lisensi-MIT-green.svg" alt="Lisensi MIT">
    <img src="https://img.shields.io/badge/Status-Aktif-brightgreen" alt="Status Proyek">
    <img src="https://img.shields.io/badge/Kontribusi-Dipersilakan-orange" alt="Kontribusi">
</p>

**Doodozer CLI** adalah sebuah _command-line interface_ (CLI) tool yang dirancang untuk memberikan pengalaman terbaik dalam mengunduh video dari DoodStream. Proyek ini merupakan evolusi dari [Dood-NG (versi web)]() yang diadaptasi untuk kemudahan penggunaan di terminal, terutama bagi pengguna di lingkungan seperti Termux di Android.

Ucapkan selamat tinggal pada iklan yang mengganggu dan pop-up yang tidak jelas. Fokus kami adalah menyediakan alat yang cepat, efisien, dan fungsional langsung dari genggaman terminal Anda.

## 📖 Tentang Proyek

Proyek ini lahir dari kebutuhan akan sebuah alat yang efisien dan aman untuk mengakses konten dari DoodStream tanpa antarmuka grafis. Situs aslinya sering kali dipenuhi dengan iklan agresif yang merusak pengalaman dan menimbulkan risiko keamanan. Doodozer CLI hadir sebagai solusi _lightweight_ dengan memprioritaskan:

* **Keamanan & Privasi:** Tidak ada interaksi dengan iklan, pelacak, atau skrip berbahaya.
* **Efisiensi:** Proses pengunduhan berjalan secara asinkron untuk performa maksimal.
* **Kemudahan Akses:** Didesain untuk mudah digunakan di berbagai platform, termasuk lingkungan server dan mobile via Termux.
* **Kode Berkualitas:** Dibangun dengan prinsip OOP, struktur modular, dan kode Python yang bersih.

## ✨ Fitur Utama

* **Unduhan Asinkron:** Dibangun menggunakan `asyncio` dan `aiohttp` untuk menangani proses unduhan secara non-blocking, menghasilkan performa yang sangat cepat.
* **Antarmuka CLI Profesional:** Dilengkapi dengan argumen yang jelas, pesan bantuan (`--help`) yang detail, dan validasi input untuk pengalaman pengguna yang intuitif.
* **Bebas Gangguan:** Mengambil _direct download link_ tanpa perlu membuka browser, sepenuhnya menghindari iklan dan pop-up.
* **Progress Bar Informatif:** Memberikan umpan balik visual saat proses unduhan berlangsung menggunakan tqdm, sehingga Anda tahu persis progresnya.
* **Struktur Kode Bersih:** Dirancang dengan struktur proyek yang rapi, menerapkan OOP, dan memisahkan setiap concern untuk kemudahan pengembangan di masa depan.

## 🎞️ Contoh Penggunaan & Tampilan

Berikut adalah contoh bagaimana Doodozer CLI bekerja di terminal.

### 1. Menjalankan Perintah Unduhan Dasar:

```bash
python main.py https://d-s.io/e/abc123xyz
```

**Output Terminal:**

```text
2025-08-26 17:39:23 [INFO] - Mengunduh 1 video...
2025-08-26 17:39:23 [INFO] - Memproses video 1/1: https://d-s.io/d/abc123xyz
2025-08-26 17:39:23 [INFO] - Memproses URL: https://d-s.io/d/abc123xyz
2025-08-26 17:39:24 [INFO] - Direct download link berhasil dibuat untuk 'Night Skyline Manila - DoodStream'
2025-08-26 17:39:24 [INFO] - Video akan disimpan di: /mnt/c/Doodozer/Night Skyline Manila - DoodStream.mp4
2025-08-26 17:39:25 [INFO] - Memulai proses pengunduhan...
Night Skyline Manila - DoodStream.mp4: 100%|█████████████████████████████████████████████████████████████████████| 3.33M/3.33M [00:09<00:00, 386kB/s]2025-08-26 17:39:34 [INFO] - 
Unduhan selesai! Video berhasil disimpan.
```

### 2. Menampilkan Opsi Bantuan (`--help`):

```bash
python main.py --help
```

**Output Bantuan:**

```text
python main.py --help
usage: main.py [-h] [-o OUTPUT_PATH] [-v] [--no-progress] URL

Doodozer CLI - Alat Pengunduh Video dari DoodStream.

  -h, --help            show this help message and exit
  -o, --output OUTPUT_PATH  Nama file atau path untuk menyimpan video
  -v, --verbose         Aktifkan mode verbose
  --no-progress         Nonaktifkan progress bar
```

## 🛠️ Teknologi yang Digunakan

* **Bahasa:** [Python 3.8+](https://www.python.org/)
* **Core Libraries:**
  * [Asyncio](https://docs.python.org/3/library/asyncio.html) - Untuk fondasi pemrograman asinkron.
  * [Aiohttp](https://docs.aiohttp.org/) - Untuk request HTTP asinkron.
  * [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Untuk parsing konten HTML.
  * [Tqdm](https://github.com/tqdm/tqdm) - Untuk progress bar yang elegan.
  * [Aiofiles](https://github.com/Tinche/aiofiles) - Untuk operasi file I/O asinkron.

## 🚀 Instalasi

Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut.

1. **Prasyarat**
    Pastikan Anda telah menginstal **Python versi 3.8 atau lebih tinggi**.

2. **Kloning Repositori**
   
   ```bash
   git clone https://github.com/RozhakDev/Doodozer.git
   cd Doodozer
   ```

3. **Siapkan Lingkungan Virtual & Dependensi**
    Sangat disarankan untuk menggunakan lingkungan virtual (`venv`) untuk mengisolasi dependensi proyek.
   
   ```bash
   # Buat dan aktifkan venv
   python -m venv venv
   source venv/bin/activate  # Di Windows, gunakan: venv\Scripts\activate
   
   # Instal semua dependensi yang dibutuhkan
   pip install -r requirements.txt
   ```

Setelah langkah-langkah ini selesai, Doodozer CLI siap digunakan!

## ⚙️ Cara Penggunaan

Gunakan perintah `python main.py` diikuti dengan URL DoodStream dan opsi tambahan jika diperlukan.

1. **Unduhan Paling Sederhana:**
    Nama file akan dibuat secara otomatis dari judul video.
   
   ```bash
   python main.py "URL_VIDEO_DOODSTREAM"
   ```
2. **Unduhan dengan Nama File Kustom:**
    Gunakan flag `-o` atau `--output` untuk menentukan nama file.
   
   ```bash
   python main.py "URL_VIDEO_DOODSTREAM" -o "video_favorit_saya.mp4"
   ```
3. **Simpan ke Direktori Lain:**
    Anda juga bisa menentukan path direktori. Nama file akan tetap dibuat otomatis.
   
   ```bash
   python main.py "URL_VIDEO_DOODSTREAM" -o "/path/untuk/menyimpan/video/"
   ```
4. **Mode Verbose:**
    Gunakan flag -v untuk melihat log yang lebih detail, berguna untuk debugging.
   
   ```bash
   python main.py "URL_VIDEO_DOODSTREAM" -v
   ```

## ⚠️ Peringatan (Warning)
Alat ini dibuat untuk tujuan **edukasi dan penelitian semata**. Pengguna bertanggung jawab penuh atas bagaimana mereka menggunakan alat ini. Mengunduh konten berhak cipta tanpa izin dapat melanggar hukum di negara Anda.

Harap gunakan alat ini dengan bijak dan hormati hak cipta para pembuat konten. Pengembang tidak bertanggung jawab atas penyalahgunaan perangkat lunak ini.

## ☕ Dukung Pengembangan

Jika Anda ingin mendukung pengembangan proyek ini, Anda dapat memberikan donasi melalui:

- [Trakteer](https://trakteer.id/rozhak_official/tip?)
- [PayPal](https://paypal.me/rozhak9)

Setiap dukungan sangat berarti dan membantu proyek ini terus berkembang!

## 🤝 Kontribusi

Kami sangat terbuka untuk kontribusi! Jika Anda memiliki ide untuk fitur baru, perbaikan bug, atau peningkatan lainnya, silakan berbagi dengan kami. Kami senang menerima kontribusi dari komunitas dan akan memastikan bahwa setiap kontribusi yang diterima akan dihargai dan diintegrasikan ke dalam proyek.

## 📜 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.