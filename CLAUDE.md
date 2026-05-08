# CLAUDE.md — Skripsi Fauzi Noorsyabani

> Context dan instruksi untuk Claude Code. Baca file ini SEBELUM mengerjakan task apapun di repo.

---

## 1. IDENTITAS PROYEK

| Field | Value |
|-------|-------|
| **Nama** | Fauzi Noorsyabani |
| **NPM** | 227007042 |
| **Prodi** | Sistem Informasi |
| **Fakultas** | Teknik |
| **Universitas** | Universitas Siliwangi (Unsil), Tasikmalaya |
| **Pembimbing I** | Dr. Ir. Acep Irham Gufroni, S.Kom., M.Eng., IPM., ASEAN Eng. (NIDN: 0414038501) |
| **Pembimbing II** | Ir. Andi Nur Rachman, S.T., M.T. (NIDN: 0412088503) |
| **Tahun** | 2026 |
| **Status saat ini** | Draft Laporan Seminar Hasil (revisi dari UP) |

### Judul Tugas Akhir
**ANALISIS DATA AGREGAT PERGURUAN TINGGI NEGERI BADAN LAYANAN UMUM (PTN BLU) MENGGUNAKAN PENDEKATAN *BUSINESS INTELLIGENCE***

---

## 2. RINGKASAN PENELITIAN

### Masalah
- Data PDDikti (Pangkalan Data Pendidikan Tinggi) bersifat **tabel statis & deskriptif** → belum mendukung analisis longitudinal kapasitas akademik.
- Penelitian BI di pendidikan tinggi umumnya level **mikro** (prodi/dashboard internal), bukan PTN BLU.
- Universitas Siliwangi sebagai **PTN BLU** butuh analisis kapasitas akademik berbasis data agregat.

### Rumusan Masalah
1. Bagaimana kondisi kapasitas akademik Unsil (PTN BLU) berdasarkan tren rasio dosen:mahasiswa per prodi secara longitudinal?
2. Bagaimana sistem BI berbasis data warehouse + dashboard analitik dapat mendukung DSS dalam menyajikan informasi kapasitas akademik secara terstruktur?

### Indikator Utama
**Rasio Dosen terhadap Mahasiswa**:
```
Rasio = Jumlah Mahasiswa Aktif / Jumlah Dosen Penghitung Rasio
```

### Sumber Data
- **PDDikti** (Kemendikbudristek) — data agregat institusi
- **Variabel**: jumlah mahasiswa aktif, jumlah dosen tetap, jumlah dosen penghitung rasio, periode pelaporan
- **Periode**: 5 semester
  - Genap 2022/2023
  - Ganjil 2023/2024
  - Genap 2023/2024
  - Ganjil 2024/2025
  - Genap 2024/2025
- **Scope**: institusi (Unsil) + per program studi

### Batasan
- Hanya Unsil — tidak banding antar PT
- Tidak prediktif, tidak evaluasi individu
- Tidak pakai data rinci dosen (umur, beban kerja, pensiun) karena tidak ada di data agregat PDDikti

---

## 3. METODOLOGI: BI ROADMAP (Moss & Atre, 2003)

6 fase, urutan kaku:

| Fase | Output |
|------|--------|
| **1. Justification** | Identifikasi masalah → justifikasi kebutuhan BI |
| **2. Planning** | Cetak biru arsitektur: ETL Python/Colab + DW star schema + dashboard |
| **3. Business Analysis** | Spesifikasi kebutuhan informasi (4 kebutuhan: distribusi mhs, distribusi dosen, nilai rasio, tren longitudinal) |
| **4. Design** | Star schema: 1 fact + 3 dim |
| **5. Construction** | Implementasi ETL + load ke DW |
| **6. Deployment** | Integrasi DW ↔ dashboard, validasi konsistensi |

### Star Schema
```
FACT_RASIO_KAPASITAS
├── jumlah_mahasiswa
├── jumlah_dosen
├── jumlah_dosen_penghitung_rasio
└── rasio (precomputed)
       │
       ├── DIM_WAKTU         (semester, tahun_akademik, periode_pelaporan)
       ├── DIM_UNIVERSITAS   (kode_pt, nama_pt, status)
       └── DIM_PROGRAM_STUDI (kode_prodi, nama_prodi, jenjang, status_aktif)
```

**Grain**: 1 baris fact = 1 prodi × 1 periode pelaporan.

### Pipeline ETL (Python di Google Colab)
```
EXTRACT
└── Filter Unsil dari data nasional PDDikti
└── Drop prodi non-aktif & prodi dengan mhs=0

TRANSFORM
└── Pisah kolom periode → semester + tahun
└── Konversi rasio "1:X" (string) → float
└── Hitung rasio = mhs_aktif / dosen_penghitung_rasio
└── Cleaning umum

LOAD
└── Star schema → file data warehouse
└── Connect ke dashboard
```

---

## 4. STRUKTUR FOLDER YANG DIHARAPKAN

Folder root: `D:\College\Semester-an\SEMESTER 8\Skripsi`

Saran struktur (kalau belum ada, buat):
```
Skripsi/
├── CLAUDE.md                      ← file ini
├── data/
│   ├── raw/                       ← CSV/Excel mentah dari PDDikti
│   ├── interim/                   ← hasil transform sementara
│   └── warehouse/                 ← star schema final (parquet/csv/sqlite)
├── notebooks/                     ← .ipynb untuk Colab/Jupyter
│   ├── 01_extract.ipynb
│   ├── 02_transform.ipynb
│   ├── 03_load_warehouse.ipynb
│   └── 04_eda_validasi.ipynb
├── src/                           ← kode reusable (.py)
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── utils.py
├── dashboard/                     ← file dashboard (Metabase/Tableau/Streamlit/dll)
├── docs/
│   ├── draft_seminar_hasil.docx
│   ├── panduan_TA.pdf
│   ├── alur_pendaftaran.pdf
│   └── referensi/                 ← Creswell, mix method, jurnal
├── output/
│   ├── figures/                   ← PNG/SVG untuk laporan
│   ├── tables/                    ← tabel hasil olahan
│   └── exports/                   ← export ke laporan akhir
└── requirements.txt
```

---

## 5. ATURAN OUTPUT — IKUTI PANDUAN TA UNSIL

### Format Naskah (PANDUAN_TA.pdf)
- **Font**: Times New Roman 12pt
- **Spasi**: 2.0 (double); tabel boleh 1 atau 1.5
- **Margin**: atas 4cm, kiri 4cm, bawah 3cm, kanan 3cm; header/footer 2cm
- **Kertas**: A4, HVS 80 g/m², putih, satu muka
- **Alinea**: indent 1.27cm (1 tab default)
- **Justify** untuk body
- **Sampul**: hardcover biru tua, tinta emas

### Penomoran
- Pendahuluan/awal: angka Romawi kecil (i, ii, iii)
- Isi: angka Arab dengan kode bab (I-1, II-3, III-5)
- Lampiran: L1-1, L2-1, dst (kanan atas)

### Tabel & Gambar
- Tabel: nomor + judul **di atas**, center, tanpa titik akhir (e.g., `Tabel 3.1 Nama Tabel`)
- Gambar: nomor + judul **di bawah**, center
- Penomoran ikut bab: `Tabel 5.3` = tabel ke-3 di Bab 5

### Bahasa & Sitasi
- **Bahasa**: Indonesia baku (EYD), pasif, jangan pakai "saya/aku/kita"
- **Istilah asing**: italic
- **Sitasi**: **Harvard Anglia Style** (Author, Year)
- **Daftar pustaka**: alfabetis, format Harvard
- **Penelitian terkait**: minimal 10 judul, 10 tahun terakhir

### Persamaan
Format: nomor di kanan dengan kode bab → `(2.3)` = persamaan ke-3 Bab 2
```
F = m × a              (2.3)
```

### Abstrak
- 200-250 kata
- Dwibahasa (Indonesia + English)
- 3-5 kata kunci, alfabetis
- Tidak boleh ada tabel/gambar/rumus (kecuali objek penelitian = rumus)

---

## 6. INSTRUKSI UNTUK CLAUDE — PROTOKOL KERJA

### A. PRINSIP UMUM (WAJIB)

1. **Bahasa Indonesia** untuk semua komunikasi dan dokumen output (kecuali code/comment).
2. **Padat. Tajam. Selesai.** — No basa-basi, no penutup, no echo pertanyaan. Kalau bisa 50 kata, jangan 100.
3. **Konsistensi terminologi** — gunakan persis istilah yang sudah dipakai di draft (misal "rasio dosen terhadap mahasiswa", bukan "rasio dosen ke mahasiswa").
4. **Sitasi**: pertahankan format `(Author, Year)` Harvard Anglia. Jangan ganti style.
5. **Italic** untuk istilah asing: *Business Intelligence*, *data warehouse*, *star schema*, *Extract Transform Load*, dll.

### B. SAAT CODING / OLAH DATA

1. **Baca dulu** struktur data sebelum nulis kode. Pakai `df.head()`, `df.dtypes`, `df.info()`.
2. **Reproducibility**: set seed kalau ada randomness, log versi library.
3. **Path**: pakai `pathlib.Path` atau path relatif dari root, **jangan hardcode path Windows absolut**.
4. **Output**: simpan figure ke `output/figures/`, tabel ke `output/tables/`.
5. **Naming**:
   - `df_raw_*` untuk data mentah
   - `df_clean_*` untuk hasil transform
   - `dim_*`, `fact_*` untuk warehouse
6. **Library standard**: `pandas`, `numpy`, `matplotlib`/`seaborn`/`plotly`, `sqlalchemy`, `openpyxl`, `pyarrow`.
7. **Komentar kode**: bahasa Indonesia, hanya untuk logika non-obvious. Skip komentar yang cuma echo nama variabel.
8. **Validasi**: setiap tahap ETL harus ada assertion / sanity check (jumlah baris, dtype, range nilai, null count).
9. **Charts ikut style laporan**: title bahasa Indonesia, font Times New Roman kalau bisa, hindari emoji.

### C. SAAT NULIS / EDIT LAPORAN

1. **Patuh format Panduan TA Unsil** (lihat section 5).
2. **Body paragraf** untuk teori dan pembahasan — bukan bullet panjang.
3. **Bullet** hanya untuk: rumusan masalah, tujuan, batasan, manfaat, perincian teknis.
4. **Setiap claim teoretis = sitasi**. Tidak ada klaim tanpa rujukan.
5. **Penelitian terkait**: format tabel multi-baris per item (Penulis, Judul, Objek, Permasalahan, Metode, Hasil, Perbandingan).
6. **Pertahankan suara akademik pasif**: "dilakukan", "dianalisis", "digunakan" — bukan "saya melakukan".
7. **Jangan menggemukkan**: kalau ide sama, jangan ditulis 2x dengan kalimat beda. Cek draft saat ini ada duplikasi paragraf di BAB III subbab Design — **jangan ulangi pola ini**.

### D. SAAT BIKIN VISUALISASI

1. **Format**: PNG 300dpi untuk laporan, SVG kalau perlu vector.
2. **Style**: simpel, hitam-putih friendly (laporan bisa di-fotokopi B/W).
3. **Label**: bahasa Indonesia, jelas, no jargon kalau bisa dihindari.
4. **Caption**: di bawah gambar, format `Gambar X.Y Judul`.
5. **Untuk dashboard**: warna konsisten, gunakan palette aksesibel (avoid red-green only).

### E. WORKFLOW TYPICAL

| Task user | Action Claude |
|-----------|---------------|
| "Bersihkan data PDDikti" | Cek struktur file → buat script di `src/` atau notebook di `notebooks/` → output ke `data/interim/` |
| "Hitung rasio" | Pakai formula resmi (mhs/dosen_penghitung_rasio), simpan ke fact table |
| "Bikin chart tren" | Line chart per prodi, x=periode, y=rasio, title sesuai konvensi |
| "Update bab III" | Edit `docs/draft_*.docx` mengikuti format Unsil |
| "Bikin star schema" | Implementasi 1 fact + 3 dim, simpan ke `data/warehouse/` (parquet atau sqlite) |
| "Validasi data" | Sanity check: null, range, konsistensi semester, jumlah prodi konsisten antar periode |

### F. JANGAN DILAKUKAN

- ❌ Edit langsung file di `data/raw/` — selalu copy dulu
- ❌ Commit/push tanpa izin
- ❌ Install library aneh tanpa konfirmasi
- ❌ Ubah judul TA atau struktur bab tanpa diminta
- ❌ Tambah penelitian terkait di luar 15 yang sudah ada tanpa diminta
- ❌ Ganti format sitasi (tetap Harvard Anglia)
- ❌ Pakai bahasa Inggris untuk body laporan

---

## 7. FILE REFERENSI YANG TERSEDIA

Letakkan/simpan di `docs/referensi/`:

| File | Fungsi |
|------|--------|
| `PANDUAN_TA.pdf` | **Wajib patuh** — format penulisan Fakultas Teknik Unsil |
| `Panduan_TA-UP_SINTESYS.pdf` | Panduan modul TA di sintesys.unsil.ac.id |
| `Alur_Pendaftaran_Tugas_Akhir_Mahasiswa_Sistem_Informasi.pdf` | SOP pendaftaran (tanggal 1-10, 11-20, 21-30 setiap bulan) |
| `FORMULIR_PERMOHONAN_BIMBINGAN_DAN_SK.pdf` | Form pengajuan |
| `Draft_Laporan_Ujian_Seminar_Hasil_Fauzi_Noorsyabani_227007042.docx` | **Draft aktif** — basis revisi |
| `_Creswell_John_W__Clark_Vicki_L_Plano__Designing_a__pdf_2.pdf` | Creswell — Designing & Conducting Mixed Methods Research |
| `mix_method_creswell_2018.pdf` | Creswell 2018 — Mixed Methods Research design |

> Creswell **bukan** untuk metodologi utama (kita pakai BI Roadmap). Creswell sebagai referensi sekunder kalau pembimbing minta justifikasi pendekatan campuran kualitatif-kuantitatif.

---

## 8. STATUS DRAFT SAAT INI (Snapshot)

**Sudah ada:**
- BAB I lengkap (latar belakang, rumusan, tujuan, batasan, manfaat)
- BAB II lengkap (4 landasan teori + 15 penelitian terkait di Tabel 2.1)
- BAB III lengkap (6 fase BI Roadmap)
- Daftar Pustaka (sudah Harvard Anglia)

**Belum / Perlu Dikerjakan:**
- ❗ **BAB IV Hasil dan Pembahasan** — masih kosong (`# BAB IV HASIL DAN PEMBAHASAN`)
- ❗ **BAB V Kesimpulan dan Saran** — belum ada
- ❗ **Abstrak Indonesia + English** — belum ada
- ❗ **Daftar Tabel & Gambar** — masih placeholder
- ❗ Implementasi ETL aktual (kode Python)
- ❗ Star schema fisik (warehouse file)
- ❗ Dashboard
- ❗ Validasi konsistensi DW vs dashboard

**Issue di draft:**
- Subbab 3.1.4 (Design) ada **duplikasi paragraf** — paragraf yang sama diulang 2x. Perlu dirapikan.
- Tabel 3.1 dan Gambar 3.1-3.4 masih placeholder `*[...]*` — belum di-insert real.

---

## 9. CHECKLIST SEBELUM SEMINAR HASIL

- [ ] BAB IV terisi dengan analisis longitudinal 5 periode
- [ ] BAB V kesimpulan menjawab rumusan masalah Bab I
- [ ] Abstrak ID + EN (200-250 kata)
- [ ] Semua gambar/tabel ter-insert dan ter-cite di teks
- [ ] Daftar Tabel & Daftar Gambar auto-update
- [ ] Halaman pengesahan + tanda tangan pembimbing
- [ ] Lembar pernyataan keaslian + materai
- [ ] Format margin, font, spasi sesuai panduan
- [ ] Penomoran halaman benar (i,ii,iii untuk awal; I-1, II-1 untuk isi)
- [ ] Sitasi Harvard konsisten
- [ ] Daftar pustaka alfabetis
- [ ] Draft Artikel Ilmiah (syarat seminar hasil)
- [ ] SK Bimbingan TA + Lembar Bimbingan + Transkrip Nilai

---

## 10. KOMUNIKASI

- Default: **bahasa Indonesia, padat, langsung ke jawaban**.
- Kalau ambigu, **bertanya 1 pertanyaan singkat** sebelum kerja besar — jangan asumsi luas.
- Kalau task butuh > 5 menit eksekusi, **kasih plan dulu** sebelum jalan.
- Kalau hasil mengandung uncertainty (data tidak lengkap, asumsi diambil), **kasih tahu eksplisit** di akhir output.

---

*File ini = source of truth. Update kalau ada perubahan scope, judul, atau pembimbing.*
