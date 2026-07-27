# Naskah Lengkap & Detail Revisi Bab IV dan Bab V (Ekspansi 6 Langkah BI Roadmap)

Dokumen ini menyajikan **naskah akademis yang sangat komprehensif, panjang, dan mendalam** untuk **Bab IV** dan **Bab V**. Setiap sub-sub-bab (4.1.1 hingga 4.6.3) telah diekspansi menjadi beberapa paragraf analitis yang kaya akan teori, latar belakang teknis, regulasi nasional, serta tidak mengurangi sedikit pun data dan hasil eksperimen yang sudah ada sebelumnya.

---

## BAB IV HASIL DAN PEMBAHASAN

Penelitian ini mengimplementasikan sistem *Business Intelligence* (BI) berbasis *Data Warehouse* untuk menganalisis kapasitas akademik di Universitas Siliwangi. Pembahasan pada bab ini distrukturkan secara sistematis mengikuti enam fase sekuensial dari metodologi *Business Intelligence Roadmap* (Moss dan Atre, 2003), yaitu *Justification, Planning, Business Analysis, Design, Construction,* dan *Deployment*.

---

### 4.1 Fase *Justification* (Evaluasi Kebutuhan Bisnis)

Fase *Justification* merupakan tahap awal untuk menilai kelayakan dan memberikan dasar pembenaran yang kuat mengenai perlunya pembangunan sistem *Business Intelligence* di lingkungan Universitas Siliwangi.

#### 4.1.1 Evaluasi Kebutuhan Pemantauan Kapasitas Akademik
Proses tata kelola dan pemantauan kapasitas akademik di perguruan tinggi, khususnya terkait keseimbangan rasio dosen terhadap mahasiswa, merupakan salah satu indikator vital dalam menjaga mutu penyelenggaraan pendidikan. Di Universitas Siliwangi, pemantauan data akademik selama ini masih menghadapai kendala berupa format pelaporan yang bersifat statis, tersebar di berbagai unit, serta memerlukan waktu yang relatif lama untuk diolah menjadi informasi yang siap pakai. 

Keterlambatan dalam mengidentifikasi ketimpangan beban mengajar dosen dapat berdampak langsung pada penurunan kualitas proses pembelajaran serta berpotensi menimbulkan kendala dalam proses akreditasi program studi. Oleh karena itu, dibutuhkan sebuah mekanisme pemantauan yang mampu menyajikan data secara terintegrasi, visual, dan dinamis, sehingga potensi masalah seperti penumpukan beban mahasiswa pada program studi tertentu dapat dideteksi sejak dini (*Early Warning System*).

#### 4.1.2 Justifikasi Kelayakan Sistem Business Intelligence
Penerapan *Business Intelligence* (BI) berbasis *Data Warehouse* dijustifikasi sebagai solusi yang paling tepat untuk menjawab kebutuhan pemantauan tersebut. Berbeda dengan sistem pemrosesan transaksi tradisional (*Online Transaction Processing* / OLTP) yang dirancang untuk mendukung operasional harian, sistem BI berbasis *Data Warehouse* (*Online Analytical Processing* / OLAP) dirancang khusus untuk memfasilitasi analisis data historis dan agregat secara cepat.

Dengan memanfaatkan data historis PDDikti yang diekstraksi dan ditransformasikan ke dalam model *Data Warehouse*, pimpinan universitas maupun pengelola fakultas dapat melakukan analisis longitudinal (antar-periode) dan analisis komparatif (antar-program studi). Pembenaran ini selaras dengan pandangan Moss dan Atre (2003) yang menyatakan bahwa BI memberikan nilai tambah strategis bagi organisasi dengan mengubah data mentah yang terisolasi menjadi wawasan pengetahuan (*insight*) yang mendukung pengambilan keputusan berbasis data faktual (*data-driven decision making*).

---

### 4.2 Fase *Planning* (Perencanaan Infrastruktur)

Fase *Planning* menetapkan perencanaan sumber daya teknis, arsitektur perangkat lunak, dan mekanisme pengelolaan data yang akan digunakan selama siklus pengembangan sistem.

#### 4.2.1 Perencanaan Infrastruktur Komputasi dan Alat Visualisasi
Pada fase perencanaan proyek, infrastruktur perangkat lunak ditetapkan berdasarkan kriteria efisiensi komputasi, fleksibilitas integrasi, serta kemudahan aksesibilitas bagi pengguna akhir. Untuk lingkungan pemrosesan data (*back-end*), dipilih bahasa pemrograman Python 3.x dengan pustaka utama Pandas dan NumPy. Python dipilih karena keandalannya dalam manipulasi struktur data berukuran besar, ketersediaan pustaka transformasi data yang kaya, serta kemudahannya dalam mengimplementasikan *pipeline* ETL (*Extract, Transform, Load*) secara terprogram.

Untuk antarmuka visualisasi (*front-end*), ditetapkan penggunaan Google Looker Studio (sebelumnya dikenal sebagai Google Data Studio). Google Looker Studio dipilih karena merupakan platform analitik berbasis *cloud* yang mampu menyajikan visualisasi interaktif secara *real-time*, mendukung pembuatan filter terparameter (seperti filter Fakultas dan Rumpun Ilmu), serta dapat diakses oleh pemangku kepentingan melalui peramban web tanpa memerlukan instalasi perangkat lunak khusus di sisi pengguna.

#### 4.2.2 Penentuan Sumber Data dan Media Penyimpanan
Sumber data utama yang direncanakan dalam penelitian ini adalah data publik teragregasi yang bersumber dari portal Pangkalan Data Pendidikan Tinggi (PDDikti). Data tersebut mencakup profil program studi, jumlah dosen penghitung rasio, jumlah mahasiswa aktif, serta metadata institusi. 

Arsitektur penyimpanan direncanakan memanfaatkan Google Drive dan Google Sheets sebagai media perantara (*staging area*) dan penyimpanan data terpusat terintegrasi *cloud*. Pemilihan arsitektur ini memastikan bahwa berkas *Data Warehouse* hasil pemrosesan ETL dapat terhubung secara lancar (*seamless integration*) dengan Google Looker Studio tanpa menimbulkan kendala konektivitas *database* lokal.

---

### 4.3 Fase *Business Analysis* (Analisis Kebutuhan Bisnis)

Fase *Business Analysis* bertujuan mendefinisikan secara detail indikator-indikator kunci yang akan diukur serta menetapkan aturan bisnis (*business rules*) yang menjadi tolok ukur evaluasi kapasitas akademik.

#### 4.3.1 Analisis Indikator Kunci (KPI)
Berdasarkan hasil analisis kebutuhan informasi manajemen perguruan tinggi, ditetapkan empat *Key Performance Indicator* (KPI) utama yang menjadi fokus analisis dalam sistem BI ini, yaitu:
1. **Total Mahasiswa Aktif:** Jumlah akumulatif mahasiswa yang terdaftar dan aktif melakukan registrasi pada periode pelaporan tertentu.
2. **Total Dosen Penghitung Rasio:** Jumlah dosen tetap yang memenuhi kualifikasi dan dihitung sebagai beban pengajar utama program studi.
3. **Jumlah Program Studi Aktif:** Cakupan program studi di Universitas Siliwangi yang memiliki aktivitas akademik pada periode pengamatan.
4. **Nilai Rasio Dosen-Mahasiswa:** Indikator utama yang menggambarkan perbandingan kuantitatif antara jumlah mahasiswa dan dosen, yang dihitung menggunakan formulasi matematika sederhana:

$$\text{Nilai Rasio} = \frac{\text{Jumlah Mahasiswa}}{\text{Jumlah Dosen}}$$

#### 4.3.2 Penetapan Ambang Batas Toleransi Rasio
Aturan bisnis terpenting dalam penelitian ini adalah penetapan ambang batas toleransi rasio dosen terhadap mahasiswa. Mengacu pada regulasi nasional yang tertuang dalam Surat Edaran Dirjen Dikti serta pedoman instrumen akreditasi Badan Akreditasi Nasional Perguruan Tinggi (BAN-PT), ditetapkan pemisahan ambang batas kritis berdasarkan karakteristik rumpun keilmuan:
* **Rumpun Ilmu Sains dan Teknologi (Saintek / Eksakta):** Ambang batas toleransi kritis maksimal ditetapkan sebesar **1 : 30**.
* **Rumpun Ilmu Sosial dan Humaniora (Soshum):** Ambang batas toleransi kritis maksimal ditetapkan sebesar **1 : 45**.

Penetapan ambang batas ini difungsikan sebagai logika bisnis pada sistem *Early Warning System*. Program studi yang memiliki nilai rasio melebihi angka toleransi tersebut akan secara otomatis dikategorikan berstatus **"Melebihi Batas"** dan diberi indikator visual warna merah pada dashboard, sebagai sinyal bagi pimpinan universitas untuk melakukan tindakan korektif (seperti penambahan dosen atau pembatasan kuota mahasiswa baru).

---

### 4.4 Fase *Design* (Perancangan Sistem)

Fase *Design* menerjemahkan kebutuhan bisnis dan aturan analitis ke dalam rancangan struktur data logis dan fisik menggunakan pendekatan pemodelan *Data Warehouse*.

#### 4.4.1 Pemilihan Pemodelan Star Schema
Penelitian ini memilih pemodelan *Star Schema* (Skema Bintang) sebagai arsitektur basis data analitis. *Star Schema* merupakan bentuk pemodelan multidimensi yang terdiri atas satu tabel fakta terpusat yang dikelilingi oleh beberapa tabel dimensi yang saling berhubungan secara langsung tanpa hierarki bercabang (*denormalized structure*).

Pemilihan *Star Schema* didasari oleh tiga pertimbangan teknis:
1. **Performa Kueri:** Struktur terdenormalisasi meminimalisir operasi penggabungan tabel (*join*), sehingga eksekusi agregasi data pada dashboard interaktif menjadi jauh lebih cepat.
2. **Kemudahan Pemahaman:** Struktur bintang sangat intuitif dan mudah dipahami oleh pengguna akhir maupun pengembang dalam memetakan hubungan antara metrik bisnis (fakta) dan konteks analisis (dimensi).
3. **Proporsionalitas Skala Data:** Skala data penelitian ini (201 baris rekaman fakta, 35 program studi, dan 5 periode pelaporan) sangat ideal diproses menggunakan *Star Schema* dibandingkan *Snowflake Schema* yang lebih kompleks dan memerlukan redundansi struktur.

#### 4.4.2 Desain Tabel Fakta dan Tabel Dimensi
Rancangan *Star Schema* yang dikembangkan terdiri atas 1 (satu) Tabel Fakta dan 3 (tiga) Tabel Dimensi, dengan rincian struktur sebagai berikut:

1. **Tabel Fakta (`Fact_Kapasitas_Pendidikan`):** 
   Merupakan tabel utama yang menyimpan metrik numerik dan *foreign key* yang menghubungkan ke tabel-tabel dimensi. Kolom utama meliputi: `id_fakta`, `sk_waktu`, `sk_universitas`, `sk_prodi`, `jumlah_mahasiswa`, `jumlah_dosen`, dan `nilai_rasio`.
2. **Tabel Dimensi Waktu (`Dim_Waktu`):** 
   Menyimpan konteks temporal analisis. Kolom meliputi: `sk_waktu`, `tahun_pelaporan`, `semester` (Ganjil/Genap), dan `tahun`.
3. **Tabel Dimensi Universitas (`Dim_Universitas`):** 
   Menyimpan metadata institusi. Kolom meliputi: `sk_universitas`, `kode_pt`, `nama_universitas`, `kota`, dan `provinsi`.
4. **Tabel Dimensi Program Studi (`Dim_Prodi`):** 
   Menyimpan konteks keilmuan dan kelembagaan prodi. Kolom meliputi: `sk_prodi`, `kode_prodi`, `nama_program_studi`, `jenjang`, `akreditasi`, `fakultas`, dan `rumpun_ilmu`.

---

### 4.5 Fase *Construction* (Pembangunan Sistem - ETL)

Fase *Construction* merupakan tahap realisasi teknis melalui pembuatan dan eksekusi skrip pemrosesan data *Extract, Transform, Load* (ETL) menggunakan Python.

#### 4.5.1 Hasil Tahap Extract
Tahap *Extract* bertugas membaca dan mengambil data mentah dari sumber data awal. Dalam penelitian ini, data mentah hasil *scraping* dari portal PDDikti disimpan dalam dua berkas CSV mentah, yaitu `unsil_prodi_fresh.csv` (memuat data program studi) dan `unsil_univ_fresh.csv` (memuat metadata institusi). Skrip Python membaca berkas mentah ini ke dalam struktur *DataFrame* Pandas. Hasil tahap ekstraksi berhasil memuat seluruh rekaman data mentah tanpa adanya kegagalan pembacaan berkas.

#### 4.5.2 Hasil Tahap Transform
Tahap *Transform* merupakan inti dari pemrosesan data, di mana data mentah dibersihkan, distandarisasi, dan diperkaya agar sesuai dengan aturan bisnis. Tahap ini mengeksekusi 6 (enam) langkah transformasi secara berurutan:
1. **Langkah 0 (Scope Filtering):** Menyaring data nasional sehingga hanya menyisakan rekaman data milik Universitas Siliwangi (Kode PT: 002008).
2. **Langkah 1 (Drop Null Kritis):** Menghapus baris yang kehilangan identitas utama (`kode_prodi` atau `tahun_pelaporan`).
3. **Langkah 2 (Parsing Periode):** Memecah kolom `tahun_pelaporan` (misal: "Ganjil 2023") menjadi dua kolom terpisah, yaitu `semester` ("Ganjil") dan `tahun` (2023).
4. **Langkah 3 (Konversi Tipe Data):** Mengubah tipe data numerik dari format objek (string) menjadi numerik (`float64`/`int64`).
5. **Langkah 4 (Parsing dan Kalkulasi Rasio):** Ekstraksi string nilai rasio (misal "1:45.5") menjadi nilai desimal murni (`45.5`).
6. **Langkah 5 (Standarisasi dan Mapping Metadata):** Menambahkan kolom `fakultas` dan `rumpun_ilmu` secara otomatis berdasarkan kamus data (*dictionary mapping*) program studi Universitas Siliwangi.

Hasil akhir transformasi menghasilkan **201 baris rekaman data yang valid**, mencakup 35 program studi aktif selama 5 periode pelaporan (Ganjil 2023 hingga Ganjil 2025).

#### 4.5.3 Hasil Tahap Load
Tahap *Load* bertanggung jawab mendistribusikan data yang telah ditransformasi ke dalam struktur fisik *Data Warehouse*. Skrip Python secara otomatis memecah *DataFrame* hasil transformasi dan mengisikannya ke dalam berkas CSV terpisah yang mewakili tabel-tabel *Star Schema* (`Fact_Kapasitas_Pendidikan.csv`, `Dim_Waktu.csv`, `Dim_Universitas.csv`, `Dim_Prodi.csv`).

Selain itu, untuk memfasilitasi kebutuhan visualisasi di Google Looker Studio yang memerlukan tabel datar terdenormalisasi, tahap *Load* juga menghasilkan satu berkas *flat table* utama bernama `master_looker_unsil.csv` yang berisi 201 baris data komplit beserta seluruh atribut dimensi.

---

### 4.6 Fase *Deployment* (Implementasi dan Validasi)

Fase *Deployment* merupakan tahap penyerahan hasil pengembangan sistem dalam bentuk *dashboard* analitik interaktif serta pelaksanaan validasi untuk menjamin kualitas data.

#### 4.6.1 Hasil Implementasi Dashboard Analitik
*Dashboard Academic Capacity Analytics* dibangun di atas Google Looker Studio dengan menghubungkan berkas `master_looker_unsil.csv` sebagai *data source*. Antarmuka *dashboard* dirancang menjadi 3 (tiga) halaman utama:
1. **Halaman Executive Overview:** Menyajikan ringkasan KPI institusi (Total Mahasiswa, Total Dosen, Rata-rata Rasio, Jumlah Prodi) dalam bentuk *scorecard*, distribusi mahasiswa per jenjang, serta pemetaan rasio institusi.
2. **Halaman Detail Per Program Studi:** Memfasilitasi eksplorasi mendalam untuk melihat performa dan status rasio pada prodi tertentu.
3. **Halaman Tren Longitudinal:** Menyajikan grafik garis pergerakan rasio dosen-mahasiswa secara time-series antar-periode.

Sebagai tindak lanjut revisi, *dashboard* telah dilengkapi dengan **Control Filter interaktif per Fakultas dan per Rumpun Ilmu (Sains/Sosial)** di bagian atas antarmuka, sehingga pengguna dapat menyaring tampilan data sesuai kebutuhan analisis kelembagaan.

#### 4.6.2 Validasi Konsistensi Data
Untuk menjamin integritas data dari sumber awal hingga tampil di *dashboard*, dilakukan validasi berlapis (*Sanity Check*):

1. **Validasi Jumlah Record dan Mahasiswa (Sebelum vs Sesudah ETL):**
   * Total Mahasiswa Kumulatif sebelum ETL (Data Mentah): **101.401 Mahasiswa**
   * Total Mahasiswa Kumulatif sesudah ETL (Data Warehouse): **101.401 Mahasiswa**
   * Hasil menunjukkan **tingkat konsistensi 100% (persentase data berhasil diproses = 100%, data dibuang karena null = 0 baris)**.
2. **Validasi Antar-Semester (Deteksi Anomali):**
   * Evaluasi perbedaan data antara semester Ganjil dan Genap pada tahun ajaran yang sama menunjukkan deviasi yang wajar (< 200 mahasiswa) pada 34 program studi reguler.
   * Ditemukan 1 (satu) anomali deviasi signifikan pada program studi Pendidikan Profesi Guru (PPG) sebesar 624 mahasiswa (Ganjil 2023: 1.327 vs Genap 2023: 703). Berdasarkan analisis, fluktuasi ini dinyatakan **wajar** karena sistem penerimaan PPG memang berbasis gelombang (*batch*), bukan reguler per semester.

#### 4.6.3 Hasil Visualisasi dan Analisis Rumpun Ilmu
Hasil analisis visualisasi pada *dashboard* mengungkap adanya perbedaan (*disparitas*) beban mengajar yang sangat mencolok antara rumpun ilmu Sains (Saintek) dan Sosial (Soshum):

* **Rumpun Ilmu Sains dan Teknologi (Saintek):**
  Seluruh program studi berumpun Saintek (seperti Teknik Informatika, Teknik Sipil, Agroteknologi) menunjukkan nilai rasio yang relatif stabil dan berada **di bawah ambang batas kritis 1 : 30**. Hal ini mengindikasikan bahwa kapasitas dosen pengajar pada bidang eksakta di Universitas Siliwangi berada dalam kondisi cukup seimbang dan memadai.
* **Rumpun Ilmu Sosial dan Humaniora (Soshum):**
  Sebaliknya, beberapa program studi pada rumpun Soshum terdeteksi mengalami kondisi kritis atau **"Melebihi Batas" (rasio > 1 : 45)**. Temuan tertinggi dicatatkan oleh Program Studi **Akuntansi (rasio 1 : 54)** dan **Pendidikan Sejarah (rasio 1 : 53)**. Kondisi ini dipicu oleh pesatnya pertumbuhan jumlah mahasiswa baru yang tidak diimbangi dengan penambahan jumlah dosen tetap secara proporsional.

Temuan analitis ini membuktikan keberhasilan sistem BI dalam berfungsi sebagai *Early Warning System*, memberikan masukan konkret bagi pimpinan universitas untuk memprioritaskan alokasi rekrutmen dosen baru pada program studi berumpun sosial.

---

## BAB V KESIMPULAN DAN SARAN

### 5.1 Kesimpulan

Berdasarkan hasil penelitian dan pembahasan yang telah dipaparkan, dapat ditarik beberapa kesimpulan utama sebagai berikut:

1. Sistem *Business Intelligence* berbasis *Data Warehouse* berhasil dibangun untuk mengolah dan mengintegrasikan data agregat PDDikti terkait kapasitas akademik Universitas Siliwangi. Penerapan pemodelan *Star Schema* yang terdiri atas 1 tabel fakta dan 3 tabel dimensi terbukti optimal dalam menyusun data terstruktur serta mempercepat eksekusi kueri analitis.
2. Pendekatan metodologi *Business Intelligence Roadmap* (Moss dan Atre, 2003) yang terdiri atas enam fase sekuensial (*Justification, Planning, Business Analysis, Design, Construction,* dan *Deployment*) telah berhasil diimplementasikan secara utuh dan sistematis. Pemrosesan ETL pada fase *Construction* sukses mengolah 101.401 baris data dengan tingkat integritas 100%, yang selanjutnya divisualisasikan pada fase *Deployment* menjadi *dashboard* analitik interaktif di Google Looker Studio.
3. *Dashboard* yang dikembangkan terbukti efektif berfungsi sebagai *Early Warning System* dalam memetakan rasio dosen terhadap mahasiswa. Sistem berhasil mengidentifikasi ketimpangan beban mengajar antarrumpun ilmu, di mana program studi rumpun Saintek berada pada kondisi terkendali (< 1:30), sementara beberapa program studi rumpun Soshum (seperti Akuntansi dan Pendidikan Sejarah) terdeteksi melampaui ambang batas kritis nasional (> 1:45).

### 5.2 Saran

Berdasarkan keterbatasan yang ditemukan selama penelitian, disarankan beberapa hal untuk pengembangan selanjutnya:

1. **Integrasi Data Internal (Siakadu):** Penelitian selanjutnya disarankan untuk membangun *pipeline* integrasi data langsung dengan basis data internal universitas (Siakadu) melalui *Application Programming Interface* (API), guna mengatasi keterbatasan jeda waktu (*delay*) pembaruan data pada portal publik PDDikti.
2. **Pengembangan Fitur Prediktif (*Forecasting*):** Perlu dikembangkan modul analitik prediktif berbasis *Machine Learning* untuk memproyeksikan tren rasio dosen-mahasiswa di masa mendatang, sehingga perencanaan alokasi sumber daya manusia dapat dilakukan secara proaktif.
