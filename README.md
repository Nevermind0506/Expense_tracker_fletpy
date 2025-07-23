# 💸 Expense Tracker App (Python + Flet)

**Expense Tracker** adalah aplikasi berbasis Python yang menggunakan framework [Flet](https://flet.dev/) untuk mencatat, mengelola, dan menganalisis pengeluaran pribadi. Aplikasi ini berjalan sebagai desktop UI dan memungkinkan pengguna menambahkan pengeluaran berdasarkan judul, jumlah, kategori, dan tanggal.

![preview](https://user-images.githubusercontent.com/yourusername/yourimage.png) <!-- (Opsional: screenshot app jika ada) -->

## ✨ Fitur

- 📅 **Pilih Tanggal**: Tambahkan pengeluaran berdasarkan tanggal.
- 🧾 **Filter Bulanan**: Lihat pengeluaran berdasarkan bulan tertentu atau seluruh data.
- 📊 **Pie Chart Dinamis**: Tampilkan distribusi kategori pengeluaran dalam bentuk grafik.
- 📈 **Progress Bar per Kategori**: Lihat seberapa besar porsi setiap kategori terhadap total pengeluaran.
- 💾 **Simpan Data Otomatis**: Data disimpan secara lokal dalam file `expenses.json`.
- ⚠️ **SnackBar Notifikasi**: Menampilkan pesan notifikasi untuk aksi seperti sukses menambahkan, error, atau menghapus data.

## 🖥️ Screenshot

> (Tambahkan tangkapan layar aplikasi Anda di sini jika tersedia.)

## 📦 Instalasi

1. **Clone repositori**

   ```bash
   git clone https://github.com/yourusername/expense-tracker-flet.git
   cd expense-tracker-flet
   ```

2. **Buat environment dan install dependencies**

   ```bash
   python -m venv env
   source env/bin/activate   # Windows: env\Scripts\activate
   pip install flet
   ```

3. **Jalankan aplikasi**

   ```bash
   python main.py
   ```

## 🧠 Teknologi yang Digunakan

- [Python 3.10+](https://www.python.org/)
- [Flet](https://flet.dev/): UI framework berbasis Flutter untuk Python
- JSON (untuk penyimpanan data lokal)

## 📁 Struktur File

```
expense-tracker-flet/
│
├── main.py               # File utama aplikasi
├── expenses.json         # File penyimpanan data lokal (akan dibuat otomatis)
└── README.md             # Dokumentasi proyek
```

## 🛠️ Todo / Pengembangan Selanjutnya

- [ ] Fitur edit pengeluaran
- [ ] Export data ke CSV
- [ ] Sinkronisasi dengan penyimpanan cloud (Google Drive, Firebase, dll)
- [ ] Mode statistik mingguan / tahunan

## 📃 Lisensi

Proyek ini berlisensi di bawah [MIT License](LICENSE).

---

Jika Anda ingin saya tambahkan **badge**, **GIF demo**, atau **logo khusus**, beri tahu saya.
