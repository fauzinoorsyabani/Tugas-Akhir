# BAB III METODOLOGI PENELITIAN

## III.1 Jenis dan Pendekatan Penelitian

Penelitian ini menggunakan jenis penelitian deskriptif kuantitatif dengan pendekatan _Business Intelligence_ (BI) sebagai pendukung _Decision Support System_ (DSS). Penelitian deskriptif kuantitatif bertujuan untuk menggambarkan kondisi data secara objektif berdasarkan data numerik yang tersedia tanpa melakukan pengujian hipotesis maupun analisis prediktif.

Pendekatan _Business Intelligence_ digunakan untuk mengolah, menganalisis, dan menyajikan data agregat institusi pendidikan tinggi dalam bentuk informasi yang terstruktur dan mudah dipahami. Kerangka kerja yang digunakan dalam pengembangan _Business Intelligence_ pada penelitian ini adalah **Business Intelligence Roadmap** yang dikemukakan oleh Moss & Atre (2003). Informasi yang dihasilkan melalui _Business Intelligence_ selanjutnya dimanfaatkan sebagai komponen pendukung dalam _Decision Support System_ (DSS) untuk membantu pengambilan keputusan berbasis data pada tingkat institusi.

Dalam penelitian ini, DSS diposisikan sebagai kerangka konseptual yang memanfaatkan hasil analisis dan visualisasi BI. Dengan demikian, DSS berperan sebagai pendukung interpretasi data kapasitas akademik tanpa menggantikan peran pengambil keputusan institusional.

## III.2 Objek Penelitian

Objek penelitian dalam penelitian ini adalah Perguruan Tinggi Negeri berstatus Badan Layanan Umum (PTN BLU), dengan studi kasus pada Universitas Siliwangi. Pemilihan ini didasarkan pada karakteristik kebijakan layanan yang relatif homogen serta peran strategis PTN BLU dalam penyelenggaraan pendidikan tinggi negeri.

Unit analisis dalam penelitian ini dilakukan pada tingkat institusi secara agregat (bukan pada level individu mahasiswa dan dosen) untuk memperoleh gambaran utuh kinerja dan kapasitas layanan institusi.

## III.3 Variabel Penelitian

Variabel penelitian digunakan untuk membatasi ruang lingkup analisis agar tetap terfokus. Variabel kuantitatif yang dikaji meliputi:

1. **Jumlah Mahasiswa**, yaitu total mahasiswa aktif pada tingkat institusi.
2. **Jumlah Dosen**, yaitu total dosen aktif yang tercatat pada tingkat institusi.
3. **Rasio Dosen terhadap Mahasiswa**, yaitu perbandingan antara total beban mengajar (jumlah dosen) dengan peserta didik (jumlah mahasiswa) pada tingkat institusi.

Ketiga variabel tersebut merupakan indikator utama dalam mengukur keseimbangan kapasitas akademik dan layanan pendidikan tinggi secara agregat.

## III.4 Sumber dan Teknik Pengumpulan Data

Data yang digunakan merupakan data sekunder yang dikumpulkan dari Pangkalan Data Pendidikan Tinggi (PDDikti). PDDikti menyediakan data populasi institusional secara nasional, legal, dan memadai sebagai basis _Business Intelligence_.

Teknik pengumpulan data menggunakan metode web scraping untuk mengekstraksi data populasi dari layanan PDDikti. Scraping dilakukan terhadap profil institusi dan rekapitulasi jumlah mahasiswa serta dosen, untuk kemudian dikonversi menjadi dataset terstruktur dan siap olah.

## III.5 Kerangka Metodologi Business Intelligence Roadmap (Moss & Atre)

Penelitian ini menggunakan kerangka kerja _Business Intelligence Roadmap_ yang dikembangkan oleh Larissa T. Moss dan Shaku Atre (2003). Pendekatan ini dipilih karena memberikan panduan siklus hidup (_lifecycle_) yang terstruktur dan sistematis pada tahapan pengembangan BI. Tahapan yang disesuaikan dengan konteks penelitian ini meliputi 6 tahapan utama:

1. **Justification (Justifikasi)**
   Pada tahap ini, dilakukan penilaian kasus bisnis (_business case assessment_), yaitu mengidentifikasi masalah keterbatasan penyajian data statis PDDikti serta justifikasi kebutuhan visualisasi rasio kapasitas akademik sebagai pendukung _Decision Support System_ tingkat rektorat.
2. **Planning (Perencanaan)**
   Berfokus pada evaluasi arsitektur perangkat lunak untuk ekstraksi data serta penyusunan alur perolehan data PDDikti untuk pemrosesan berbasis Python.
3. **Business Analysis (Analisis Bisnis)**
   Tahap ini berfokus pada pendefinisian kebutuhan informasi kapasitas akademik. Proses yang terkait meliputi definisi data agregat institusi (mahasiswa, dosen, dan rasio) serta studi kelayakan metrik yang relevan.
4. **Design (Perancangan)**
   - **Desain Basis Data**: Perancangan struktur penyajian data repositori tabel dimensi dan fakta (_data mart/star schema_).
   - **Desain ETL (_Extract, Transform, Load_)**: Penentuan mekanisme penarikan raw data, pembersihan, standarisasi agregat, serta pengunggahan ke repositori analisis.
5. **Construction (Konstruksi)**
   Tahap ini merupakan pengerjaan teknis pengembangan dari desain yang telah dibuat, yang meliputi:
   - **Pengembangan ETL**: Mengimplementasikan kode _Python_ dan _Pandas_ untuk mengekstrak dan membersihkan data PDDikti (menangani atribut data nol, inkonsistensi nama program studi, dll.).
   - **Pengembangan Aplikasi/Dashboard**: Pembuatan antarmuka visualisasi _Dashboard BI_ (misal dengan Tableau/Power BI/Metabase) berdasarkan data agregat rasio.
6. **Deployment (Implementasi/Penyebaran)**
   Tahap di mana _Dashboard Business Intelligence_ kapasitas akademik dieksekusi dan diuji, kemudian hasil visualisasinya dievaluasi sebagai bentuk penyokong laporan manajerial atau Decision Support System bagi institusi PTN BLU (Universitas Siliwangi).

## III.6 Proses Ekstraksi dan Transformasi Data (ETL)

Sesuai tahap konstruksi pada _BI Roadmap_, data mentah diproses melalui tahapan _Extract, Transform, dan Load_ (ETL).

- Ekstraksi dilakukan secara terprogram menggunakan otomatisasi web (seperi pustaka Selenium atau pemanggilan API).
- Transformasi mengutamakan _data cleaning_ dan penyesuaian atribut data seperti agregasi di tingkat fakultas dan universitas.
- Load dilaksanakan dengan pembentukan ekstensi tabular (CSV/Database) yang mendukung query instan bagi pembentukan dashboard grafis.

## III.7 Operasionalisasi Variabel dan Perhitungan Rasio

Dalam _Business Intelligence Roadmap_, aturan perhitungan rasio diimplementasikan pada lapis presentasi BI. Rasio dosen terhadap mahasiswa digunakan sebagai _Key Performance Indicator_ (KPI).

$$ Rasio = \frac{Total Mahasiswa Aktif}{Total Dosen} $$

Nilai rasio tersebut akan divisualisasikan menggunakan batas rentang acuan:

- **Rasio ≤ 30** (Relatif Seimbang): Kapasitas pengajaran dosen masih aman.
- **Rasio > 30** (Perlu Perhatian): Beban dosen meningkat dan butuh strategi tata kelola SDM akademik yang lebih cermat.

## III.8 Desain Dashboard Business Intelligence

Integrasi akhir dari _BI Roadmap_ (tahap penyebaran infrastruktur kognitif) tertuang dalam wujud _Dashboard BI_. Dashboard menyajikan beberapa panel interaktif: panel tren jumlah mahasiswa, histogram ketersediaan dosen, serta proporsi rasio aktual per fakultas maupun universitas, yang semuanya dilabeli indikator warna untuk memfasilitasi pengambilan keputusan strategis tingkat eksekutif secara intuitif.
