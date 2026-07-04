# ANALISIS DATA AGREGAT PERGURUAN TINGGI NEGERI BADAN LAYANAN UMUM (PTN BLU) MENGGUNAKAN PENDEKATAN BUSINESS INTELLIGENCE

**Fauzi Noorsyabani¹\***
¹Program Studi Sistem Informasi, Fakultas Teknik, Universitas Siliwangi; Tasikmalaya, Indonesia

**Keywords:** _Business Intelligence; Data Warehouse; Institutional Capacity Analytics; PDDikti; Higher Education Data Governance._

**Corespondent Email:** career.fauzinoorsyabani@gmail.com

---

**Abstrak.** _Pangkalan Data Pendidikan Tinggi (PDDikti) menyediakan data agregat nasional yang fundamental bagi tata kelola data pendidikan tinggi (Higher Education Data Governance). Namun, penyajian yang bersifat statis menghambat evaluasi kapasitas institusional, khususnya tren rasio dosen terhadap mahasiswa pada Perguruan Tinggi Negeri Badan Layanan Umum (PTN BLU). Penelitian ini mengimplementasikan Business Intelligence (BI) untuk mewujudkan Institutional Capacity Analytics melalui analisis longitudinal data agregat Universitas Siliwangi sebagai PTN BLU, yang mencakup 35 program studi aktif selama lima periode pelaporan (Ganjil 2023–Ganjil 2025). Metodologi BI Roadmap digunakan untuk menstrukturkan proses Extract, Transform, Load (ETL) guna mengintegrasikan data agregat PDDikti ke dalam sebuah Data Warehouse berskema bintang (star schema). Hasil analisis longitudinal mengungkap disparitas tersembunyi antar program studi, di mana tiga program studi teridentifikasi melampaui ambang batas rasio maksimal yang ditetapkan regulasi (Pendidikan Sejarah 1:54,0; Pendidikan Masyarakat 1:50,9; Akuntansi 1:45,7). Kontribusi utama penelitian ini adalah kerangka Decision Support berbasis Data Warehouse yang memperkuat kapabilitas analitik institusi. Dashboard dalam penelitian ini difungsikan murni sebagai mekanisme penyampaian informasi (delivery mechanism) dari proses BI yang telah mentransformasi data statis menjadi landasan pengambilan keputusan strategis secara terstruktur dan terpusat._

**Abstract.** _The Higher Education Database (PDDikti) provides national aggregate data fundamental to Higher Education Data Governance. However, its static presentation hinders the evaluation of institutional capacity, specifically the lecturer-to-student ratio trends in Public Universities with Public Service Agency status (PTN BLU). This study implements Business Intelligence (BI) to realize Institutional Capacity Analytics through longitudinal analysis of PDDikti aggregate data from Universitas Siliwangi as a PTN BLU, encompassing 35 active study programs across five reporting periods (Odd Semester 2023–Odd Semester 2025). The BI Roadmap methodology is employed to structure the Extract, Transform, Load (ETL) processes, integrating PDDikti aggregate data into a star schema Data Warehouse. The results of the longitudinal analysis revealed hidden disparities among study programs, identifying three programs exceeding the maximum regulatory ratio threshold: Pendidikan Sejarah (1:54.0), Pendidikan Masyarakat (1:50.9), and Akuntansi (1:45.7). The main contribution of this research is a Data Warehouse-based Decision Support framework that strengthens the analytical capabilities of the institution. The dashboard in this study functions purely as a delivery mechanism for the BI process, which has successfully transformed static data into a foundation for structured and centralized strategic decision-making._

---

## 1. PENDAHULUAN

Perguruan tinggi modern secara kontinu menghasilkan data akademik dalam volume besar yang esensial untuk dimanfaatkan sebagai landasan tata kelola data pendidikan tinggi (_Higher Education Data Governance_) dan pengambilan keputusan strategis [1]. Dalam konteks Perguruan Tinggi Negeri berstatus Badan Layanan Umum (PTN BLU), _Institutional Capacity Analytics_—khususnya terkait pemantauan kapasitas akademik—memiliki implikasi langsung terhadap efektivitas layanan pendidikan, akuntabilitas kinerja, serta perencanaan sumber daya. Keseimbangan rasio antara jumlah dosen dan mahasiswa merupakan metrik vital; ketidakseimbangan pada rasio ini berpotensi menurunkan kualitas pembelajaran dan mendistorsi distribusi beban akademik secara tidak proporsional [2]. Oleh karena itu, evaluasi objektif mengenai keseimbangan kapasitas institusi menjadi prasyarat mutlak agar institusi dapat mematuhi standar mutu pendidikan yang ditetapkan oleh regulasi pemerintah [3]. Universitas Siliwangi, sebagai PTN BLU di Tasikmalaya, merepresentasikan konteks institusional yang relevan di mana pengelolaan kapasitas akademik berbasis data menjadi kebutuhan yang mendasar dan terstruktur.

Secara nasional, Pangkalan Data Pendidikan Tinggi (PDDikti) telah menjadi repositori utama yang merepresentasikan data agregat institusi pendidikan tinggi secara publik. PDDikti memuat informasi agregat yang bersifat fundamental bagi tata kelola data publik. Namun, tantangan mendasar yang muncul adalah penyajian representasi data pada portal tersebut masih bersifat statis dan deskriptif, di mana informasi umumnya hanya disajikan dalam format laporan standar untuk satu periode pelaporan tertentu [2]. Kondisi yang tidak terintegrasi untuk komparasi lintas-periode ini menyebabkan data mentah tersebut sulit dieksploitasi secara otomatis untuk mendukung analisis tren longitudinal. Akibatnya, pimpinan institusi kesulitan memetakan kapasitas akademik secara utuh dan menyeluruh tanpa harus melalui proses rekapitulasi manual yang rentan terhadap inefisiensi dan inkonsistensi data.

Di sisi lain, telaah terhadap penelitian terdahulu menunjukkan bahwa implementasi pendekatan _Business Intelligence_ (BI) di sektor pendidikan tinggi masih dominan berfokus pada skala mikro dan operasional lokal. Mayoritas riset cenderung mengisolasi pengolahan data pada _database_ internal kampus untuk keperluan spesifik, seperti analisis data pelacakan alumni (_tracer study_) [4], evaluasi sistem penerimaan mahasiswa baru [5], atau pemantauan metrik penjaminan mutu fakultas yang beroperasi dalam silo [6]. Penelitian-penelitian tersebut sering kali meminggirkan peran strategis dari integrasi pemrosesan _Extract, Transform, Load_ (ETL) dan ketangguhan arsitektur _Data Warehouse_ sebagai inti kapabilitas analitik institusi, serta belum mengeksplorasi potensi pemanfaatan data agregat PDDikti berskala nasional. Hal ini menciptakan **kesenjangan penelitian (_research gap_)** yang signifikan antara ketersediaan data terbuka pemerintah dengan kapabilitas analitik dan visibilitas pada tingkat institusi.

Berangkat dari _research gap_ tersebut, **kebaruan (_novelty_)** dari penelitian ini terletak pada perancangan arsitektur _Business Intelligence_ yang _end-to-end_—mengekstraksi data agregat publik (PDDikti) secara terotomasi dan menstrukturkannya ke dalam _Data Warehouse_ yang secara khusus didedikasikan untuk kebutuhan _Institutional Capacity Analytics_ secara longitudinal. Pendekatan ini mentransformasi metode evaluasi kapasitas akademik tradisional yang reaktif menjadi tata kelola data terpusat (_Single Version of the Truth_). Adapun **kontribusi** utama dari riset ini adalah ketersediaan _pipeline_ ETL dan infrastruktur _Data Warehouse_ yang menghasilkan kerangka sistem pendukung keputusan (_Decision Support System_/DSS) yang tangguh. Sistem ini secara proaktif mampu mendeteksi disparitas struktural dan potensi pelanggaran batas rasio akademik (seperti rasio > 1:45). Dalam konteks ini, _dashboard_ diposisikan murni sebagai mekanisme penyampaian informasi (_delivery mechanism_) dari wawasan yang dihasilkan _Data Warehouse_, bukan sebagai fokus tunggal dari sistem [7].

Dengan demikian, **tujuan dari penelitian ini** adalah untuk mengimplementasikan pendekatan _Business Intelligence_ berbasis integrasi _Data Warehouse_ dan proses ETL guna mengevaluasi tren rasio dosen terhadap mahasiswa secara longitudinal menggunakan data agregat PDDikti. Evaluasi ini pada akhirnya ditujukan untuk menyediakan infrastruktur _Decision Support_ yang terstruktur bagi pimpinan PTN BLU dalam memantau dan mengoptimalkan perencanaan strategis kapasitas akademik.

## 2. TINJAUAN PUSTAKA

Isi bagian tinjauan pustaka difokuskan secara ringkas pada landasan teori yang benar-benar digunakan sebagai fondasi arsitektur analitik dalam penelitian ini.

**2.1 Business Intelligence**
_Business Intelligence_ (BI) merupakan kerangka kerja komprehensif yang mengintegrasikan metodologi, arsitektur, dan teknologi untuk mengubah data mentah menjadi wawasan bermakna guna mendorong tindakan strategis [8]. Dalam domain pendidikan tinggi, BI melampaui sekadar visualisasi data; BI adalah serangkaian proses sistematis yang mengekstraksi nilai dari aset data institusi untuk mentransformasi manajemen reaktif menjadi proaktif [9].

**2.2 Data Warehouse**
_Data Warehouse_ (DW) bertindak sebagai infrastruktur fundamental di dalam arsitektur BI yang mensentralisasi data ke dalam satu repositori analitik [10]. Dalam penelitian ini, DW dirancang menggunakan pendekatan pemodelan dimensional (_star schema_), yang secara logis memisahkan fakta kuantitatif dari dimensi deskriptif guna mengoptimalkan agregasi data [11]. Kehadiran DW mendirikan satu kebenaran tunggal (_Single Version of the Truth_) yang memastikan seluruh pemangku kepentingan mengakses metrik tervalidasi yang seragam [12].

**2.3 Decision Support System**
_Decision Support System_ (DSS) adalah entitas komputasional yang mendukung pimpinan dalam memecahkan permasalahan manajerial semi-terstruktur [1]. Dalam konteks kapasitas akademik, integrasi antara _Data Warehouse_ sebagai penyuplai data terstruktur dan antarmuka analitik menghasilkan kerangka DSS yang memampukan pengambil keputusan merespons dinamika rasio dosen dan mahasiswa secara cepat [7].

**2.4 Data Agregat PDDikti**
Data agregat merupakan metrik tingkat makro hasil konsolidasi observasi individu, yang memungkinkan penemuan tren tanpa mengungkap data granular [13]. Pangkalan Data Pendidikan Tinggi (PDDikti) berfungsi sebagai sentra data agregat nasional yang determinatif bagi _Higher Education Data Governance_. Data PDDikti menjadi fondasi standar yang sah untuk mengevaluasi kepatuhan institusi terhadap ambang batas regulasi rasio pendidikan [2].

**2.5 Research Gap Analysis**
Studi literatur terhadap penelitian sebelumnya mengungkap bahwa adopsi BI di institusi pendidikan tinggi dominan berfokus pada optimasi _database_ internal dan bersifat parsial. Studi oleh Sinlae dkk. (2024) [4] dan Mellyka dkk. (2025) [14] membatasi penerapan BI pada pemantauan data alumni secara terisolasi. MZ dkk. (2022) [5] memanfaatkan BI untuk ranah admisi mahasiswa baru. Sementara itu, Sorour & Atkins (2024) [6] dan Hasan (2019) [15] masing-masing memfokuskan implementasi BI pada sistem penjaminan mutu dan rekam jejak penelitian dosen secara parsial. Riset-riset tersebut menunjukkan relevansi BI di perguruan tinggi, namun terbatas pada metrik tingkat sub-unit dan belum mengeksplorasi pemanfaatan data agregat berskala nasional.

Di sisi lain, kajian yang bersinggungan langsung dengan PDDikti, seperti yang dilakukan oleh Astuti dkk. (2024) [2] dan Ady Bakri dkk. (2023) [16], lebih mengedepankan isu tata kelola data dari sudut pandang adopsi manajerial dan _user acceptance_, tanpa mengembangkan arsitektur analitik untuk memproses data tersebut. Oleh karena itu, terdapat celah (_research gap_) yang nyata: **belum adanya riset komprehensif yang mengimplementasikan arsitektur _Data Warehouse_ secara spesifik untuk mengintegrasikan data agregat PDDikti guna kepentingan _Institutional Capacity Analytics_ secara longitudinal.** Penelitian ini mengisi celah tersebut dengan merancang _pipeline_ BI yang berfokus pada kapabilitas mendeteksi kepatuhan rasio kapasitas akademik Universitas Siliwangi sebagai PTN BLU terhadap standar regulasi pemerintah.

## 3. METODE PENELITIAN

Metode penelitian dirancang secara sistematis untuk mengekstraksi, mentransformasi, dan menganalisis data agregat perguruan tinggi agar dapat memfasilitasi pengambilan keputusan strategis.

**3.1 Research Design**
Penelitian ini menggunakan pendekatan kuantitatif yang mengadopsi kerangka kerja _Business Intelligence_ untuk mengevaluasi kapasitas akademik Universitas Siliwangi (PTN BLU). Variabel utama yang dianalisis mencakup jumlah mahasiswa aktif, jumlah dosen penghitung rasio, dan rasio dosen terhadap mahasiswa pada tingkat program studi. Analisis dilakukan secara longitudinal yang mencakup lima periode pelaporan beruntun (Ganjil 2023 hingga Ganjil 2025).

**3.2 Business Intelligence Roadmap**
Pengembangan arsitektur analitik disusun berdasarkan metodologi _Business Intelligence Roadmap_ [11] yang terstruktur atas enam fase sekuensial: _Justification_ (penentuan urgensi analitik kapasitas), _Planning_ (perencanaan arsitektur data), _Business Analysis_ (penetapan kebutuhan informasi dan metrik rasio), _Design_ (perancangan model struktural), _Construction_ (implementasi _pipeline_ pemrosesan data), dan _Deployment_ (pengembangan _dashboard_ dan uji coba).

**3.3 Data Collection**
Sumber data primer diperoleh langsung dari portal Pangkalan Data Pendidikan Tinggi (pddikti.kemdiktisaintek.go.id). Karena ketiadaan _Application Programming Interface_ (API) publik, metode _web scraping_ diimplementasikan menggunakan pustaka _Selenium WebDriver_ dengan bahasa pemrograman Python. Otomasi ini menavigasi halaman detail perguruan tinggi untuk mengekstraksi 12 atribut data agregat dari seluruh program studi di setiap periode pelaporan ke dalam _dataset_ mentah (_raw data_).

**3.4 ETL Process**
Tahap _Construction_ direalisasikan melalui mekanisme _Extract, Transform, Load_ (ETL) menggunakan pustaka Pandas pada Python:

1. **Extract**: Membaca arsip CSV mentah hasil rekaman _web scraping_.
2. **Transform**: Mengeksekusi enam langkah pembersihan secara komputasional, meliputi pemfilteran ruang lingkup institusi, eliminasi baris bernilai _null_, pemisahan atribut periode, konversi tipe data numerik, standarisasi metadata dasar institusi, serta _parsing_ pemformatan teks rasio dari "1:X" menjadi metrik absolut bernilai _float_.
3. **Load**: Menyimpan himpunan data yang telah ditransformasikan ke dalam repositori _Data Warehouse_.

**3.5 Data Warehouse Design**
_Data Warehouse_ didesain menggunakan pendekatan pemodelan dimensional untuk mempercepat kueri analitik multidimensi. Sebagaimana praktik terbaik integrasi data pada penelitian terdahulu, pemodelan dimensional terbukti sangat efektif dalam menyederhanakan kompleksitas basis data relasional dan mengoptimalkan performa arsitektur _data warehouse_ [17]. Tingkat granularitas (_grain_) data ditetapkan secara ketat pada "satu program studi per satu periode pelaporan". Penetapan _grain_ ini penting untuk menjamin konsistensi matematis dalam agregasi kalkulasi turunan pada _dashboard_ [11].

**3.6 Star Schema Design**
Arsitektur model data diimplementasikan dalam pola _Star Schema_, memuat satu tabel fakta (`Fact_Kapasitas_Pendidikan`) yang terpusat dan dikelilingi oleh tiga tabel dimensi (`Dim_Waktu`, `Dim_Universitas`, dan `Dim_Prodi`). Tabel fakta merekam metrik esensial berupa jumlah mahasiswa, jumlah dosen penghitung rasio, serta nilai absolut rasio. Formula fundamental untuk rasio akademik didefinisikan secara konseptual sebagai pembagian antara total jumlah mahasiswa dengan total jumlah dosen penghitung rasio.

**3.7 Dashboard Development**
Siklus _Deployment_ diwujudkan melalui pengintegrasian himpunan data _Data Warehouse_ (yang didenormalisasi) ke dalam Google Looker Studio via _cloud spreadsheet_. _Dashboard_ ini menstrukturkan penyajian informasi ke dalam tiga panel spesifik: fitur agregasi tingkat eksekutif, _heatmap_ disparitas rasio antar program studi, serta pemantauan tren kapasitas secara longitudinal. Pemrograman visualisasi komparatif menggunakan _Matplotlib_ dan _Seaborn_ pada Python turut diterapkan sebagai ekstensi pendalaman analitik (_drill-down_).

**3.8 Data Validation**
Tahap validasi memastikan integritas implementasi BI melalui pengujian konsistensi data akhir. Pengujian dilakukan dengan pencocokan komparatif antara metrik hasil komputasi _Data Warehouse_ di _back-end_ dengan representasi _front-end_ yang dirender pada _dashboard_ Looker Studio. Proses konfirmasi membuktikan tingkat presisi 100%, menjamin tidak adanya distorsi logika maupun matematis dari serangkaian intervensi pemrosesan ETL yang telah dikonstruksi.

## 4. HASIL DAN PEMBAHASAN

Bagian ini menyajikan luaran konkrit dari implementasi sistem _Business Intelligence_ pada data agregat PDDikti Universitas Siliwangi, yang mencakup hasil pemrosesan _pipeline_ ETL, pembentukan _Data Warehouse_, dan presentasi metrik kapasitas akademik melalui antarmuka _dashboard_ analitik.

**4.1 Hasil Implementasi ETL**
Proses _Extract, Transform, Load_ (ETL) secara komputasional telah mengeksekusi integrasi data agregat dari PDDikti. Pada tahap **Extract**, skrip otomatisasi berhasil menghimpun _dataset_ mentah nasional tanpa hambatan struktural. Tahap **Transform** kemudian secara spesifik menyaring ruang lingkup data hanya untuk Universitas Siliwangi, mengeliminasi observasi yang berstatus _null_, dan mengonversi format teks rasio "1:X" menjadi metrik absolut bernilai _float_. Transformasi ini menghasilkan _dataset_ bersih sejumlah 202 baris rekaman data, yang merepresentasikan 35 program studi aktif selama 5 periode pelaporan berturut-turut. Rangkuman luaran tahap transformasi dapat dilihat pada Tabel 1.

**Tabel 1.** Ringkasan Hasil Pemrosesan Transformasi Data
| Langkah Pemrosesan | Hasil Luaran |
| :--- | :--- |
| Penyaringan Ruang Lingkup | Mengisolasi data khusus Universitas Siliwangi dari _dataset_ nasional. |
| Eliminasi _Null_ | Menghapus baris tanpa kode prodi, periode, atau rasio. |
| Konversi Format Rasio | Mengekstraksi teks format "1:X" menjadi nilai absolut _float_. |
| Standarisasi Metadata | Membakukan nama universitas, status PTN, dan akreditasi. |

Pada tahap **Load**, data yang telah ditransformasi direstrukturisasi menjadi arsitektur _Star Schema Data Warehouse_. Pembentukan struktur ini menghasilkan empat tabel utama: `Fact_Kapasitas_Pendidikan` (202 baris), `Dim_Prodi` (41 baris referensi termasuk prodi inaktif), `Dim_Waktu` (5 baris referensi semester kronologis), dan `Dim_Universitas` (1 baris). Keseluruhan tabel terintegrasi ini menjadi pondasi penyimpanan terpusat (_Single Version of the Truth_).

**Tabel 2.** Spesifikasi _Star Schema Data Warehouse_ yang Terbentuk

| Nama Tabel | Jenis Model | Jumlah Atribut | Rekaman Baris |
| :--- | :--- | :--- | :--- |
| Fact\_Kapasitas\_Pendidikan | Fact Table | 10 Kolom | 202 Baris |
| Dim\_Prodi | Dimension Table | 5 Kolom | 41 Baris |
| Dim\_Waktu | Dimension Table | 4 Kolom | 5 Baris |
| Dim\_Universitas | Dimension Table | 6 Kolom | 1 Baris |

**4.2 Hasil Dashboard Analitik**
Hasil akhir perancangan BI diwujudkan melalui platform Google Looker Studio. _Dashboard_ difungsikan murni sebagai _delivery mechanism_ dari wawasan komputasional yang diproduksi oleh _Data Warehouse_, dan disusun dalam tiga panel utama sebagaimana ditampilkan pada Gambar 1, 2, dan 3.

**Gambar 1.** Panel _Executive Overview_ — _Dashboard_ Analitik Kapasitas Akademik Universitas Siliwangi pada Google Looker Studio

![Gambar 1 Panel Executive Overview Dashboard Analitik Universitas Siliwangi](d:\Code\Tugas Akhir\Skripsi\Hasil Dashboard ke dua\Screenshot 2026-06-08 073435.png)

*Sumber: Hasil implementasi penelitian (2026)*

Panel **Executive Overview** (Gambar 1) menyajikan pemantauan _Key Performance Indicator_ (KPI) secara makro. _Scorecard_ interaktif pada panel ini menampilkan akumulasi total mahasiswa aktif dan dosen penghitung rasio dari seluruh periode pelaporan, dilengkapi _line chart_ untuk pelacakan tren rasio institusional secara kronologis dan diagram distribusi prodi yang menunjukkan dominasi jenjang Strata 1 sebesar 89,7%. Nilai rata-rata rasio dosen terhadap mahasiswa per program studi yang dianalisis secara akurat menggunakan Python berada pada kisaran **24,1—24,9** selama periode pengamatan — jauh di bawah ambang batas regulasi DIKTI (1:45), menunjukkan kondisi institusi secara agregat masih dalam kategori sehat.

**Gambar 2.** Panel Analisis Detail Per Program Studi — Matriks Nilai Rasio, _Bar Chart_, dan _Scatter Plot_ Dosen-Mahasiswa Universitas Siliwangi

![Gambar 2 Panel Analisis Detail Per Program Studi](d:\Code\Tugas Akhir\Skripsi\Hasil Dashboard ke dua\Screenshot 2026-06-08 073637.png)

*Sumber: Hasil implementasi penelitian (2026)*

Panel **Analisis Detail Per Program Studi** (Gambar 2) menyajikan alat ukur komparatif antar-departemen. Matriks tabel silang (_cross-table_) program studi × periode pelaporan memfasilitasi visibilitas titik kelebihan beban mengajar. _Scatter plot_ jumlah mahasiswa terhadap nilai rasio mengungkap struktur beban spesifik — Pendidikan Masyarakat dan Pendidikan Sejarah menjadi program studi dengan kombinasi populasi mahasiswa signifikan dan rasio melebihi ambang DIKTI.

**Gambar 3.** Panel Tren Longitudinal dan Monitoring — Tren Rasio Lintas-Semester Per Program Studi

![Gambar 3 Panel Tren Longitudinal dan Monitoring](d:\Code\Tugas Akhir\Skripsi\Hasil Dashboard ke dua\Screenshot 2026-06-08 073711.png)

*Sumber: Hasil implementasi penelitian (2026)*

Panel **Tren Longitudinal** (Gambar 3) menampilkan perkembangan nilai rasio per program studi sepanjang lima periode pelaporan, dilengkapi tabel peringkat untuk identifikasi cepat program studi berbeban tertinggi. Melalui tahap validasi teknis, dipastikan bahwa seluruh metrik yang dihitung oleh _Data Warehouse_ di _back-end_ konsisten 100% dengan representasi yang ditampilkan melalui visualisasi Python pada tingkat presisi absolut.

**4.3 Temuan Analitik (_Analytical Findings_)**
Implementasi _Business Intelligence_ memfasilitasi pergeseran analisis dari agregasi level makro menuju komparasi lintas departemen secara granular. Secara agregat, _Data Warehouse_ berhasil mengintegrasikan 202 rekaman observasi yang merepresentasikan akumulasi data dari 35 program studi aktif Universitas Siliwangi selama lima semester (Ganjil 2023–Ganjil 2025), dengan total kumulatif 101.401 catatan data mahasiswa aktif dan 2.461 catatan data dosen penghitung rasio dari seluruh periode pelaporan. Angka kumulatif tersebut merupakan penjumlahan seluruh rekaman antar-semester, bukan representasi jumlah populasi aktual mahasiswa atau dosen pada satu periode tertentu. Pada level institusional per semester, nilai rata-rata rasio per program studi Universitas Siliwangi secara konsisten berada dalam rentang **24,1—24,9** — jauh di bawah ambang batas regulasi maksimal pemerintah (1:45).

Namun demikian, analisis _heatmap_ dan komparasi program studi mengungkap keberadaan disparitas beban akademik struktural yang tertutupi oleh nilai rata-rata institusi tersebut. Sebagai instrumen analitik komplementer, visualisasi _heatmap_ longitudinal pada Gambar 4 menyajikan distribusi nilai rasio secara multidimensi (program studi × periode pelaporan), memfasilitasi identifikasi pola persistensi beban berlebih secara serentak.

**Gambar 4.** _Heatmap_ Nilai Rasio Dosen:Mahasiswa per Program Studi × Periode Pelaporan Universitas Siliwangi (Ganjil 2023—Ganjil 2025)

![Gambar 4 Heatmap Rasio per Program Studi x Semester](d:\Code\Tugas Akhir\Outputs\Visualizations\heatmap_prodi_semester.png)

*Sumber: Hasil analisis data PDDikti menggunakan Python/Seaborn (2026)*

Penarikan data dari _Data Warehouse_ berhasil mendeteksi **tiga program studi** yang pada periode terbaru (Ganjil 2025) secara spesifik beroperasi melampaui batas rasio maksimal 1:45, yakni: **Pendidikan Sejarah** (1:54,0), **Pendidikan Masyarakat** (1:50,9), dan **Akuntansi** (1:45,7). Analisis longitudinal lebih lanjut menegaskan bahwa Pendidikan Masyarakat menunjukkan pola pelanggaran yang paling persisten — nilai rasionya melampaui ambang batas DIKTI pada tiga dari lima periode pengamatan (47,6 → 57,4 → 58,5 → 50,8 → 50,9). Secara longitudinal, pemantauan tren historis menunjukkan bahwa fluktuasi metrik rasio pada program studi tersebut tidak mengalami perbaikan organik yang signifikan selama lima semester pelaporan terakhir.

**4.4 Pembahasan (_Discussion_)**
Temuan analitik kuantitatif di atas menegaskan urgensi penerapan _Institutional Capacity Analytics_ pada tingkat institusional. Disparitas kapasitas pengajaran yang tersembunyi berdampak langsung pada ketidakseimbangan alokasi beban kerja dosen, yang secara probabilitas memengaruhi efektivitas pembelajaran serta berisiko menurunkan pemenuhan instrumen akreditasi [3]. Implikasi institusional dari temuan ini menuntut pimpinan perguruan tinggi untuk menggeser paradigma kebijakan distribusi sumber daya—dari pola pemerataan konvensional menuju intervensi presisi. Strategi mitigasi, baik melalui pembatasan rasional kuota mahasiswa baru maupun prioritas penambahan formasi dosen tetap, harus dialokasikan secara tajam ke **tiga program studi** yang telah diidentifikasi berada dalam zona kritis (Pendidikan Sejarah, Pendidikan Masyarakat, dan Akuntansi).

Dalam kerangka _Decision Support_, penelitian ini menggarisbawahi kekuatan arsitektur _Data Warehouse_ sebagai kontributor utama, alih-alih mereduksi BI sekadar menjadi alat pembuat _dashboard_. _Dashboard_ tidak lebih dari instrumen presentasi (_delivery mechanism_); nilai inovasi sesungguhnya terletak pada keberhasilan _pipeline_ ETL dalam mengotomatisasi ekstraksi data statis pelaporan PDDikti, mentransformasikannya, dan menstrukturkannya menjadi ruang analitik komprehensif. Infrastruktur ini secara efektif mengeliminasi audit rekonsiliasi manual yang rentan bias. Dengan mendirikan repositori _Single Version of the Truth_, institusi kini dilengkapi dengan kapabilitas analisis proaktif berbasis bukti objektif [1].

Sebagai komparasi, literatur terdahulu merepresentasikan kesenjangan operasional. Riset-riset terdahulu, sebagaimana yang dilakukan oleh Sinlae dkk. (2024) [4] dan MZ dkk. (2022) [5], membatasi kapabilitas BI pada basis data level lokal yang spesifik (seperti data alumni atau seleksi mahasiswa) dengan orientasi yang dominan pada aspek perancangan visual antarmuka (UI). Penelitian ini melangkah lebih jauh dengan membuktikan bahwa pendayagunaan data agregat berskala nasional melalui perancangan _Star Schema Data Warehouse_ yang kokoh merupakan fondasi sejati bagi terbentuknya tata kelola data pendidikan tinggi (_Higher Education Data Governance_) yang mampu memberikan daya dukung keputusan strategis secara terukur [10].

## 5. KESIMPULAN

Berdasarkan hasil perancangan dan analisis implementasi _Business Intelligence_ pada data agregat PDDikti, dapat ditarik beberapa kesimpulan sebagai berikut:

1. **Temuan Utama:** Implementasi arsitektur analitik pada data agregat PDDikti Universitas Siliwangi berhasil mengekstraksi dan mengintegrasikan data statis institusi menjadi wawasan longitudinal. Meskipun rasio dosen terhadap mahasiswa pada tingkat makro universitas terlihat stabil (rata-rata per prodi berkisar 24,1—24,9), kapabilitas agregasi mendeteksi adanya ketimpangan struktural yang tersembunyi pada **tiga program studi** (Pendidikan Sejarah, Pendidikan Masyarakat, dan Akuntansi), di mana rasio beban pengajaran secara konsisten melampaui atau mendekati batas maksimal regulasi 1:45.
2. **Kontribusi Penelitian:** Penelitian ini berkontribusi memperkuat _Higher Education Data Governance_ dengan membuktikan bahwa arsitektur BI _end-to-end_—dari otomatisasi _pipeline_ ETL hingga _Star Schema Data Warehouse_—merupakan kerangka fundamental yang menggerakkan _Decision Support System_, alih-alih sekadar perancangan visual antarmuka (_dashboard_).
3. **Implikasi Praktis:** Bagi Universitas Siliwangi, ketersediaan repositori terpusat ini mentransformasi mekanisme evaluasi kapasitas institusi dari pola audit rekapitulasi manual yang reaktif menjadi tata kelola proaktif berbasis data (_Single Version of the Truth_). Pimpinan dapat langsung mengeksekusi intervensi presisi, seperti prioritas rekrutmen formasi dosen tetap atau pembatasan kuota mahasiswa baru pada **tiga program studi** yang berada dalam zona kritis (Pendidikan Sejarah, Pendidikan Masyarakat, dan Akuntansi).
4. **Keterbatasan:** Ruang lingkup komputasional penelitian ini secara eksklusif membatasi sumber data pada variabel agregat publik PDDikti. Pemodelan belum mengintegrasikan metrik internal operasional kampus secara granular, seperti sistem pelacakan Beban Kerja Dosen (BKD) _real-time_.
5. **Penelitian Lanjutan:** Riset di masa mendatang sangat direkomendasikan untuk memperluas arsitektur analitik ini dengan mengintegrasikan kapabilitas pemelajaran mesin (_Machine Learning_). Hal ini bertujuan agar _Data Warehouse_ mampu melakukan prediksi (_forecasting_) tren kelebihan beban akademik secara prediktif sebelum ambang batas rasio terlampaui.

## DAFTAR PUSTAKA

[1] J. Zhang and S. B. Goyal, "AI-Driven Decision Support System Innovations to Empower Higher Education Administration," _Journal of Computers, Mechanical and Management_, vol. 3, no. 2, pp. 35-41, 2024.
[2] H. M. Astuti, R. P. Wibowo, and A. Herdiyanti, "Towards the National Higher Education Database in Indonesia: Challenges to Data Governance Implementation from The Perspective of a Public University," _Procedia Computer Science_, vol. 234, pp. 1322-1331, 2024.
[3] S. Gaftandzhieva, S. Hussain, S. Hilcenko, R. Doneva, and K. Boykova, "Data-driven Decision Making in Higher Education Institutions: State-of-play," _International Journal of Advanced Computer Science and Applications_, vol. 14, no. 6, 2023.
[4] F. Sinlae, M. Yasir, and A. Muhajirin, "Application of Business Intelligence in the Analysis and Visualization of XYZ University Alumni Data Using the Tableau Platform," _JURTEKSI (Jurnal Teknologi dan Sistem Informasi)_, vol. 10, no. 2, pp. 209-216, 2024.
[5] Y. MZ, J. E. Bororing, S. Rahayu, and T. A. Ramadhani, "Aplikasi Dashboard Visualisasi Data Calon Mahasiswa Baru mengunakan Metabase," _Edumatic: Jurnal Pendidikan Informatika_, vol. 6, no. 1, pp. 116-125, 2022.
[6] A. Sorour and A. Atkins, "Developing BI Scorecards for Assessing Higher Education Quality Dashboards Using Human-Computer Interaction Concept: A Case Study," _Cloud Computing and Data Science_, pp. 35-53, 2024.
[7] H. S. Sharma and H. D. Joshi, "Pooling Business Intelligence and Dashboard Technology for Decisions Making in Higher Education Institutions," _Towards Excellence_, pp. 36-48, 2022.
[8] C. L. Stewart and M. A. A. Dewan, "A Systemic Mapping Study of Business Intelligence Maturity Models for Higher Education Institutions," _Computers_, vol. 11, no. 11, p. 153, 2022.
[9] E. Cardoso and X. Su, "Designing a Business Intelligence and Analytics Maturity Model for Higher Education: A Design Science Approach," _Applied Sciences_, vol. 12, no. 9, p. 4625, 2022.
[10] S. Chaudhuri, U. Dayal, and V. Narasayya, "An overview of business intelligence technology," _Communications of the ACM_, vol. 54, no. 8, pp. 88-98, 2011.
[11] L. T. Moss and S. Atre, _Business Intelligence Roadmap: The Complete Project Lifecycle for Decision-Support Applications_. Addison-Wesley Professional, 2003.
[12] R. Kimball and M. Ross, _The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling_, 3rd ed. John Wiley & Sons, 2013.
[13] G. T. Murti and S. Mulyani, "The determinant of business intelligence systems quality on Indonesian higher education information center," _Linguistics and Culture Review_, vol. 6, pp. 581-595, 2022.
[14] G. Mellyka, I. Islamiyah, and P. P. Widagdo, "Penerapan Business Intelligence dalam Dashboard Data Alumni Universitas Mulawarman," _Jutisi: Jurnal Ilmiah Teknik Informatika dan Sistem Informasi_, vol. 14, no. 1, p. 189, 2025.
[15] F. N. Hasan, "Implementasi Sistem Business Intelligence Untuk Data Penelitian di Perguruan Tinggi," _Prosiding Seminar Nasional Teknoka_, vol. 4, pp. I1-I10, 2019.
[16] A. Ady Bakri et al., "The Evaluation of PDDIKTI User Acceptance Using The Unified Theory of Acceptance and Use of Technology Approach," _Jurnal Informasi dan Teknologi_, vol. 5, no. 3, pp. 31-35, 2023.
[17] R. A. Pradipta, P. B. Wintoro, and D. Budiyanto, "Perancangan Pemodelan Basis Data Sistem Informasi Secara Konseptual dan Logikal," _Jurnal Informatika dan Teknik Elektro Terapan (JITET)_, vol. 10, no. 2, 2022.
