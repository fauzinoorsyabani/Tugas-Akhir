# BAB III METODOLOGI PENELITIAN

Pelaksanaan penelitian ini disusun berdasarkan tahapan-tahapan sistematis agar pengolahan data rasio kapasitas akademik menghasilkan informasi yang relevan dan terukur bagi pengambil keputusan di lingkungan Perguruan Tinggi Negeri Badan Layanan Umum (PTN BLU). Kerangka pemecahan masalah yang digunakan mengadopsi model **Business Intelligence Roadmap** yang dikemukakan oleh Moss & Atre (2003).

Metodologi ini dipilih karena pendekatannya yang berfokus pada integrasi data dari berbagai sumber serta berorientasi pada penyajian _dashboard_ analitik untuk pihak manajemen (eksekutif). Tahapan penelitian dijabarkan ke dalam enam langkah utama kerangka operasional _Business Intelligence Roadmap_ (Moss & Atre, 2003; Stewart & Dewan, 2022) sebagai berikut:

## III.1 Tahapan Penelitian (Business Intelligence Roadmap)

---

> **[TANDAI - TEMPATKAN GAMBAR DI SINI]**
> _Silakan masukkan_ **[Gambar Bagan Siklus Business Intelligence Roadmap (6 Tahapan)]** _dari jurnal rujukan Anda atau dari buku (Moss & Atre, 2003)._

---

**1. Tahap Justifikasi (Justification)**
Tahap awal penelitian dilakukan melalui penilaian kasus (_Business Case Assessment_). Pada tahap ini, diidentifikasi urgensi penyajian data agregat institusional yang selama ini disajikan secara statis dalam Pangkalan Data Pendidikan Tinggi (PDDikti) (Murti & Mulyani, 2022). Justifikasi dilakukan untuk memproposalkan rancangan visualisasi _Business Intelligence_ berupa indikator Rasio Dosen dan Mahasiswa sebagai penyokong fungsional dari _Decision Support System_ (DSS) untuk manajemen PTN BLU (Universitas Siliwangi).

**2. Tahap Perencanaan (Planning)**
Tahapan ini berfokus pada rekayasa _Enterprise Infrastructure Evaluation_ untuk menilai kebutuhan sistem dan infrastruktur. Peneliti merencanakan alat serta perangkat lunak pendukung ekstraksi data:

- Bahasa pemrograman _Python_ dan _library_ otomatisasi (_Selenium/Requests_) untuk ekstraksi pangkalan data.
- Area persiapan data (_staging_) menggunakan format _Comma-Separated Values_ (CSV).
- Platform pelaporan (visualisasi) seperti _Tableau, Microsoft Power BI,_ atau modul web visual yang akan digunakan (Santhi dkk., 2021).

**3. Tahap Analisis Bisnis (Business Analysis)**
Melakukan analisis kebutuhan proyek (_Project Planning_) untuk menetapkan batasan analisis dan sumber informasi.

- **Sumber Data:** Data populasi dari laman terpusat PDDikti (Astuti dkk., 2024).
- **Definisi Variabel Utama:** "Jumlah Mahasiswa Aktif", "Jumlah Dosen yang Ditugaskan", dan metrik turunannya yaitu "Rasio Dosen terhadap Mahasiswa".
- **Pendefinisian Standar:** Penyelarasan ambang batas nilai rasio disesuaikan dengan Standar Nasional Pendidikan Tinggi (SN-Dikti) dan Badan Akreditasi Nasional Perguruan Tinggi (BAN-PT) terkait Beban Kerja Dosen (BKD).

---

> **[TANDAI - TEMPATKAN TABEL DI SINI]**
> _Silakan masukkan_ **[Tabel Operasionalisasi / Definisi Variabel Penelitian]** _yang menjelaskan Jumlah Dosen, Jumlah Mahasiswa, dan Rumus Rasio diukur menggunakan skala apa._

---

**4. Tahap Perancangan (Design)**
Menerjemahkan analisis ke dalam spesifikasi teknis arsitektur pangkalan data.

- **Perancangan Repositori (_Data Mart_):** Membuat desain _Star Schema_ konseptual yang memetakan _Fact Table_ (tabel berisi total mahasiswa, total dosen, hasil perbandingan rasio) pusat serta _Dimension Tables_ (seperti rincian per prodi, fakultas, atau rentang waktu semester) (Rahim dkk., 2025).
- **Perancangan ETL (_Extract, Transform, Load_):** Mendesain aliran penarikan raw data (_extract_), aturan pembersihan/filter (membuang tabel gosong/duplikat dan standardisasi nama fakultas) (_transform_), dan penyimpanan ulang dataset bersih ke tabel master siap pakai (_load_).

**5. Tahap Konstruksi (Construction)**
Fase perakitan pengolahan (_coding_) maupun pembuatan sistem:

- **Konstruksi ETL:** Mengeksekusi penarikan data PDDikti dan menjalankan perhitungan konversi rumus Rasio Dosen dan Mahasiswa menggunakan otomasi skrip.  
  Formulasi matematis rasio dihitung menggunakan patokan rasio ekuivalensi (Gaftandzhieva dkk., 2023):
  $$ Rasio_Kapasitas = \frac{Total\,Mahasiswa\,Aktif\,Tertulis}{Total\,Dosen\,Penugasan\,Terdaftar} $$
- **Pengembangan Dashboard (Aplikasi):** Menyusun modul visualisasi (grafik tren, _bar chart_ klasifikasi fakultas, _gauge/indicator chart_ tingkat wajar/waspada) (Sharma & Joshi, 2022). Indikator rasio memancarkan zona aman (hijau) jika **≤ 30**, wajar bersyarat untuk humaniora jika **≤ 45**, dan kondisi gawat/waspada darurat penambahan dosen (merah) untuk lonjakan rasio di angka ekstrem **> 60** (UU Dosen/BAN-PT).

**6. Tahap Implementasi / Penyebaran (Deployment)**
Tahap ini merupakan pengerahan instrumen terakhir (_Release_). _Dashboard Business Intelligence_ dipresentasikan secara visual sebagai _Output_ kepada pengguna (_user/manajemen_). Pada titik ini, dilakukan penelaahan evaluasi apakah penyajian kapasitas mutu pendidikan tinggi tersebut layak menjadi alat bantu indikasi empiris (_Decision Support System_) rujukan pimpinan Universitas Siliwangi (Mellyka dkk., 2025).

---

> **[TANDAI - TEMPATKAN GAMBAR DI SINI]**
> _Di sini tempatkan_ **[Gambar Alur Proses / Flowchart]** _sistem kerja dari mulai penarikan data hingga tampil ke Dashboard, yang dirancang oleh Anda sendiri._

---
