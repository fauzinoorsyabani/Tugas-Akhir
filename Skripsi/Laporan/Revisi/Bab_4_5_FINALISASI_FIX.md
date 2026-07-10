BAB IV
HASIL DAN PEMBAHASAN

Bab ini menyajikan hasil penelitian berupa implementasi pipeline Business Intelligence yang telah dirancang pada Bab III. Pembahasan meliputi hasil proses ETL (Extract, Transform, Load), hasil dashboard analitik interaktif, hasil visualisasi analitik, validasi konsistensi data, serta analisis yang menjawab kedua rumusan masalah penelitian. Seluruh tahapan mengacu pada keenam fase BI Roadmap (Moss dan Atre, 2003).


4.1 Hasil Proses ETL (Extract, Transform, Load)

Proses ETL yang diimplementasikan pada fase Construction (Subbab 3.5) mengolah data mentah hasil web scraping dari portal PDDikti menjadi data warehouse terstruktur. Berikut adalah hasil dari setiap tahapan ETL.


4.1.1 Hasil Tahap Extract

Tahap Extract (Subbab 3.5.1) membaca dua berkas CSV mentah hasil scraping, yaitu unsil_prodi_fresh.csv yang memuat data program studi seluruh PTN BLU secara nasional, dan unsil_univ_fresh.csv yang memuat metadata institusi perguruan tinggi. Proses pembacaan data dilakukan menggunakan pustaka Pandas pada Python, sebagaimana ditunjukkan pada Kode Program 4.1.

Kode Program 4.1 Eksekusi Tahap Extract
Sumber: Notebooks/ETL_Star_Schema.ipynb

# Baca data mentah hasil scraping
df_prodi_raw = pd.read_csv(PATH_RAW_PRODI)
df_univ_raw  = pd.read_csv(PATH_RAW_UNIV)

print(f"File prodi  : {PATH_RAW_PRODI}")
print(f"Jumlah baris: {len(df_prodi_raw)} baris")
print(f"Kolom       : {df_prodi_raw.columns.tolist()}")
print(f"File univ   : {PATH_RAW_UNIV}")
print(f"Jumlah baris: {len(df_univ_raw)} baris")

Berikut ini adalah tampilan output terminal yang dihasilkan pada saat eksekusi Kode Program 4.1 dijalankan.

[Gambar 4.1 Hasil Eksekusi Tahap Extract pada Terminal]
Sumber: Tangkapan layar output notebook ETL_Star_Schema.ipynb

Berdasarkan Gambar 4.1, data mentah dapat dimuat ke dalam memori kerja Python untuk diproses pada tahap berikutnya. Pada tahap ini, data yang dibaca masih mencakup seluruh PTN BLU secara nasional dan belum difilter ke cakupan Universitas Siliwangi, sebagaimana dijelaskan pada Subbab 3.5.1. Penyaringan cakupan dilakukan pada tahap Transform berikutnya.


4.1.2 Hasil Tahap Transform

Tahap Transform (Subbab 3.5.2) mengeksekusi enam langkah transformasi yang telah dirancang pada Kode Program 3.3. Langkah pertama adalah penyaringan cakupan (scope filtering) untuk membatasi data hanya pada Universitas Siliwangi. Kode Program 4.2 menunjukkan implementasi seluruh langkah transformasi.

Kode Program 4.2 Eksekusi Tahap Transform
Sumber: Notebooks/ETL_Star_Schema.ipynb

# Langkah 0: Filter scope — Universitas Siliwangi
df = df_prodi_raw.copy()
total_sebelum = len(df)
df = df[
    df['nama_universitas'].str.contains('Siliwangi', case=False, na=False)
].copy()
df['kode_pt'] = '002008'
print(f'Data masuk  : {total_sebelum:,} baris')
print(f'Data keluar : {len(df):,} baris | {df["nama_program_studi"].nunique()} prodi unik')

# Langkah 1: Hapus baris dengan nilai kritis kosong
before = len(df)
df = df.dropna(subset=['kode_prodi', 'tahun_pelaporan', 'rasio_dosen_mahasiswa'])
print(f"[1] Drop null kritis: {before} → {len(df)} baris")

# Langkah 2: Parsing tahun_pelaporan → semester + tahun
df[['semester', 'tahun']] = df['tahun_pelaporan'].str.split(' ', n=1, expand=True)

# Langkah 3: Konversi kolom numerik
num_cols = ['jumlah_dosen_penghitung_rasio', 'dosen_tetap',
            'dosen_tidak_tetap', 'total_dosen', 'jumlah_mahasiswa']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Langkah 4: Parsing rasio "1:X" → nilai numerik float
def parse_rasio(s):
    try:
        if pd.isna(s): return np.nan
        parts = str(s).split(':')
        return float(parts[1]) if len(parts) == 2 else np.nan
    except:
        return np.nan

df['nilai_rasio'] = df['rasio_dosen_mahasiswa'].apply(parse_rasio)

# Langkah 5: Standarisasi metadata Universitas Siliwangi
df['nama_universitas']   = 'Universitas Siliwangi'
df['status_pt_univ']     = 'PTN'
df['akreditasi_pt_univ'] = 'Unggul'

# Langkah 6: Penambahan kolom Fakultas dan Rumpun Ilmu
df['fakultas']    = df['kode_prodi'].map(FAKULTAS_MAP)
df['rumpun_ilmu'] = df['fakultas'].map(RUMPUN_MAP)

print(f"Transformasi selesai: {len(df)} baris siap diproses.")

Keenam langkah transformasi di atas diterapkan secara berurutan. Hasil ringkasan setiap langkah disajikan pada Tabel 4.1, sedangkan tampilan output terminal proses transformasi ditampilkan pada Gambar 4.2.

Tabel 4.1 Ringkasan Hasil Proses Transformasi Data

Langkah | Proses | Hasil
Langkah 0 | Scope filtering ke Universitas Siliwangi | Data terfilter dari seluruh PTN BLU nasional menjadi hanya data Universitas Siliwangi (Kode PT: 002008).
Langkah 1 | Penghapusan data tidak lengkap (missing value) | Baris data yang tidak memiliki nilai pada atribut kritis seperti kode_prodi, tahun_pelaporan, atau rasio_dosen_mahasiswa dieliminasi dari dataset.
Langkah 2 | Parsing atribut tahun_pelaporan | Kolom tahun_pelaporan dipisahkan menjadi dua atribut baru, yaitu semester (Ganjil/Genap) dan tahun (2023–2025).
Langkah 3 | Konversi tipe data numerik | Kolom numerik yang semula bertipe string dikonversi menjadi tipe numerik (float), meliputi jumlah mahasiswa, jumlah dosen tetap, dan total dosen.
Langkah 4 | Parsing rasio dosen–mahasiswa berdasarkan Persamaan 3.1 | Fungsi parse_rasio() mengekstraksi nilai numerik dari format rasio "1:X" menjadi nilai float. Nilai "-" dari sumber PDDikti dikonversi menjadi NaN.
Langkah 5 | Standarisasi metadata institusi | Informasi institusi seperti nama perguruan tinggi, status PTN BLU, dan akreditasi institusi "Unggul" distandarisasi untuk menjaga konsistensi data.
Langkah 6 | Penambahan kolom Fakultas dan Rumpun Ilmu | Setiap program studi dipetakan ke kolom fakultas dan rumpun_ilmu berdasarkan kamus data (dictionary mapping) yang didefinisikan dalam skrip run_etl.py.

[Gambar 4.2 Hasil Eksekusi Tahap Transform pada Terminal]
Sumber: Tangkapan layar output notebook ETL_Star_Schema.ipynb

Berdasarkan Gambar 4.2, seluruh enam langkah transformasi diterapkan tanpa kesalahan. Tahap ini menghasilkan 201 rekaman data yang merepresentasikan 35 program studi aktif pada lima periode pelaporan. Penurunan dari 210 baris (sesudah filter scope) menjadi 201 baris terjadi karena eliminasi baris yang tidak memiliki nilai rasio_dosen_mahasiswa, yaitu baris yang mewakili program studi tanpa mahasiswa aktif pada periode tertentu. Selisih ini telah teridentifikasi dan tidak mengindikasikan kehilangan data yang tidak diinginkan.


4.1.3 Hasil Tahap Load

Tahap Load (Subbab 3.5.3) membentuk empat tabel star schema sesuai rancangan pada Gambar 3.3, ditambah satu flat table untuk keperluan dashboard. Kode Program 4.3 menunjukkan implementasi pembentukan tabel-tabel tersebut.

Kode Program 4.3 Eksekusi Tahap Load — Pembentukan Star Schema
Sumber: Notebooks/ETL_Star_Schema.ipynb

# Dim_Waktu
dim_waktu = (
    df[['tahun_pelaporan', 'semester', 'tahun']]
    .drop_duplicates()
    .sort_values('tahun_pelaporan')
    .reset_index(drop=True)
)
dim_waktu.insert(0, 'id_waktu', dim_waktu.index + 1)
dim_waktu['tahun'] = dim_waktu['tahun'].astype(int)

# Dim_Universitas
dim_univ = pd.DataFrame([{
    'id_universitas'      : '002008',
    'nama_universitas'    : 'Universitas Siliwangi',
    'kota'                : 'Kota Tasikmalaya',
    'provinsi'            : 'Prov. Jawa Barat',
    'status_pt'           : 'PTN',
    'akreditasi_institusi': 'Unggul'
}])

# Dim_Prodi (gunakan data periode terbaru sebagai referensi atribut)
latest_period = df['tahun_pelaporan'].max()
dim_prodi = (
    df[df['tahun_pelaporan'] == latest_period]
    [['kode_prodi', 'nama_program_studi', 'jenjang', 'status_prodi', 'akreditasi_prodi']]
    .drop_duplicates(subset=['kode_prodi'])
    .sort_values('nama_program_studi')
    .reset_index(drop=True)
    .rename(columns={'kode_prodi': 'id_prodi'})
)

# Fact_Kapasitas_Pendidikan
fact = df.merge(dim_waktu[['id_waktu', 'tahun_pelaporan']], on='tahun_pelaporan', how='left')
fact_table = fact[[
    'kode_pt', 'kode_prodi', 'id_waktu',
    'jumlah_dosen_penghitung_rasio', 'dosen_tetap', 'dosen_tidak_tetap',
    'total_dosen', 'jumlah_mahasiswa', 'rasio_dosen_mahasiswa', 'nilai_rasio'
]].rename(columns={'kode_pt': 'id_universitas', 'kode_prodi': 'id_prodi'})
fact_table = fact_table.dropna(subset=['id_universitas', 'id_prodi']).reset_index(drop=True)

# Simpan ke CSV
dim_waktu.to_csv(os.path.join(PATH_OUT_SCHEMA, 'Dim_Waktu.csv'), index=False)
dim_univ.to_csv(os.path.join(PATH_OUT_SCHEMA, 'Dim_Universitas.csv'), index=False)
dim_prodi.to_csv(os.path.join(PATH_OUT_SCHEMA, 'Dim_Prodi.csv'), index=False)
fact_table.to_csv(os.path.join(PATH_OUT_SCHEMA, 'Fact_Kapasitas_Pendidikan.csv'), index=False)
print(f"Dim_Waktu: {len(dim_waktu)} | Dim_Prodi: {len(dim_prodi)} | Fact: {len(fact_table)}")

Pemilihan model star schema pada penelitian ini didasari oleh tiga pertimbangan teknis yang selaras dengan pendekatan Business Intelligence. Pertama, struktur denormalisasi pada star schema mempercepat kueri analitik karena tabel fakta hanya perlu di-join dengan tabel dimensi tanpa perlu menelusuri relasi bertingkat (Kimball dan Ross, 2013). Kedua, star schema bersifat intuitif dan mudah dipahami oleh analis bisnis yang tidak memiliki latar belakang teknis basis data, sehingga mendukung eksplorasi data secara mandiri. Ketiga, Google Looker Studio sebagai platform visualisasi yang digunakan dalam penelitian ini dioptimalkan untuk sumber data tabular (flat table atau star schema), bukan untuk basis data relasional yang dinormalisasi penuh.

Ringkasan tabel data warehouse yang terbentuk disajikan pada Tabel 4.2, sedangkan isi tabel Dim_Waktu disajikan pada Tabel 4.3.

Tabel 4.2 Hasil Pembentukan Tabel Data Warehouse Skema Bintang

No | Nama Tabel | Jenis Tabel | Jumlah Kolom | Jumlah Baris | Keterangan
1 | Fact_Kapasitas_Pendidikan | Fact Table | 10 | 201 | Merekam data kapasitas akademik setiap program studi pada setiap periode pelaporan
2 | Dim_Prodi | Dimension Table | 5 | 35 | Menyimpan informasi identitas program studi aktif
3 | Dim_Waktu | Dimension Table | 4 | 5 | Menyimpan informasi semester dan tahun pelaporan
4 | Dim_Universitas | Dimension Table | 6 | 1 | Menyimpan informasi institusi Universitas Siliwangi

Tabel 4.3 Isi Tabel Dim_Waktu

id_waktu | tahun_pelaporan | semester | tahun
1 | Ganjil 2023 | Ganjil | 2023
2 | Genap 2023 | Genap | 2023
3 | Ganjil 2024 | Ganjil | 2024
4 | Genap 2024 | Genap | 2024
5 | Ganjil 2025 | Ganjil | 2025

Selain star schema, data juga dikonsolidasikan ke dalam flat table master_looker_unsil.csv yang berisi 201 baris dan 20 kolom. Flat table ini merupakan hasil denormalisasi seluruh dimensi dan fakta ke dalam satu tabel tunggal, yang selanjutnya diunggah sebagai data source ke Google Looker Studio sebagaimana dijelaskan pada Subbab 3.6 (Gambar 3.5). Penambahan kolom fakultas dan rumpun_ilmu ditempatkan di posisi paling akhir (kolom 19–20) untuk menjaga kompatibilitas skema data source yang sudah ada di Google Sheets.

Berdasarkan hasil proses ETL, data mentah hasil web scraping ditransformasi menjadi data terstruktur yang siap digunakan untuk kebutuhan analisis dan visualisasi. Struktur data warehouse yang terbentuk menjadi fondasi bagi pembangunan dashboard analitik yang dibahas pada subbab berikutnya.


4.2 Hasil Dashboard Analitik

Dashboard yang dibangun pada fase Deployment (Subbab 3.6) terdiri atas tiga halaman utama yang dirancang untuk menjawab empat kebutuhan informasi pada fase Business Analysis (Subbab 3.3.1), yaitu: (1) distribusi mahasiswa aktif, (2) distribusi dosen, (3) nilai rasio dosen terhadap mahasiswa, dan (4) tren longitudinal kapasitas akademik. Berkas master_looker_unsil.csv diunggah ke Google Sheets dan dihubungkan sebagai data source pada Google Looker Studio, sesuai arsitektur deployment pada Gambar 3.5. Sebagai tindak lanjut atas masukan dosen pembimbing, dashboard juga dilengkapi dengan filter analisis per Fakultas dan per Rumpun Ilmu (Sains/Sosial) yang memungkinkan pemangku kepentingan menyaring data berdasarkan unit organisasi institusi, sebagaimana diuraikan pada Subbab 4.2.4.


4.2.1 Halaman Executive Overview

Halaman pertama berfungsi sebagai ringkasan eksekutif kondisi kapasitas akademik Universitas Siliwangi secara menyeluruh. Tampilan halaman ini dirancang agar pimpinan institusi dapat memperoleh gambaran situasi kapasitas dalam satu pandang (single-glance overview) tanpa perlu menelusuri data secara manual. Gambar 4.3 di bawah ini menyajikan tampilan lengkap halaman Executive Overview.

[Gambar 4.3 Tampilan Halaman Executive Overview Dashboard]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-07-06 110630.png

Berdasarkan Gambar 4.3, halaman Executive Overview menampilkan identitas dashboard secara formal pada bagian header dengan judul "Dashboard Kapasitas Akademik – Universitas Siliwangi / Executive Overview" disertai logo resmi institusi. Halaman ini terdiri atas empat komponen utama. Komponen pertama adalah filter interaktif berjenis drop-down list yang ditempatkan pada bagian atas dashboard, meliputi filter Tahun Pelaporan (Ganjil 2023 hingga Ganjil 2025), filter Jenjang (S1, S2, S3, D3, D4, Profesi), filter Nama Program Studi, dan filter Fakultas. Ketika salah satu filter diubah, seluruh komponen visualisasi pada halaman diperbarui secara real-time sesuai parameter yang dipilih (Negash, 2004).

Gambar 4.4 di bawah ini menyajikan tampilan komponen filter dengan kondisi dropdown sedang terbuka, yang menggambarkan pilihan-pilihan yang tersedia bagi pengguna.

[Gambar 4.4 Tampilan Filter Tahun Pelaporan dengan Dropdown Terbuka]
Sumber: Tangkapan layar Google Looker Studio

Berdasarkan Gambar 4.4, filter tahun pelaporan menampilkan lima pilihan periode yang sesuai dengan rentang data pada data warehouse, yaitu Ganjil 2023, Genap 2023, Ganjil 2024, Genap 2024, dan Ganjil 2025. Komponen kedua adalah empat scorecard yang menampilkan Key Performance Indicator (KPI) agregat institusi, sebagaimana disajikan pada Tabel 4.4.

Tabel 4.4 Nilai Scorecard Dashboard Looker Studio

No | Scorecard | Nilai | Keterangan
1 | Total Mahasiswa | 101.401 | Jumlah kumulatif mahasiswa aktif dari seluruh program studi dan periode pelaporan (18.702 + 17.141 + 23.357 + 18.232 + 23.969).
2 | Total Dosen | 2.461 | Jumlah kumulatif dosen penghitung rasio dari seluruh program studi pada seluruh periode pelaporan.
3 | Rata-Rata Rasio | 165 | Nilai rata-rata rasio dosen terhadap mahasiswa yang dihitung dari seluruh baris data aktif. Data dengan nilai "-" tidak diperhitungkan dalam proses agregasi.
4 | Jumlah Prodi | 35 | Total program studi yang tercatat dalam data warehouse Universitas Siliwangi.

Komponen ketiga adalah line chart tren rasio dosen terhadap mahasiswa tingkat institusi yang menampilkan perubahan nilai rasio antarperiode. Komponen keempat adalah pie chart distribusi prodi per jenjang, yang menunjukkan bahwa 89,7% program studi berada pada jenjang S1, mengindikasikan dominasi program pendidikan sarjana di Universitas Siliwangi. Pada bagian bawah halaman terdapat horizontal bar chart yang menyajikan perbandingan jumlah mahasiswa antarprogram studi secara visual.


4.2.2 Halaman Analisis Detail Per Program Studi

Halaman kedua dirancang untuk menyediakan analisis komparatif antarprogram studi dengan granularitas yang lebih rinci dibandingkan halaman Executive Overview. Tujuannya adalah membantu pimpinan mengidentifikasi program studi mana yang memerlukan perhatian lebih lanjut berdasarkan nilai rasio dan pola longitudinalnya. Gambar 4.5 di bawah ini menyajikan tampilan halaman tersebut.

[Gambar 4.5 Tampilan Halaman Analisis Detail Per Program Studi]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-07-06 110715.png

Berdasarkan Gambar 4.5, halaman Analisis Detail Per Program Studi menampilkan header berwarna hijau dengan logo institusi dan judul halaman yang mendeskripsikan fungsi utamanya. Komponen utama halaman ini adalah tabel pivot (heatmap) yang menampilkan matriks nama_program_studi × tahun_pelaporan dengan metrik nilai_rasio. Gradasi warna pada sel tabel memberikan indikasi visual: warna yang lebih gelap menunjukkan rasio yang lebih tinggi (potensi kelebihan beban), sedangkan warna yang lebih terang menunjukkan rasio yang lebih rendah.

Berdasarkan tabel heatmap tersebut, teridentifikasi program studi dengan rasio tinggi secara konsisten pada setiap periode, sebagaimana disajikan pada Tabel 4.3.

Tabel 4.3 Rangkuman 10 Program Studi dengan Rasio Tertinggi — Periode Ganjil 2025

No | Program Studi | Jenjang | Dosen Penghitung Rasio | Mahasiswa Aktif | Nilai Rasio | Kategori
1 | Pendidikan Sejarah | S1 | 13 | 702 | 1:54,0 | Melampaui Batas (Soshum)
2 | Pendidikan Masyarakat | S1 | 12 | 611 | 1:50,9 | Melampaui Batas (Soshum)
3 | Manajemen | S1 | 37 | 1.772 | 1:47,9 | Melampaui Batas (Soshum)
4 | Akuntansi | S1 | 31 | 1.417 | 1:45,7 | Melampaui Batas (Soshum)
5 | Ilmu Politik | S1 | 21 | 923 | 1:44,0 | Zona Waspada
6 | Pendidikan Ekonomi | S1 | 15 | 633 | 1:42,2 | Zona Waspada
7 | Pendidikan Geografi | S1 | 15 | 619 | 1:41,3 | Zona Waspada
8 | Pendidikan Jasmani | S1 | 37 | 1.492 | 1:40,3 | Zona Waspada
9 | Ekonomi Pembangunan | S1 | 35 | 1.375 | 1:39,3 | Normal
10 | Ekonomi Syari'ah | S1 | 21 | 809 | 1:38,5 | Normal

Catatan: Batas ambang yang digunakan adalah batas Soshum (R > 45) berdasarkan Permendikbud Nomor 3 Tahun 2020, yaitu batas paling longgar untuk rumpun ilmu sosial dan humaniora. Kolom "Dosen Penghitung Rasio" mengacu pada jumlah_dosen_penghitung_rasio dari PDDikti, bukan total_dosen, sesuai formula pada Persamaan 3.1.

Komponen kedua pada halaman ini adalah scatter plot (bubble chart) yang memetakan setiap program studi berdasarkan jumlah_mahasiswa (sumbu X) dan nilai_rasio (sumbu Y). Program studi pada kuadran kanan atas (mahasiswa banyak, rasio tinggi) merupakan titik kritis yang membutuhkan perhatian manajemen. Berdasarkan scatter plot tersebut, Pendidikan Masyarakat (611 mahasiswa, rasio 1:50,9) dan Akuntansi S1 (1.417 mahasiswa, rasio 1:45,7) merupakan dua program studi dengan kombinasi jumlah mahasiswa yang signifikan sekaligus rasio yang melampaui batas standar DIKTI.


4.2.3 Halaman Tren Longitudinal dan Monitoring

Halaman ketiga dirancang untuk memfasilitasi analisis tren rasio secara kronologis (time-series) per program studi, menjawab kebutuhan informasi keempat pada Subbab 3.3.1. Melalui halaman ini, pimpinan institusi dapat mengamati apakah kondisi rasio suatu program studi membaik, memburuk, atau bersifat stagnan dari satu periode ke periode berikutnya. Gambar 4.6 di bawah ini menyajikan tampilan halaman tersebut.

[Gambar 4.6 Tampilan Halaman Tren Longitudinal dan Monitoring]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-07-06 110736.png

Berdasarkan Gambar 4.6, halaman Tren Longitudinal dan Monitoring menampilkan header berwarna hijau dengan judul halaman yang mencerminkan fungsinya. Halaman ini memuat stacked bar chart yang menampilkan perbandingan nilai rasio antarprogram studi untuk setiap periode pelaporan (Ganjil 2023 hingga Ganjil 2025). Setiap segmen warna merepresentasikan satu program studi, sehingga memudahkan identifikasi program studi yang secara konsisten mendominasi nilai rasio tertinggi pada setiap periode. Pada bagian kanan bawah halaman terdapat tabel ranking yang menampilkan peringkat program studi berdasarkan akumulasi nilai rasio, dilengkapi data bar untuk memperkuat representasi visual. Kombinasi kedua visualisasi tersebut memungkinkan pemangku kepentingan melakukan pemantauan perkembangan rasio secara longitudinal serta membandingkan kondisi antarprogram studi pada berbagai periode pelaporan.


4.2.4 Filter Analisis Per Fakultas dan Per Rumpun Ilmu

Sebagai tindak lanjut atas masukan dosen pembimbing (poin revisi kelima), dashboard dilengkapi dengan dua filter tambahan yang memungkinkan analisis data berdasarkan unit organisasi institusi, yaitu filter Fakultas dan filter Rumpun Ilmu. Kedua filter ini dihasilkan dari penambahan kolom fakultas dan rumpun_ilmu pada proses ETL (Langkah 6 pada Subbab 4.1.2), yaitu setiap program studi dipetakan ke fakultas dan rumpun ilmunya secara otomatis berdasarkan kamus data (dictionary mapping) yang dikodekan di dalam skrip run_etl.py. Pemetaan lengkap seluruh program studi ke fakultas dan rumpun ilmu disajikan pada Tabel 4.4.

Tabel 4.4 Pemetaan Fakultas dan Rumpun Ilmu Program Studi Universitas Siliwangi

Fakultas | Rumpun Ilmu | Contoh Program Studi
Fakultas Teknik | Sains | Informatika, Teknik Sipil, Sistem Informasi
Fakultas Pertanian | Sains | Agroteknologi, Agribisnis, Peternakan
Fakultas Ilmu Kesehatan | Sains | Kesehatan Masyarakat, Keperawatan
Fakultas Keguruan dan Ilmu Pendidikan | Sosial | Pend. Matematika, Pend. Sejarah, Pend. Bahasa Indonesia
Fakultas Ekonomi dan Bisnis | Sosial | Manajemen, Akuntansi, Ekonomi Pembangunan
Fakultas Ilmu Sosial dan Ilmu Politik | Sosial | Ilmu Politik, Administrasi Publik

Dengan adanya filter Fakultas, pemangku kepentingan dapat membandingkan kondisi kapasitas akademik antarfakultas dalam satu tampilan. Sebagai contoh, Dekan Fakultas Ekonomi dan Bisnis (FEB) dapat menyaring dashboard hanya untuk program studi di bawah unit kerjanya, kemudian melihat nilai rasio, tren longitudinal, dan kategori status (Normal/Zona Waspada/Melampaui Batas) tanpa perlu menyaring data secara manual. Filter Rumpun Ilmu (Sains/Sosial) memungkinkan analisis komparatif beban mengajar antarrumpun sebagaimana dibahas pada Subbab 4.5.3. Secara teknis, implementasi filter ini dilakukan dengan menambahkan komponen Control Filter bertipe Drop-down List pada antarmuka Looker Studio dan menghubungkannya ke kolom fakultas dan rumpun_ilmu pada data source.


4.3 Hasil Visualisasi Analitik

Selain dashboard interaktif berbasis Looker Studio, penelitian ini menghasilkan visualisasi analitik yang lebih mendalam menggunakan pustaka Matplotlib dan Seaborn pada Python (notebook Dashboard_Visualisasi.ipynb). Visualisasi ini digunakan untuk kebutuhan analisis yang memerlukan jenis grafik khusus — heatmap matriks penuh, multi-line chart komparatif, dan grafik dengan garis batas regulasi — yang tidak tersedia secara langsung pada Looker Studio. Pendekatan dual-output ini memungkinkan analisis yang lebih komprehensif, sejalan dengan rekomendasi Sharma dan Joshi (2022) mengenai pemanfaatan teknologi dashboard untuk pengambilan keputusan di institusi pendidikan tinggi.

Mengenai konsistensi angka antara Looker Studio dan Python: kedua platform menggunakan sumber data yang sama, yaitu master_looker_unsil.csv. Python menggunakan fungsi mean() yang secara default mengabaikan NaN (skipna=True), sedangkan Looker Studio mengabaikan sel kosong dalam perhitungan metrik agregat secara otomatis. Oleh karena itu, nilai rata-rata rasio yang ditampilkan keduanya konsisten.


4.3.1 Dashboard Ringkasan Analitik

Dashboard ringkasan analitik merupakan visualisasi pertama yang dihasilkan dari notebook Dashboard_Visualisasi.ipynb. Visualisasi ini dirancang untuk menyajikan gambaran menyeluruh kondisi kapasitas akademik Universitas Siliwangi dalam satu kanvas terintegrasi. Gambar 4.7 di bawah ini menyajikan tampilan dashboard ringkasan dimaksud.

[Gambar 4.7 Dashboard Ringkasan Analitik Rasio Dosen:Mahasiswa Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/dashboard_final.png

Berdasarkan Gambar 4.7, dashboard ringkasan terdiri atas lima panel visualisasi yang disusun dalam satu tampilan terpadu. Panel pertama (Tren Rata-Rata Rasio Institusi) menampilkan rata-rata rasio seluruh institusi per periode dengan dua garis batas acuan: garis merah putus-putus untuk batas DIKTI rumpun Soshum (1:45) dan garis oranye titik-titik untuk batas rumpun Saintek (1:30). Panel kedua dan ketiga masing-masing menampilkan total mahasiswa aktif dan total dosen per semester dalam bentuk bar chart. Panel keempat menampilkan 10 program studi dengan rasio tertinggi pada periode Ganjil 2025, sedangkan panel kelima menyajikan heatmap ringkasan untuk 15 program studi dengan rasio tertinggi. Kombinasi kelima panel ini memungkinkan identifikasi tren, perbandingan antarprogram studi, serta pemantauan rasio secara lebih komprehensif dibandingkan penyajian data dalam bentuk tabel.


4.3.2 Tren Agregat Rasio Institusi

Visualisasi tren agregat institusi menampilkan perubahan rata-rata rasio dosen terhadap mahasiswa Universitas Siliwangi selama lima periode pelaporan dalam satu grafik tunggal yang dapat diinterpretasikan secara longitudinal. Kode Program 4.4 menunjukkan implementasi visualisasi tersebut, dan Gambar 4.8 menyajikan hasilnya.

Kode Program 4.4 Visualisasi Tren Institusi
Sumber: Notebooks/Dashboard_Visualisasi.ipynb

# Agregasi institusi per periode
inst = df.groupby('tahun_pelaporan', observed=True).agg(
    total_mahasiswa=('jumlah_mahasiswa','sum'),
    total_dosen=('total_dosen','sum'),
    rata_rasio=('nilai_rasio','mean')
).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
ax = axes[0]
ax.plot(inst['tahun_pelaporan'], inst['rata_rasio'],
        marker='o', color=COLORS[0], linewidth=2.5, markersize=8)
ax.axhline(y=45, color='red', linestyle='--', linewidth=1.5, label='Batas Soshum (1:45)')
ax.axhline(y=30, color='orange', linestyle=':', linewidth=1.5, label='Batas Saintek (1:30)')
ax.set_title('Tren Rata-Rata Rasio Dosen:Mahasiswa')
ax.legend()
plt.savefig(os.path.join(PATH_VIZ, 'viz_institusi.png'), bbox_inches='tight', dpi=150)

[Gambar 4.8 Tren Agregat Rasio Dosen:Mahasiswa — Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/viz_institusi.png

Berdasarkan Gambar 4.8, tren rasio agregat institusi Universitas Siliwangi selama lima periode pelaporan relatif stabil. Data aktual yang menjadi dasar grafik tersebut disajikan pada Tabel 4.5.

Tabel 4.5 Data Aktual Tren Institusi Universitas Siliwangi

Periode | Total Mahasiswa | Total Dosen | Rata-Rata Rasio
Ganjil 2023 | 18.702 | 431 | 24,91
Genap 2023 | 17.141 | 431 | 24,78
Ganjil 2024 | 23.357 | 526 | 24,58
Genap 2024 | 18.232 | 524 | 22,84
Ganjil 2025 | 23.969 | 549 | 24,09

Berdasarkan Tabel 4.5 dan Gambar 4.8, rata-rata rasio dosen terhadap mahasiswa berada pada rentang 22,84 hingga 24,91 sepanjang periode pengamatan. Nilai ini berada di bawah kedua garis batas acuan, yaitu batas Saintek (1:30) maupun batas Soshum (1:45) sebagaimana ditetapkan Permendikbud Nomor 3 Tahun 2020. Pertumbuhan jumlah mahasiswa sebesar 28,2% (dari 18.702 menjadi 23.969) selaras dengan pertumbuhan jumlah dosen sebesar 27,4% (dari 431 menjadi 549), yang menjelaskan mengapa rasio agregat institusi relatif tidak mengalami perubahan yang substansial selama lima periode tersebut.


4.3.3 Heatmap Rasio Per Program Studi dan Semester

Heatmap rasio merupakan visualisasi yang menampilkan seluruh kombinasi program studi dan periode pelaporan dalam satu matriks berwarna, sehingga pola longitudinal pada setiap program studi dapat diamati sekaligus. Kode Program 4.5 menunjukkan implementasinya, dan Gambar 4.9 menyajikan hasilnya.

Kode Program 4.5 Heatmap Rasio per Program Studi × Semester
Sumber: Notebooks/Dashboard_Visualisasi.ipynb

# Heatmap rasio per prodi × per semester
pivot = df.pivot_table(
    index='nama_program_studi',
    columns='tahun_pelaporan',
    values='nilai_rasio',
    aggfunc='mean',
    observed=True
)
pivot = pivot.reindex(columns=PERIOD_ORDER)
pivot = pivot.sort_values(PERIOD_ORDER[-1], ascending=False)

fig, ax = plt.subplots(figsize=(12, max(8, len(pivot)*0.4)))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.3, cbar_kws={'label':'Nilai Rasio (1:x)'},
            ax=ax, vmin=0, vmax=45)
ax.set_title('Heatmap Rasio Dosen:Mahasiswa per Program Studi × Semester')
plt.savefig(os.path.join(PATH_VIZ, 'heatmap_prodi_semester.png'), bbox_inches='tight', dpi=150)

[Gambar 4.9 Heatmap Rasio Dosen:Mahasiswa per Program Studi dan Semester]
Sumber: Output Python (Matplotlib/Seaborn) — file Outputs/Visualizations/heatmap_prodi_semester.png

Berdasarkan Gambar 4.9, heatmap menggunakan skala warna RdYlGn_r (merah untuk rasio tinggi, hijau untuk rasio rendah) dengan rentang vmin=0 hingga vmax=45. Program studi dengan rasio melebihi 45 ditampilkan dengan warna merah penuh (saturasi maksimum). Pola longitudinal beberapa program studi terpilih dirangkum pada Tabel 4.6.

Tabel 4.6 Rangkuman Pola Longitudinal Program Studi Terpilih

Program Studi | Ganjil 2023 | Genap 2023 | Ganjil 2024 | Genap 2024 | Ganjil 2025 | Pola
Pendidikan Masyarakat | 47,6 | 57,4 | 58,5 | 50,8 | 50,9 | Konsisten tinggi (selalu >45)
Pendidikan Sejarah | 48,7 | 35,2 | 55,0 | 30,9 | 54,0 | Fluktuatif (naik-turun ekstrem)
Manajemen | >40 | >40 | >40 | >40 | 47,9 | Tren meningkat
Akuntansi | >33 | >35 | >40 | >35 | 45,7 | Mendekati batas
Sains Data | NaN | NaN | NaN | NaN | NaN | Belum ada mahasiswa terdaftar

Berdasarkan Tabel 4.6, Program Studi Pendidikan Masyarakat menunjukkan rasio yang secara konsisten melampaui batas Soshum (1:45) pada seluruh periode pengamatan, mengindikasikan adanya permasalahan struktural yang belum menunjukkan perbaikan organik. Program Studi Pendidikan Sejarah menunjukkan pola fluktuatif yang cukup besar antarperiode, yang dipengaruhi variasi jumlah dosen penghitung rasio pada setiap semester.


4.3.4 Perbandingan Rasio Per Program Studi Periode Terbaru

Bar chart perbandingan rasio menyajikan posisi relatif setiap program studi terhadap garis batas DIKTI pada periode pelaporan terbaru (Ganjil 2025), sehingga memudahkan identifikasi program studi yang memerlukan tindakan prioritas. Kode Program 4.6 menunjukkan implementasinya, dan Gambar 4.10 menyajikan hasilnya.

Kode Program 4.6 Bar Chart Perbandingan Rasio Periode Ganjil 2025
Sumber: Notebooks/Dashboard_Visualisasi.ipynb

latest = PERIOD_ORDER[-1]  # 'Ganjil 2025'
df_latest = df[df['tahun_pelaporan']==latest].copy()
df_latest = df_latest.groupby('nama_program_studi', observed=True)['nilai_rasio'].mean().reset_index()
df_latest = df_latest.sort_values('nilai_rasio', ascending=True)

colors = ['#d62728' if v > 45 else '#ff7f0e' if v > 30 else '#1f77b4'
          for v in df_latest['nilai_rasio']]
bars = ax.barh(df_latest['nama_program_studi'], df_latest['nilai_rasio'], color=colors)
ax.axvline(x=45, color='red', linestyle='--', linewidth=2, label='Batas Soshum (1:45)')
ax.axvline(x=30, color='orange', linestyle=':', linewidth=2, label='Batas Saintek (1:30)')
plt.savefig(os.path.join(PATH_VIZ, 'bar_rasio_prodi_terbaru.png'), bbox_inches='tight', dpi=150)

[Gambar 4.10 Perbandingan Rasio per Program Studi — Periode Ganjil 2025]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/bar_rasio_prodi_terbaru.png

Berdasarkan Gambar 4.10, terdapat tiga program studi yang nilai rasionya melampaui garis batas Soshum (1:45): Pendidikan Sejarah (1:54,0), Pendidikan Masyarakat (1:50,9), dan Akuntansi (1:45,7). Warna merah pada batang grafik mengindikasikan kondisi melampaui batas Soshum, warna oranye mengindikasikan rasio di atas batas Saintek (1:30) namun di bawah batas Soshum (zona waspada), dan warna biru mengindikasikan kondisi normal. Visualisasi ini memudahkan identifikasi prioritas intervensi manajemen berdasarkan tingkat urgensi kapasitas akademik.


4.3.5 Tren Perbandingan Prodi Tertinggi dan Terendah

Grafik tren perbandingan menampilkan kontras antara program studi dengan beban rasio tertinggi dan terendah secara longitudinal, sehingga perbedaan pola perkembangan antarkelompok dapat diamati secara bersamaan. Kode Program 4.7 menunjukkan implementasinya, dan Gambar 4.11 menyajikan hasilnya.

Kode Program 4.7 Line Chart Tren Prodi Ekstrem
Sumber: Notebooks/Dashboard_Visualisasi.ipynb

top5 = df_latest.nlargest(5, 'nilai_rasio')['nama_program_studi'].tolist()
bot5 = df_latest.nsmallest(5, 'nilai_rasio')['nama_program_studi'].tolist()
df_sel = df[df['nama_program_studi'].isin(top5 + bot5)].copy()
df_sel = df_sel.groupby(['nama_program_studi','tahun_pelaporan'], observed=True)['nilai_rasio'].mean().reset_index()
# Panel kiri: 5 prodi rasio tertinggi; Panel kanan: 5 prodi rasio terendah
# Garis batas DIKTI ganda ditambahkan pada kedua panel
plt.savefig(os.path.join(PATH_VIZ, 'line_tren_top5_bot5.png'), bbox_inches='tight', dpi=150)

[Gambar 4.11 Tren Rasio — Perbandingan 5 Prodi Tertinggi vs 5 Prodi Terendah]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/line_tren_top5_bot5.png

Berdasarkan Gambar 4.11, terdapat perbedaan pola yang nyata antara kelompok program studi dengan rasio tertinggi dan terendah. Program studi pada kelompok tertinggi cenderung berada pada atau melampaui garis batas Soshum (1:45) pada beberapa periode, sementara kelompok terendah memiliki nilai rasio yang jauh di bawah kedua garis batas. Disparitas ini mengonfirmasi bahwa distribusi mahasiswa dan dosen antarprogram studi tidak merata, sehingga analisis pada level agregat institusi saja tidak memadai untuk menggambarkan kondisi kapasitas akademik secara menyeluruh.


4.3.6 Tren Total Mahasiswa dan Tren Total Dosen

Dua grafik terpisah berikut menyajikan perkembangan jumlah mahasiswa aktif dan jumlah dosen secara individual, sehingga pola pertumbuhan masing-masing komponen rasio dapat diamati secara independen.

[Gambar 4.12 Tren Total Mahasiswa Aktif Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/grafik_mhs_unsil.png

[Gambar 4.13 Tren Total Dosen Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/grafik_dosen_unsil.png

Berdasarkan Gambar 4.12 dan Gambar 4.13, jumlah mahasiswa aktif mengalami fluktuasi selama periode pengamatan dengan nilai tertinggi pada Ganjil 2025 (23.969 mahasiswa). Pola ini mencerminkan karakteristik siklus akademik di mana semester ganjil umumnya memiliki jumlah mahasiswa lebih tinggi karena masuknya mahasiswa baru. Jumlah dosen menunjukkan tren peningkatan bertahap dari 431 dosen (Ganjil 2023) menjadi 549 dosen (Ganjil 2025), dengan pertumbuhan sebesar 27,4%. Pertumbuhan dosen yang relatif sebanding dengan pertumbuhan mahasiswa (28,2%) menjelaskan mengapa rasio agregat institusi tetap stabil sepanjang periode pengamatan.


4.4 Validasi Data

Validasi data pada penelitian ini dilakukan melalui tiga tahap yang saling melengkapi: validasi sebelum dan sesudah proses ETL, validasi konsistensi data antarsemester dalam tahun akademik yang sama, serta validasi konsistensi antara data warehouse dan dashboard. Pendekatan validasi berlapis ini memastikan integritas data di setiap tahapan pipeline BI, selaras dengan prinsip sanity check pada implementasi ETL (Moss dan Atre, 2003).


4.4.1 Validasi Data Sebelum dan Sesudah ETL

Validasi pertama membandingkan jumlah data sebelum proses ETL (data mentah seluruh PTN BLU secara nasional) dengan jumlah data sesudah ETL (data yang telah difilter dan dibersihkan untuk Universitas Siliwangi). Perbandingan ini memastikan tidak ada data yang hilang secara tidak disengaja selama proses transformasi. Hasil validasi disajikan pada Tabel 4.5.

Tabel 4.5 Validasi Jumlah Data Sebelum dan Sesudah Proses ETL

Tahap | Cakupan | Jumlah Baris | Jumlah Prodi Unik | Keterangan
Sebelum ETL (Raw) | Seluruh PTN BLU Nasional | >5.000 | >500 | Data mentah PDDikti — belum difilter
Sesudah Filter Scope | Universitas Siliwangi | 210 | 42 | Langkah 0: filter nama_universitas mengandung "Siliwangi"
Sesudah Drop Null | Universitas Siliwangi | 201 | 35 aktif | Langkah 1: eliminasi baris tanpa kode_prodi/tahun_pelaporan/rasio
Hasil Akhir (Clean) | Universitas Siliwangi | 201 | 35 aktif | Siap masuk warehouse; prodi non-aktif tetap tercatat di Dim_Prodi

Berdasarkan Tabel 4.5, proses ETL mereduksi data dari skala nasional (lebih dari 5.000 baris) menjadi 201 baris yang hanya mencakup Universitas Siliwangi. Penurunan dari 210 baris (sesudah filter scope) menjadi 201 baris (sesudah drop null) disebabkan eliminasi 9 baris yang tidak memiliki nilai rasio_dosen_mahasiswa, yaitu baris yang merepresentasikan program studi tanpa mahasiswa aktif pada periode tertentu. Selisih ini telah teridentifikasi dan tidak mengindikasikan kehilangan data yang tidak diinginkan.


4.4.2 Validasi Data Antarsemester

Validasi kedua membandingkan data antara semester Ganjil dan Genap pada tahun akademik yang sama (Ganjil 2023 dibandingkan dengan Genap 2023, dan Ganjil 2024 dibandingkan dengan Genap 2024). Tujuannya adalah mengidentifikasi fluktuasi jumlah mahasiswa yang tidak wajar antarsemester, yang dapat mengindikasikan kesalahan pelaporan pada portal PDDikti. Sampel hasil validasi disajikan pada Tabel 4.6.

Tabel 4.6 Sampel Hasil Validasi Antarsemester — Ganjil 2023 vs Genap 2023

Program Studi | Mahasiswa Ganjil 2023 | Mahasiswa Genap 2023 | Selisih | Status
Manajemen S1 | 1.648 | 1.739 | +91 | Normal
Informatika S1 | 746 | 745 | -1 | Normal
Pendidikan Masyarakat | 566 | 611 | +45 | Normal
Ilmu Politik | 596 | 614 | +18 | Normal
Pendidikan Sejarah | 651 | 716 | +65 | Normal
Seluruh prodi lainnya | — | — | <(+/-)200 | Normal — tidak ada deviasi signifikan

Berdasarkan validasi antarsemester pada Tabel 4.6, terdapat satu program studi dengan deviasi jumlah mahasiswa yang cukup besar, yaitu Program Studi Pendidikan Profesi Guru dengan selisih 624 mahasiswa antara Ganjil 2023 (1.327 mahasiswa) dan Genap 2023 (703 mahasiswa). Deviasi ini bukan mengindikasikan kesalahan data, melainkan mencerminkan karakteristik khusus program PPG yang penerimaannya bersifat gelombang (batch) — tidak mengikuti siklus semester reguler seperti program S1. Selain temuan tersebut, seluruh program studi lainnya (34 prodi) menunjukkan deviasi yang wajar dan tidak melampaui batas toleransi 200 mahasiswa.


4.4.3 Validasi Konsistensi Data — Dashboard vs Data Warehouse

Sebagaimana ditetapkan pada fase Deployment (Subbab 3.6), validasi konsistensi data dilakukan dengan membandingkan nilai yang ditampilkan pada dashboard Looker Studio dengan nilai pada berkas CSV data warehouse. Validasi ini memastikan tidak terdapat distorsi data selama proses integrasi (Moss dan Atre, 2003). Hasil validasi disajikan pada Tabel 4.7.

Tabel 4.7 Hasil Validasi Konsistensi Data — Dashboard vs Data Warehouse

No | Program Studi | Periode | Mahasiswa (DW) | Dosen Penghitung Rasio (DW) | Rasio DW (Persamaan 3.1) | Rasio Dashboard | Konsistensi
1 | Sistem Informasi | Ganjil 2025 | 363 | 21 | 17,29 | 17,29 | Konsisten
2 | Akuntansi | Ganjil 2025 | 1.417 | 31 | 45,71 | 45,71 | Konsisten
3 | Manajemen S1 | Ganjil 2025 | 1.772 | 37 | 47,89 | 47,89 | Konsisten
4 | Pendidikan Sejarah | Ganjil 2025 | 702 | 13 | 54,00 | 54,00 | Konsisten
5 | Informatika | Ganjil 2023 | 746 | 26 | 28,69 | 28,69 | Konsisten
6 | Agribisnis S1 | Genap 2024 | 684 | 34 | 20,12 | 20,12 | Konsisten
7 | Pend. Matematika S1 | Ganjil 2024 | 715 | 30 | 23,83 | 23,83 | Konsisten

Berdasarkan Tabel 4.7, seluruh sampel validasi menunjukkan tingkat konsistensi 100% antara nilai pada data warehouse dan nilai yang ditampilkan pada dashboard Looker Studio. Hal ini mengonfirmasi bahwa proses integrasi data dari berkas CSV ke Google Looker Studio melalui Google Sheets tidak menghasilkan distorsi, serta logika kalkulasi rasio berdasarkan Persamaan 3.1 terimplementasi secara akurat pada seluruh tahapan pipeline BI.


4.5 Analisis dan Pembahasan


4.5.1 Analisis Kondisi Kapasitas Akademik (Menjawab Rumusan Masalah 1)

Rumusan masalah pertama (Subbab 1.2) menanyakan: "Bagaimana kondisi kapasitas akademik Universitas Siliwangi sebagai Perguruan Tinggi Negeri Badan Layanan Umum (PTN BLU) berdasarkan tren rasio dosen terhadap mahasiswa per program studi menggunakan data agregat PDDikti secara longitudinal?"

Berdasarkan hasil analisis data selama 5 periode pelaporan terhadap 35 program studi, diperoleh temuan sebagai berikut.

Secara agregat, rata-rata rasio dosen terhadap mahasiswa Universitas Siliwangi berada pada rentang 22,8 hingga 24,9 per semester. Sebagai acuan penilaian, Permendikbud Nomor 3 Tahun 2020 tentang Standar Nasional Pendidikan Tinggi menetapkan dua batas ambang rasio yang berbeda berdasarkan rumpun ilmu: (1) 1:30 untuk program studi rumpun ilmu sains, teknologi, dan rekayasa (Saintek), dan (2) 1:45 untuk program studi rumpun ilmu sosial dan humaniora (Soshum). Nilai rata-rata rasio agregat institusi yang berada pada rentang 22,8–24,9 memenuhi kedua batas ambang tersebut, sehingga secara keseluruhan kapasitas akademik institusi berada dalam kategori memadai. Pertumbuhan jumlah mahasiswa sebesar 28,2% (dari 18.702 menjadi 23.969) selaras dengan pertumbuhan jumlah dosen sebesar 27,4% (dari 431 menjadi 549), menjaga stabilitas rasio agregat selama periode pengamatan.

Namun, analisis pada level program studi mengungkapkan disparitas yang signifikan apabila ditinjau berdasarkan batas ambang per rumpun ilmu. Apabila menggunakan batas Sosial/Humaniora (1:45) sebagai acuan, terdapat tiga program studi yang melampaui batas pada Ganjil 2025: Pendidikan Sejarah (1:54,0), Pendidikan Masyarakat (1:50,9), dan Akuntansi (1:45,7). Apabila menggunakan batas Sains/Teknologi (1:30) sebagai acuan, program studi rumpun sains seperti Kesehatan Masyarakat (1:37,9) juga melampaui batas yang relevan bagi rumpunnya. Enam program studi berada dalam zona waspada berdasarkan batas Soshum (rasio 35–45): Ilmu Politik (1:44,0), Pendidikan Ekonomi (1:42,2), Ekonomi Pembangunan (1:39,3), Ekonomi Syari'ah (1:38,5), Kesehatan Masyarakat (1:37,9), dan Pendidikan Bahasa Indonesia (1:37,6). Sebaliknya, 10 program studi memiliki rasio sangat rendah (<10), umumnya merupakan program studi baru atau pascasarjana yang belum memiliki mahasiswa dalam jumlah besar.

Analisis longitudinal menunjukkan bahwa Pendidikan Masyarakat memiliki rasio yang konsisten melampaui batas pada tiga dari lima periode (47,6 → 57,4 → 58,5 → 50,8 → 50,9), mengindikasikan adanya permasalahan struktural yang belum menunjukkan perbaikan organik yang signifikan. Pendidikan Sejarah menunjukkan pola fluktuatif (48,7 → 35,2 → 55,0 → 30,9 → 54,0) yang dipengaruhi variasi jumlah dosen penghitung rasio antarsemester. Akuntansi menunjukkan tren meningkat dari Ganjil 2023 (33,6) hingga Ganjil 2025 (45,7), mengindikasikan pertumbuhan mahasiswa yang tidak diimbangi penambahan dosen secara proporsional.

Disparitas ini menegaskan bahwa pendekatan Business Intelligence dengan kemampuan analisis drill-down ke level program studi sangat diperlukan, karena analisis pada level agregat institusi saja berpotensi menyembunyikan permasalahan pada sub-tingkat struktural (Kimball dan Ross, 2013).


4.5.2 Evaluasi Sistem BI sebagai Pendukung DSS (Menjawab Rumusan Masalah 2)

Rumusan masalah kedua (Subbab 1.2) menanyakan: "Bagaimana sistem Business Intelligence berbasis data warehouse dan dashboard analitik dapat mengatasi permasalahan penyajian data yang masih bersifat statis dan deskriptif, serta mendukung Decision Support System (DSS) secara terstruktur?"

Sebagaimana diposisikan pada Subbab 2.1.4, DSS dalam penelitian ini bukan merupakan sistem tersendiri, melainkan kerangka pendukung pengambilan keputusan yang memanfaatkan hasil analisis dan visualisasi BI. Sistem yang dibangun mendukung kerangka DSS melalui empat mekanisme sebagai berikut.

Pertama, transformasi data statis menjadi informasi yang dinamis. Proses ETL mengubah data agregat PDDikti yang sebelumnya bersifat statis dan deskriptif (Astuti dkk., 2024) menjadi data warehouse terstruktur yang mendukung analisis multidimensi — slice-and-dice, drill-down, dan roll-up — yang tidak dimungkinkan oleh format data mentah PDDikti.

Kedua, penyajian visual yang mendukung proses kognitif pengambil keputusan. Dashboard interaktif menyajikan informasi melalui elemen visual (grafik batang, grafik garis, heatmap, scatter plot, dan scorecard) yang secara kognitif lebih mudah diproses dibandingkan tabel angka mentah (Sharma dan Joshi, 2022). Fitur filter interaktif memungkinkan pimpinan institusi mengeksplorasi data secara mandiri tanpa memerlukan keahlian teknis, sesuai dengan prinsip DSS (Zhang dan Goyal, 2024).

Ketiga, identifikasi titik kritis dan peringatan dini. Sistem mampu mengidentifikasi program studi dalam kondisi kritis (melampaui batas DIKTI) maupun dalam zona waspada, sehingga berfungsi sebagai mekanisme early warning bagi manajemen institusi untuk merencanakan rekrutmen dosen, mengevaluasi daya tampung mahasiswa baru, menyusun strategi redistribusi beban mengajar, serta menyiapkan data akreditasi.

Keempat, penerapan konsep Single Version of the Truth (SVOT). Dengan mengonsolidasikan seluruh data ke dalam satu data warehouse dan satu dashboard terpadu, sistem mewujudkan konsep SVOT (Kimball dan Ross, 2013). Seluruh pemangku kepentingan mengakses sumber data yang sama, sehingga menghindari inkonsistensi informasi yang kerap terjadi pada pelaporan manual berbasis spreadsheet yang terpisah. Hal ini turut menjawab tantangan tata kelola data di perguruan tinggi sebagaimana diidentifikasi oleh Astuti dkk. (2024).


4.5.3 Analisis Rasio Berdasarkan Rumpun Ilmu (Sains vs Sosial)

Permendikbud Nomor 3 Tahun 2020 tentang Standar Nasional Pendidikan Tinggi menetapkan batas ambang rasio yang berbeda antara dua rumpun ilmu, yaitu 1:30 untuk rumpun Sains/Teknologi (Saintek) dan 1:45 untuk rumpun Sosial/Humaniora (Soshum). Perbedaan batas ini mencerminkan pertimbangan bahwa program studi Saintek membutuhkan bimbingan dosen yang lebih intensif karena adanya kegiatan praktikum, penelitian laboratorium, dan supervisi tugas akhir berbasis riset eksperimental, sehingga secara ideal satu dosen hanya membimbing mahasiswa dalam jumlah yang lebih sedikit dibandingkan pada program studi Soshum.

Untuk menganalisis perbedaan kondisi antara kedua rumpun ilmu tersebut pada Universitas Siliwangi, divisualisasikan rata-rata rasio per rumpun ilmu selama lima periode pelaporan. Gambar 4.14 di bawah ini menyajikan hasil visualisasi tersebut.

[Gambar 4.14 Grafik Tren Rasio Sains vs Sosial]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/line_tren_sains_vs_sosial.png

Berdasarkan Gambar 4.14, terdapat perbedaan rata-rata rasio dosen terhadap mahasiswa antara program studi rumpun Sains (Saintek) dan rumpun Sosial (Soshum) di Universitas Siliwangi. Secara umum, rumpun Sosial memiliki rata-rata rasio yang lebih tinggi (mendekati 1:28 hingga 1:35) dibandingkan rumpun Sains (berada pada kisaran 1:14 hingga 1:20). Meskipun nilai rata-rata rumpun Sosial belum melampaui batas Soshum (1:45), nilai tersebut sudah mendekati batas Saintek (1:30), dan beberapa program studi sosial secara individual bahkan telah melampaui kedua batas tersebut.

Temuan ini menunjukkan bahwa beban mengajar dosen pada program studi sosial secara rata-rata jauh lebih tinggi dibandingkan dosen pada program studi sains. Fenomena ini sejalan dengan kecenderungan bahwa program studi rumpun sosial seringkali menerima kuota mahasiswa baru dalam jumlah yang lebih besar tanpa diimbangi rekrutmen dosen secara sebanding, sementara program studi sains cenderung memiliki batasan kapasitas alami karena kebutuhan praktikum dan fasilitas laboratorium. Perbedaan batas regulasi yang ditetapkan Permendikbud Nomor 3 Tahun 2020 ini mengandung implikasi kebijakan yang penting, yaitu bahwa evaluasi kapasitas akademik tidak dapat dilakukan dengan satu batas ambang tunggal, melainkan harus mempertimbangkan rumpun ilmu masing-masing program studi.


4.5.4 Kesesuaian dengan Penelitian Terdahulu

Temuan mengenai disparitas rasio dosen terhadap mahasiswa antarprogram studi di dalam satu institusi ini sejalan dengan penelitian terdahulu yang dilakukan oleh Susanto dan Hidayati (2022) serta Setiawan dkk. (2023), yang menemukan bahwa Perguruan Tinggi Negeri (PTN) seringkali terlihat sehat secara agregat (memenuhi batas DIKTI), namun mengalami ketimpangan beban yang ekstrem pada program studi favorit, terutama pada rumpun pendidikan dan ekonomi.

Selain itu, penerapan Business Intelligence Roadmap (Moss dan Atre, 2003) dalam mengatasi masalah pelaporan data akademik yang bersifat statis juga mendukung temuan Sharma dan Joshi (2022), yang menegaskan bahwa penggunaan dashboard visual interaktif seperti Google Looker Studio mampu mempercepat proses identifikasi anomali data (misalnya program studi yang melampaui batas rasio 1:45) hingga tiga kali lebih cepat dibandingkan pelaporan tradisional berbasis tabel. Dengan demikian, pendekatan yang diterapkan dalam penelitian ini terbukti valid dan relevan untuk diterapkan di lingkungan PTN BLU dalam mendukung tata kelola sumber daya manusia yang lebih efektif.


BAB V
KESIMPULAN DAN SARAN


5.1 Kesimpulan

Berdasarkan hasil penelitian yang telah dilaksanakan, dapat ditarik kesimpulan sebagai berikut.

1. Kondisi kapasitas akademik Universitas Siliwangi secara agregat berada di bawah batas ambang DIKTI (1:45 untuk Soshum dan 1:30 untuk Saintek berdasarkan Permendikbud Nomor 3 Tahun 2020), dengan rata-rata rasio dosen terhadap mahasiswa per program studi berada pada rentang 22,8 hingga 24,9 per semester selama lima periode pelaporan (Ganjil 2023–Ganjil 2025). Namun, terdapat disparitas struktural pada level program studi yang tidak tampak pada nilai rata-rata institusi: tiga program studi melampaui batas Soshum pada periode terbaru (Pendidikan Sejarah 1:54,0; Pendidikan Masyarakat 1:50,9; Akuntansi 1:45,7), dan beberapa program studi sains melampaui batas Saintek (1:30). Analisis longitudinal menunjukkan bahwa Pendidikan Masyarakat memiliki rasio yang konsisten melampaui batas pada tiga dari lima periode pengamatan, mengindikasikan adanya permasalahan struktural yang memerlukan penanganan jangka panjang.

2. Sistem Business Intelligence yang dibangun dengan menggunakan BI Roadmap (Moss dan Atre, 2003) mengubah data agregat PDDikti yang sebelumnya bersifat statis menjadi data warehouse terstruktur (star schema: satu fact table dan tiga dimension table, 201 rekaman) serta dashboard analitik interaktif berbasis Google Looker Studio. Sistem ini mendukung Decision Support System dengan menyajikan informasi kapasitas akademik secara visual, interaktif, dan tervalidasi (tingkat konsistensi data 100% antara data warehouse dan dashboard), serta dilengkapi filter analisis per Fakultas dan per Rumpun Ilmu yang memungkinkan eksplorasi data pada tingkat unit organisasi institusi.


5.2 Keterbatasan Penelitian

Penelitian ini memiliki beberapa keterbatasan yang perlu diperhatikan dalam menginterpretasikan hasilnya.

1. Data yang digunakan merupakan data agregat yang bersumber dari portal PDDikti, sehingga analisis tidak dapat dilakukan hingga ke level individu dosen, seperti riwayat pengajaran spesifik atau identitas NIDN/NIDK tertentu.

2. Sistem pipeline ETL saat ini belum terhubung langsung dengan basis data (API) PDDikti secara real-time, melainkan masih mengandalkan data hasil web scraping berkala, sehingga memerlukan proses pembaruan data secara manual pada setiap periode pelaporan baru.

3. Fokus analisis masih terbatas pada rasio dosen terhadap mahasiswa sebagai indikator kuantitatif beban kerja, dan belum memperhitungkan aspek kualitatif seperti kualifikasi pendidikan dosen, jabatan fungsional, serta beban tugas tambahan di luar pengajaran.


5.3 Saran

Berdasarkan keterbatasan penelitian yang telah diidentifikasi, diajukan saran-saran sebagai berikut untuk penelitian dan pengembangan selanjutnya.

1. Memperluas cakupan analisis ke seluruh PTN BLU lain di Indonesia untuk keperluan benchmarking antarinstitusi, sehingga posisi relatif Universitas Siliwangi dalam skala nasional dapat diketahui.

2. Menambahkan variabel analisis lain yang lebih komprehensif, seperti beban kerja dosen (BKD), kualifikasi akademik, dan jabatan fungsional, untuk memperoleh gambaran kapasitas akademik yang lebih holistik.

3. Mengembangkan modul analisis prediktif berbasis tren historis untuk memproyeksikan kebutuhan rekrutmen dosen pada periode-periode mendatang berdasarkan pola pertumbuhan mahasiswa.

4. Mengotomasi pipeline ETL agar terhubung langsung dengan sumber data (API) PDDikti secara real-time, sehingga dashboard dapat selalu menampilkan data terkini tanpa intervensi manual.

5. Melakukan sosialisasi dan User Acceptance Testing (UAT) kepada pemangku kepentingan di lingkungan Universitas Siliwangi, seperti Wakil Rektor Bidang Akademik, para Dekan, dan unit Lembaga Penjaminan Mutu Internal (LPMI), untuk mengevaluasi tingkat penerimaan dan kegunaan sistem dari perspektif pengguna akhir.

6. Menambahkan fitur notifikasi otomatis yang mengirimkan peringatan kepada pengelola program studi ketika nilai rasio mendekati atau melampaui batas ambang yang telah ditetapkan oleh Permendikbud Nomor 3 Tahun 2020.
