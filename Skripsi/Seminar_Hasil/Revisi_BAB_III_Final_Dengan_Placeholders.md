# BAB III METODOLOGI PENELITIAN

## III.1 Jenis dan Pendekatan Penelitian

Penelitian ini menggunakan jenis penelitian deskriptif kuantitatif dengan pendekatan _Business Intelligence_ (BI) sebagai landasan konseptual pendukung _Decision Support System_ (DSS). Sifat penelitian deskriptif kuantitatif dalam konteks ini bertujuan untuk memotret dan merepresentasikan kondisi data secara faktual dan objektif berdasarkan kumpulan data agregat numerik yang tersedia, tanpa bermaksud melakukan pengujian hipotesis (Sugiyono, 2019) maupun analisis prediktif yang kompleks.

Pendekatan _Business Intelligence_ digunakan sebagai solusi sistematis untuk mengolah, menganalisis, serta memvisualisasikan data agregat dari institusi pendidikan tinggi agar menjadi informasi yang lebih terstruktur dan berdaya guna. Metodologi kerangka kerja yang diadopsi dalam rancang bangun _Business Intelligence_ pada penelitian ini adalah **Business Intelligence Roadmap** yang dirumuskan oleh Moss & Atre (2003). Informasi yang dihasilkan melalui tahapan _Business Intelligence_ ini pada akhirnya akan direkomendasikan sebagai komponen penyokong informasi bagi _Decision Support System_ (DSS) untuk memudahkan pengambilan keputusan berbasis bukti (_data-driven decision making_) di lingkungan rektorat atau pengambil kebijakan tingkat perguruan tinggi.

Dalam penelitian ini, _Decision Support System_ (DSS) tidak dibangun sebagai aplikasi/sistem cerdas yang berdiri sendiri secara utuh, melainkan diposisikan secara konseptual (Gaftandzhieva dkk., 2023) yang memanfaatkan luaran hasil visualisasi dashboard _Business Intelligence_.

## III.2 Objek Penelitian

Objek observasi dalam penelitian ini adalah keseluruhan populasi tata kelola akademik pada Perguruan Tinggi Negeri berstatus Badan Layanan Umum (PTN BLU), dengan mengambil **studi kasus secara spesifik pada Universitas Siliwangi**. Pemilihan latar ini didasarkan pada karakteristik fleksibilitas layanan pengelolaan PTN BLU (Peraturan Pemerintah terkait) yang mengharuskan efisiensi sumber daya serta peran strategis PTN BLU dalam mencetak luaran pendidikan tinggi secara nasional.

Unit analisis dalam observasi ini berada pada level _institusi dan fakultas secara agregat_ (bukan pada level histori individu mahasiswa ataupun profil jejak rekam per dosen) untuk memperoleh gambaran utuh terkait keseimbangan kapasitas (_capacity planning_) perguruan tinggi (Murti & Mulyani, 2022).

## III.3 Variabel Penelitian

Variabel penelitian digunakan untuk membatasi arah analisis agar tetap terfokus pada rumusan masalah yang ditetapkan. Variabel kuantitatif yang diekstraksi dan dikaji meliputi:

1. **Jumlah Mahasiswa (Variabel X1):** Total persentase atau angka mahasiswa yang tercatat aktif secara administrasi pada institusi di periode tertentu.
2. **Jumlah Dosen (Variabel X2):** Total tenaga pendidik / dosen tetap maupun tidak tetap yang tercatat aktif ber-NIDN/NIDK dan ditugaskan pada tingkat institusi/fakultas.
3. **Rasio Dosen terhadap Mahasiswa (Variabel Y):** Perbandingan kalkulatif antara beban tanggungan peserta didik (mahasiswa) dibagi dengan total kapasitas pemberi layanan Tridharma (dosen) pada rumpun/institusi terkait (Santhi dkk., 2021).

Ketiga variabel tersebut merupakan _Key Performance Indicator_ (KPI) standar yang dipantau dalam mengevaluasi batas kewajaran daya tampung, akreditasi, dan pemerataan layanan kependidikan tinggi (Astuti dkk., 2024).

---

> **[TANDAI - TEMPATKAN TABEL DI SINI]**
> _Silakan masukkan di sini_ **[Tabel Definisi Operasional Variabel]** _dari salah satu jurnal referensi (misalnya jurnal tentang KPI Dasbor Akademik atau jurnal "Pooling Business Intelligence" milik Sharma & Joshi (2022)) jika Anda ingin memperlihatkan satuan ukurannya secara formal di Bab 3._

---

## III.4 Sumber dan Teknik Pengumpulan Data

Data yang digunakan dalam penelitian ini merupakan **data sekunder** (_secondary data requirement_) yang ditarik dari basis data terintegrasi milik kementerian. Sumber basis pelaporan utama diperoleh secara legal dari **Pangkalan Data Pendidikan Tinggi (PDDikti)** yang diakses melalui portal terbuka nasional (pddikti.kemdikbud.go.id). Pemilihan sumber ini krusial karena data PDDikti merepresentasikan _Single Source of Truth_ yang valid dan menjadi landasan akreditasi (Murti & Mulyani, 2022).

Pengumpulan data dari portal tersebut dieksekusi dengan teknik _Web Scraping_ dan _Crawling_ memanfaatkan otomasi _Skrip Python_ (menggunakan _library_ pemrosesan data otomatis seperti _Selenium_ atau metode _HTTP Request_). Otomasi ini mengekstraksi raw data profil institusi dan tabel komposisi (dosen-mahasiswa) program studi di lingkungan Universitas Siliwangi, yang kemudian dikonversi menjadi tabel terstruktur berekstensi _Comma-Separated Values_ (CSV) atau format _Data Mart_ lainnya sebagai fondasi analisis BI.

## III.5 Kerangka Metodologi Business Intelligence Roadmap (Moss & Atre, 2003)

Kerangka penyelesaian masalah atau pengembangan sistem dalam kajian ini berpedoman utuh pada siklus rekayasa informasi (lifecycle) **Business Intelligence Roadmap** oleh Larissa T. Moss dan Shaku Atre (2003). Metodologi ini dipandang ideal (dibandingkan CRISP-DM pada draf sebelumnya) utamanya karena pendekatan Moss & Atre (2003) sejak awal menitikberatkan pada aspek integrasi sumber daya organisasi dan diseminasi dashboard bagi pihak eksekutif bisnis/kampus (Stewart & Dewan, 2022).

---

> **[TANDAI - TEMPATKAN GAMBAR DI SINI]**
> _Silakan masukkan_ **[Gambar/Bagan Diagram Siklus Business Intelligence Roadmap (6 Tahapan)]** _atau modifikasi dari jurnal sumber (Moss & Atre, 2003) atau jurnal dari universitas lain._ _Jangan lupa cantumkan "(Sumber: Moss & Atre, 2003)" di bawah gambar tersebut._

---

Implementasi dari enam tahapan operasional berdasar panduan _Roadmap_ (Moss & Atre, 2003) ini dijelaskan sebagai berikut:

**1. Justification (Tahap Justifikasi)**
Tahap awal (_Business Case Assessment_) digunakan untuk memetakan urgensi penelitian. Pada tahap ini dirumuskan identifikasi masalah terkait penyajian laporan PDDikti yang selama ini masih bersifat tabular semata, memicu keterbatasan telaah kapasitas akademik (Astuti dkk., 2024). Karena itu, dijustifikasi sebuah usulan untuk menyajikan interaktivitas _dashboard_ guna menopang fungsionalitas DSS rektorat di Universitas Siliwangi.

**2. Planning (Tahap Perencanaan)**
Berfokus pada fase _Enterprise Infrastructure Evaluation_ (kesiapan teknologi). Peneliti merumuskan persiapan arsitektur _software_ meliputi lisensi _Python_ untuk skrip ekstraksi data (ETL), penentuan format file _CSV/JSON_ sebagai area _staging data_, serta identifikasi perangkat visualisasi (_misalnya Tableau, MS Power BI, atau antarmuka web khusus_) yang akan menerjemahkan wujud desain antar mukanya (Santhi dkk., 2021).

**3. Business Analysis (Tahap Analisis Kebutuhan Bisnis)**
Menetapkan lingkup informasi yang diharapkan oleh para pemangku kebijakan. Pada tahap analisis proyek (_Project Planning_), variabel dikerucutkan hanya pada data "Jumlah Dosen", "Jumlah Mahasiswa", perhitungan "Rasio", serta pembagiannya berdasarkan kategorisasi fakultas di internal institusi. Penyelarasan definisi operasional dipatok pada landasan pedoman BAN-PT dan _SN Dikti_ agar nilai rasio relevan secara hukum.

---

> **[TANDAI - TEMPATKAN TABEL/GAMBAR DI SINI]**
> _Silakan masukkan_ **[Gambar Conceptual Data Model]** _atau tabel pembagian "Kategori / Rentang Usia / Program Studi" sesuai jurnal referensi seperti Rahim dkk. (2025)._

---

**4. Design (Tahap Perancangan Sistem)**

- **Perancangan Repositori Data (_Data Design_):** Mendefinisikan wujud tabel repositori konseptual menggunakan model _Star Schema_ (_Data Mart_) yang memiliki _Fact Table_ (tabel pusat untuk besaran angka rasio) dikelilingi oleh _Dimension Tables_ (seperti Dimensi Waktu/Semester dan Dimensi Prodi/Fakultas).
- **Perancangan ETL (_ETL Design_):** Merancang arsitektur penarikan data mentah PDDikti, standarisasi teks yang berantakan, serta pembuangan atribut nol.

**5. Construction (Tahap Konstruksi Sistem)**
Fase perakitan teknis yang mencakup:

- **Konstruksi ETL:** Pemrograman aktual (_Coding_) untuk memproses, memformat, dan meng-_load_ dataset yang telah divalidasi ke dalam lingkungan visualisasi.
- **Konstruksi Dashboard Aplikasi (_Application Development_):** Melakukan _layouting_ dan pengembangan tata letak _Dashboard Academic Intelligence_ yang merangkum keseluruhan data populasi dari skrip ETL.

**6. Deployment (Tahap Penyebaran/Implementasi)**
_Release_ kerangka sistem akhir dengan mengeksekusi (_run_) pemuatan dasbor visual secara utuh bagi audiens manajerial. Tahapan ini selaras dengan prinsip _Decision Support System_ di mana dasbor tersebut tidak hanya dipajang, namun diuji apakah ia siap dipakai dan ditelaah (_evaluate_) sebagai pijakan penaksiran kebijakan kapasitas SDM (Sharma & Joshi, 2022).

## III.6 Tata Kelola Data dan Perhitungan Rasio Kapasitas

Mengacu pada arsitektur penyajian metriks _(Business analysis)_ dalam pendekatan BI Moss & Atre, perumusan _key value_ wajib diukur memakai formula matematis. Rumus keseimbangan rasio ini disadur dan disesuaikan standar Badan Akreditasi Nasional Perguruan Tinggi (BAN-PT) serta regulasi _Standar Nasional Pendidikan Tinggi_ (SN-Dikti) guna memonitor _Beban Kerja Dosen_ (BKD).

Formulasi ekuivalensinya adalah (Gaftandzhieva dkk., 2023):
$$ Rasio_Kapasitas = \frac{Total\,Mahasiswa\,Aktif\,Tertulis}{Total\,Dosen\,Penugasan\,Terdaftar} $$

Hasil keluaran rasio tersebut akan diproyeksikan melalui visualisasi warna (indikator waspada) pada _Dashboard BI_ berdasarkan batasan (_threshold_) interpretatif berikut:

1.  **Rasio ≤ 30 (Kondisi Ideal/Seimbang):** Beban pengajaran dosen masih aman dan proporsional untuk lingkup rumpun umum maupun eksakta (merujuk instrumen minimum pembukaan prodi BAN-PT). Indikator warna akan di-setting ke arah zona hijau.
2.  **Rasio > 30 hingga ≤ 45 (Transisi / Wajar Bersyarat):** Untuk rumpun ilmu Sosial & Humaniora dinilai masih tergolong wajar (sesuai SE BAN-PT/LLDIKTI) namun berpotensi meluap seiring penambahan _intake_ maba baru.
3.  **Rasio > 45 / 60 (Kondisi Sangat Padat / Overload):** Mengindikasikan pembengkakan beban kelas untuk satu dosen (_overcrowding_), sangat beresiko melebihi standar perhitungan 16 SKS perminggu menurut regulasi PO BKD, berimbas negatif terhadap fungsi penelitian dan kepengurusan akreditasi (Zhang & Goyal, 2024). Indikator akan dibuat menyala (warna merah/_warning_).

Penetapan pembatas rasio ini bersifat analitik-simbolik di dalam lapisan antarmuka Intelligence, bukan sebagai rekayasa vonis (Santhi dkk., 2021). Pendekatan interpretasi berbasis BI ini selaras dengan asas _Decision Support System_ yang berfungsi menyediakan indikasi empiris terstruktur tanpa mengambil kendali keputusan mutlak dari pimpinan PTN BLU (Mellyka dkk., 2025).

## III.7 Diagram Alir / Flowchart Penelitian

Untuk meringkas serangkaian pendekatan studi _deskriptif-Business Intelligence_ ini, pola urutan pelaksanaannya dirangkum pada skema alur di bawah ini.

---

> **[TANDAI - TEMPATKAN GAMBAR DI SINI]**
> _Di sini tempatkan_ **[Gambar Flowchart Pelaksanaan Analisis Data / Integrasi Penelitian Anda Sendiri yang berwujud kotak-kotak bagan alir penelitian dari awal mula start hingga kesimpulan akhir.]**

---
