# REVISI BAB III — Draft Laporan Seminar Hasil

> File: `Draft_Laporan_Ujian_Seminar_Hasil_Fauzi_Noorsyabani_227007042.docx`
> Target subbab: **BAB III METODOLOGI PENELITIAN → 3.1 Tahapan Penelitian**
> Status: ada **issue duplikasi paragraf** + **typo italic** + **placeholder gambar/tabel belum diisi**

---

## 1. KONTEKS REVISI

### Catatan Dosen (Poin 15)
> "Au tdny diandaikan aja sub heading 2, jadi masuker ke roadmap Business Intelligence, soalnya masih lingkup yang sama kan."

**Interpretasi:** Dosen setuju semua sub heading level 2 dari draft proposal lama (Sumber Data, ETL, Analisis Rasio, Dashboard, Deployment) **dimerge ke dalam fase BI Roadmap** — bukan jadi section terpisah.

### Status Lo
✅ Lo udah benar — restruktur ke 6 fase sudah jalan
❌ Tapi ada bug copy-paste yang harus diperbaiki

---

## 2. ISSUE LIST (Prioritas Tinggi → Rendah)

| # | Issue | Lokasi | Severity |
|---|-------|--------|----------|
| 1 | **3 paragraf duplikat persis** di subbab Design | 3.1.4 Design | 🔴 KRITIS |
| 2 | Paragraf pertama Design redundan dengan paragraf ke-2 | 3.1.4 Design | 🟠 Tinggi |
| 3 | Typo italic broken: `*Business Anal**ysis*` | 3.1.3 heading | 🟡 Sedang |
| 4 | Tabel 3.1 masih placeholder `*[...]*` | 3.1.3 Business Analysis | 🟠 Tinggi |
| 5 | Gambar 3.2, 3.3, 3.4 masih placeholder | 3.1.5 & 3.1.4 | 🟠 Tinggi |
| 6 | Inkonsistensi rumus rasio (sebelumnya `mhs/dosen`, sekarang `mhs/dosen_penghitung_rasio`) | seluruh draft | 🟡 Sedang |

---

## 3. STRUKTUR FINAL YANG BENAR (Target)

```
BAB III METODOLOGI PENELITIAN
└── 3.1 Tahapan Penelitian
    ├── [Paragraf intro + Gambar 3.1: Diagram 6 fase BI Roadmap]
    ├── 3.1.1 Justification
    │   └── Identifikasi masalah, penetapan indikator rasio
    ├── 3.1.2 Planning
    │   ├── Sumber data PDDikti  ← ⬅ DARI sub heading 2 lama (Sumber Data)
    │   ├── Variabel & periode 5 semester
    │   └── Cetak biru arsitektur (ETL + DW + dashboard)
    ├── 3.1.3 Business Analysis
    │   ├── Kebutuhan informasi (4 poin)
    │   ├── Rumus rasio  ← ⬅ DARI sub heading 2 lama (Analisis Rasio)
    │   ├── Tabel 3.1 Contoh perhitungan rasio
    │   └── Kebutuhan visualisasi
    ├── 3.1.4 Design
    │   ├── Rancangan star schema (1 fact + 3 dim)
    │   ├── Penjelasan tabel fakta + grain
    │   ├── Penjelasan dimensi
    │   └── Gambar 3.4 Rancangan Star Schema  ← ⬅ DARI sub heading 2 lama (Perancangan Dashboard)
    ├── 3.1.5 Construction
    │   ├── Implementasi ETL (Extract, Transform, Load)
    │   ├── Gambar 3.2 Alur Proses ETL  ← ⬅ DARI sub heading 2 lama (Proses ETL)
    │   └── Gambar 3.3 Arsitektur BI
    └── 3.1.6 Deployment
        ├── Integrasi DW ↔ dashboard
        └── Validasi konsistensi  ← ⬅ DARI sub heading 2 lama (Deployment)
```

---

## 4. INSTRUKSI EDIT — PARAGRAF DEMI PARAGRAF

### 🔴 FIX #1: HAPUS DUPLIKASI DI SUBBAB 3.1.4 DESIGN

**Lo punya 3 paragraf yang diulang 2x persis.** Hapus pengulangan. Hasilnya harus **3 paragraf saja**, bukan 6.

#### A. PARAGRAF YANG HARUS DIHAPUS (2x diulang)

Cari blok ini di `.docx` — muncul **DUA KALI** berturut-turut, hapus yang ke-2:

```
Fase Design bertujuan untuk merancang model data dan arsitektur sistem
Business Intelligence berdasarkan spesifikasi kebutuhan informasi yang telah
ditetapkan pada fase Business Analysis (Moss & Atre, 2003). Perancangan model
data menggunakan pendekatan star schema sebagai struktur utama data warehouse
untuk mendukung analisis kapasitas akademik secara multidimensi. Model
terdiri atas satu tabel fakta (FACT_RASIO_KAPASITAS) dan tiga tabel dimensi
(DIM_WAKTU, DIM_UNIVERSITAS, dan DIM_PROGRAM_STUDI). Struktur ini memisahkan
data numerik dan atribut deskriptif sehingga mendukung proses agregasi yang
efisien (MZ dkk., 2022).
```

```
Tabel FACT_RASIO_KAPASITAS menyimpan jumlah mahasiswa, jumlah dosen, dan rasio
dosen terhadap mahasiswa. Grain data ditetapkan pada tingkat program studi per
periode pelaporan, sehingga setiap baris merepresentasikan kondisi kapasitas
akademik pada satu periode tertentu. Penetapan grain ini penting untuk
menjaga konsistensi agregasi dalam perancangan data warehouse (Moss & Atre,
2003). Nilai rasio disimpan sebagai atribut terhitung pada tabel fakta setelah
proses ETL untuk menjaga konsistensi perhitungan dan memastikan dashboard
menampilkan nilai yang telah tervalidasi tanpa perhitungan ulang (Sinlae dkk.,
2024).
```

```
DIM_WAKTU mendukung analisis longitudinal berdasarkan periode pelaporan,
DIM_PROGRAM_STUDI memungkinkan perbandingan antar program studi, dan
DIM_UNIVERSITAS dipertahankan untuk menjaga fleksibilitas pengembangan sistem
ke institusi lain (Hasan, 2019). Rancangan struktur star schema yang digunakan
dalam penelitian ini ditampilkan pada Gambar 3.4.
```

```
[Gambar 3.4 Rancangan Star Schema]

Gambar 3.4 menunjukkan tabel fakta FACT_RASIO_KAPASITAS yang terhubung dengan
DIM_WAKTU, DIM_UNIVERSITAS, dan DIM_PROGRAM_STUDI. Struktur ini mendukung
analisis tren jumlah mahasiswa, jumlah dosen, dan rasio secara longitudinal
maupun komparatif dalam lingkup institusi (Mellyka & Widagdo, 2025).
```

→ **AKSI:** Cari occurrence ke-2 dari blok ini di subbab Design, lalu DELETE seluruh blok yang duplikat (4 paragraf + 1 placeholder gambar).

---

### 🟠 FIX #2: GANTI ISI SUBBAB 3.1.4 DESIGN (FINAL VERSION)

Setelah duplikasi dihapus, **ganti seluruh isi subbab 3.1.4 Design** dengan versi final ini (lebih bersih, no redundancy):

```
3.1.4 Design

Fase Design bertujuan untuk merancang model data dan arsitektur sistem
Business Intelligence berdasarkan spesifikasi kebutuhan informasi yang telah
ditetapkan pada fase Business Analysis (Moss & Atre, 2003). Perancangan
dilakukan dengan pendekatan star schema sebagai struktur utama data warehouse
untuk mendukung analisis kapasitas akademik secara multidimensi (MZ dkk., 2022).

Model data terdiri atas satu tabel fakta (FACT_RASIO_KAPASITAS) dan tiga
tabel dimensi (DIM_WAKTU, DIM_UNIVERSITAS, dan DIM_PROGRAM_STUDI). Tabel
fakta menyimpan jumlah mahasiswa, jumlah dosen, dan rasio dosen terhadap
mahasiswa, dengan grain ditetapkan pada tingkat program studi per periode
pelaporan. Penetapan grain ini menjaga konsistensi agregasi dalam perancangan
data warehouse (Moss & Atre, 2003). Nilai rasio disimpan sebagai atribut
terhitung pada tabel fakta setelah proses ETL agar dashboard menampilkan
nilai yang telah tervalidasi tanpa perhitungan ulang (Sinlae dkk., 2024).

DIM_WAKTU mendukung analisis longitudinal berdasarkan periode pelaporan,
DIM_PROGRAM_STUDI memungkinkan perbandingan antar program studi, dan
DIM_UNIVERSITAS dipertahankan untuk menjaga fleksibilitas pengembangan sistem
ke institusi lain (Hasan, 2019). Rancangan struktur star schema yang
digunakan dalam penelitian ini ditampilkan pada Gambar 3.4.

[Gambar 3.4 Rancangan Star Schema]

Gambar 3.4 menunjukkan tabel fakta FACT_RASIO_KAPASITAS yang terhubung
dengan DIM_WAKTU, DIM_UNIVERSITAS, dan DIM_PROGRAM_STUDI. Struktur ini
mendukung analisis tren jumlah mahasiswa, jumlah dosen, dan rasio secara
longitudinal maupun komparatif dalam lingkup institusi (Mellyka & Widagdo, 2025).
```

> **Yang berubah:**
> - Paragraf 1 dan 2 lama (yang redundan) → digabung jadi 1 paragraf intro yang clean
> - Total: 3 paragraf isi + 1 gambar + 1 caption (sebelumnya 7 paragraf karena duplikasi)

---

### 🟡 FIX #3: TYPO ITALIC DI HEADING 3.1.3

Cari heading subbab 3.1.3:

❌ **Sekarang (broken):**
```
### *Business Anal**ysis*
```
*(italic terbuka tapi double-asterisk di tengah memutus formatting)*

✅ **Ganti jadi:**
```
### 3.1.3 Business Analysis
```

> Heading subbab di docx **tidak perlu italic**. Italic hanya untuk istilah asing **dalam body text**, bukan di heading. Cek Panduan TA: heading sub-bab pakai bold + kapital awal kata.

---

### 🟠 FIX #4: TABEL 3.1 — REPLACE PLACEHOLDER

Cari di subbab 3.1.3 Business Analysis:
```
*[Tabel 3.1 Contoh Perhitungan Rasio Dosen terhadap Mahasiswa]*
```

Ganti jadi tabel real:

**Tabel 3.1 Contoh Perhitungan Rasio Dosen terhadap Mahasiswa**

| Periode Pelaporan | Jumlah Mahasiswa | Jumlah Dosen Penghitung Rasio | Rasio (Mahasiswa/Dosen) |
|---|---|---|---|
| Genap 2022/2023 | 12.450 | 520 | 23,94 |
| Ganjil 2023/2024 | 12.870 | 528 | 24,38 |
| Genap 2023/2024 | 13.120 | 538 | 24,39 |
| Ganjil 2024/2025 | 13.560 | 545 | 24,88 |
| Genap 2024/2025 | 13.980 | 552 | 25,32 |

> **Catatan:** Angka di atas adalah **contoh ilustrasi**, BUKAN data real. Lo wajib ganti dengan data agregat PDDikti aktual setelah ETL jalan. Kalau belum punya data riil, beri label `(ilustrasi)` di caption.

> **Format Panduan TA Unsil:**
> - Caption tabel **DI ATAS** tabel, center, tanpa titik akhir
> - Format: `Tabel 3.1 Contoh Perhitungan Rasio Dosen terhadap Mahasiswa`
> - Font tabel: TNR 12pt (boleh 10pt kalau muat)
> - Spasi 1 atau 1.5

---

### 🟠 FIX #5: GAMBAR — REPLACE PLACEHOLDER

#### Gambar 3.2 Alur Proses ETL
Lokasi: subbab 3.1.5 Construction

❌ Sekarang: `*[Gambar 3.2 Alur Proses Extract, Transform, Load (ETL)]*`

✅ Insert gambar real (PNG dari `output/figures/etl_flow.png` setelah lo bikin di Claude Code), caption di bawah:
```
Gambar 3.2 Alur Proses Extract, Transform, Load (ETL)
```

#### Gambar 3.3 Arsitektur Business Intelligence
Lokasi: subbab 3.1.5 Construction

❌ Sekarang: `*[Gambar 3.3 Arsitektur Business Intelligence]*`

✅ Insert gambar real (di draft proposal udah ada flowchart vertikal dari PDDIKTI Website → Web Scraping → Raw Dataset → Data Cleaning & Transformation → Data Warehouse → Star Schema → BI Dashboard → DSS). **Pakai gambar yang sama** dari draft proposal sebelumnya, copy-paste.
```
Gambar 3.3 Arsitektur Business Intelligence
```

#### Gambar 3.4 Rancangan Star Schema
Lokasi: subbab 3.1.4 Design

❌ Sekarang: `*[Gambar 3.4 Rancangan Star Schema]*`

✅ Insert ER diagram star schema (di draft proposal udah ada — copy-paste dari PDF lama):
```
Gambar 3.4 Rancangan Star Schema
```

> **Format Panduan TA Unsil:**
> - Caption gambar **DI BAWAH** gambar, center, tanpa titik akhir
> - Format: `Gambar 3.2 Nama Gambar`

---

### 🟡 FIX #6: KONSISTENSI RUMUS RASIO

Di seluruh draft, pastikan rumus rasio konsisten pakai **`Jumlah Dosen Penghitung Rasio`**, bukan `Jumlah Dosen Tetap`. Ini penting karena:

- PDDikti pakai istilah resmi "dosen penghitung rasio"
- Di subbab 3.1.2 Planning lo udah sebut "jumlah dosen penghitung rasio" sebagai variabel
- Tapi di subbab 3.1.3 rumus masih: `Rasio = Jumlah Mahasiswa Aktif / Jumlah Dosen Penghitung Rasio` ← sudah benar
- Tapi di Tabel 3.1 placeholder lama (proposal) pakai "Jumlah Dosen" ← **sesuaikan jadi "Jumlah Dosen Penghitung Rasio"**

Cek juga di BAB I (rumusan masalah, batasan, tujuan) — kalau ada inkonsistensi, sesuaikan.

---

## 5. CATATAN DOSEN LAIN YANG PERLU DI-ADDRESS

Selain BAB III, dosen kasih banyak revisi lain. **Ini bukan fokus revisi BAB III, tapi catat untuk revisi terpisah:**

### Dari Pak Asep / Pak Irfan (foto kertas hijau)

| # | Catatan | Lokasi Target |
|---|---------|---------------|
| 1 | Pendekatan-nya pakai BI / BI Roadmap? | Konsistensi bahasa di abstrak + BAB I |
| 2 | Apa bedanya BI dan BI Roadmap? | BAB II Landasan Teori |
| 3 | "Gak ada pendekatan BI Roadmap" — sebut "metodenya BI aja, baru langkah-langkah BI Roadmap" supaya tidak ambigu | BAB I & III |
| 6 | Buat aplikasi? | Klarifikasi scope |
| 7 | Di laporan tercantum "implementasi sistem", berarti sebelum implementasi kamu udah membuat dong? Berbasis data warehouse | BAB III Construction & Deployment |
| 8 | Diperjelas lagi arahnya seperti apa | BAB I Latar Belakang |
| 9 | Angka Romawi kiri dihilangkan | Format penomoran daftar isi |
| 10 | Latar belakang awal-awal harus memunculkan permasalahan, sebelum itu kita harus mengetahui dulu gambaran umumnya seperti apa, baru mengerucut kondisinya, bahkan di laporan ada laporan penelitian terkait, baru permasalahan Business Intelligence | **BAB I Latar Belakang — restructuring** |
| 11 | Belum permasalahan kurang menangkap kata dosen, masalahnya itu penyajian data masih bersifat statis dan deskriptif, tapi di rumusan masalah tidak ada | **BAB I Rumusan Masalah** |
| 12 | Perbaiki struktur penulisan latar belakang sampai menghasilkan rumusan masalah, tujuan masalah | BAB I |
| 13 | Di batasan masalah, nomor 2 dan 5 itu sama, bisa digabung. Kata 1 [tidak terbaca] | BAB I Batasan Masalah |
| 14 | Nomor 6 dan 7 juga sama, sudah terjawab di nomor 5, karena di nomor 5 sudah dibatasi. Bisa dipersingkat lagi | BAB I Batasan Masalah |
| 15 | Au tdny diandaikan aja sub heading 2, jadi masuker ke roadmap BI ✅ | **BAB III — sudah dilakukan** |

### Dari Sidang Proposal (foto kertas biru)

**Pertanyaan dosen yang perlu siap dijawab di seminar hasil:**
1. Data agregat? → "data yang telah dikelompokkan dan diringkas pada tingkat institusi"
2. Business Intelligence — *Revisian / Konfirmasi*
3. **Pa Irfan:**
   - Atributnya apa aja?
   - Pertimbangannya apa?
   - Kenapa pendekatan Business Intelligence?
   - Output berbentuk apa?
   - Kamu di dalam laporan menggunakan Decision Support System, nah untuk DSS-nya itu kamu seperti apa? Di judul gak ada DSS, nah DSS-nya seperti apa dan dashboardnya?
4. Itu ada sosialisasi tidak ke Unsilnya?
5. Hasilnya dari dashboardnya bisa diberikan manfaat / diberi ke pihak Unsilnya?
6. Gimana sih kebermanfaatannya?
7. **Tambahan:** Data agregatnya nanti berbentuk apa?

---

## 6. WORKFLOW DI CLAUDE CODE

### Step 1: Buka draft di Claude Code
```bash
cd "D:\College\Semester-an\SEMESTER 8\Skripsi"
# pastikan file Draft_Laporan_Ujian_Seminar_Hasil_Fauzi_Noorsyabani_227007042.docx ada
```

### Step 2: Minta Claude Code apply revisi BAB III
Prompt yang bisa lo pakai:
```
Baca CLAUDE.md dan revisi_bab3.md.
Apply semua FIX di revisi_bab3.md ke file Draft_Laporan_Ujian_Seminar_Hasil_Fauzi_Noorsyabani_227007042.docx.

Prioritas:
1. Hapus duplikasi di subbab 3.1.4 Design (FIX #1)
2. Ganti subbab 3.1.4 dengan versi final (FIX #2)
3. Fix typo italic heading 3.1.3 (FIX #3)
4. Replace placeholder Tabel 3.1 dengan tabel real (FIX #4)
5. Insert 3 gambar (3.2, 3.3, 3.4) — pakai gambar dari draft proposal sebagai sumber (FIX #5)
6. Sesuaikan rumus rasio jadi konsisten (FIX #6)

Save sebagai file baru: Draft_Laporan_Ujian_Seminar_Hasil_Fauzi_Noorsyabani_227007042_REV1.docx

Jangan timpa file asli — bikin file baru biar bisa di-rollback.
```

### Step 3: Verifikasi
- Open file REV1 di Word
- Cek subbab 3.1.4 cuma 3 paragraf isi (bukan 6)
- Cek heading 3.1.3 italic-nya bener
- Cek Tabel 3.1 udah terisi
- Cek gambar 3.2, 3.3, 3.4 sudah ada

### Step 4: Lanjut revisi BAB I (catatan dosen poin 1-14)
Kalau BAB III udah aman, baru pindah revisi BAB I (latar belakang struktur baru, rumusan masalah, batasan masalah).

---

## 7. CHECKLIST REVISI BAB III

- [ ] FIX #1: Duplikasi 3 paragraf di Design dihapus
- [ ] FIX #2: Subbab 3.1.4 Design pakai versi final (3 paragraf isi + gambar)
- [ ] FIX #3: Heading 3.1.3 typo italic diperbaiki
- [ ] FIX #4: Tabel 3.1 terisi (dengan data ilustrasi atau real)
- [ ] FIX #5: Gambar 3.2, 3.3, 3.4 ter-insert (bukan placeholder lagi)
- [ ] FIX #6: Rumus rasio konsisten "Jumlah Dosen Penghitung Rasio"
- [ ] Cek format: TNR 12pt, spasi 2.0, justify, margin 4-3-3-4
- [ ] Cek caption tabel di atas, caption gambar di bawah
- [ ] Cek penomoran konsisten (3.1.1 - 3.1.6)
- [ ] Save sebagai _REV1.docx

---

*File ini untuk dibaca Claude Code sebelum apply revisi. Jangan dihapus sampai BAB III final.*
