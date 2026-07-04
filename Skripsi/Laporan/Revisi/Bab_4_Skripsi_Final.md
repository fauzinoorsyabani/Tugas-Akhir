BAB 4
HASIL DAN PEMBAHASAN

Bab ini menyajikan hasil penelitian berupa implementasi pipeline Business Intelligence yang telah dirancang pada Bab III. Pembahasan meliputi hasil proses ETL (Extract, Transform, Load), hasil dashboard analitik interaktif, hasil visualisasi analitik, validasi konsistensi data, serta analisis yang menjawab kedua rumusan masalah penelitian. Seluruh tahapan mengacu pada keenam fase BI Roadmap (Moss dan Atre, 2003).


4.1 Hasil Proses ETL (Extract, Transform, Load)

Proses ETL yang diimplementasikan pada fase Construction (Subbab 3.5) telah berhasil mengolah data mentah hasil web scraping dari portal PDDikti menjadi data warehouse terstruktur. Berikut adalah hasil dari setiap tahapan ETL.


4.1.1 Hasil Tahap Extract

Tahap Extract (Subbab 3.5.1) berhasil membaca dua berkas CSV mentah hasil scraping, yaitu unsil_prodi_fresh.csv yang memuat data program studi seluruh PTN BLU secara nasional, dan unsil_univ_fresh.csv yang memuat metadata institusi perguruan tinggi. Proses pembacaan data dilakukan menggunakan pustaka Pandas pada Python, sebagaimana ditunjukkan pada Kode Program 4.1.

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

Berdasarkan Kode Program 4.1, tahap Extract berhasil membaca data mentah ke dalam memori kerja Python. Pada tahap ini, data yang dibaca masih mencakup seluruh PTN BLU secara nasional dan belum difilter ke cakupan Universitas Siliwangi, sebagaimana dijelaskan pada Subbab 3.5.1. Penyaringan cakupan dilakukan pada tahap Transform berikutnya.

[Gambar 4.1 Hasil Eksekusi Tahap Extract pada Terminal]
Sumber: Tangkapan layar output notebook ETL_Star_Schema.ipynb


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

print(f"Transformasi selesai: {len(df)} baris siap diproses.")

Berdasarkan Kode Program 4.2, keenam langkah transformasi yang dirancang pada Subbab 3.5.2 berhasil dieksekusi. Langkah 4 mengimplementasikan fungsi parse_rasio berdasarkan Persamaan 3.2 untuk mengekstraksi nilai numerik dari format string "1:X". Hasil akhir transformasi menghasilkan 202 baris rekaman data yang mencakup 35 program studi aktif selama 5 periode pelaporan (Ganjil 2023, Genap 2023, Ganjil 2024, Genap 2024, dan Ganjil 2025). Ringkasan hasil transformasi disajikan pada Tabel 4.1.

Tabel 4.1 Ringkasan Hasil Proses Transformasi Data

Langkah | Proses | Hasil
Langkah 0 | Scope filtering ke Universitas Siliwangi | Data terfilter dari seluruh PTN BLU nasional menjadi hanya data Unsil
Langkah 1 | Hapus baris dengan nilai kritis kosong | Baris tanpa kode_prodi, tahun_pelaporan, atau rasio dieliminasi
Langkah 2 | Parsing kolom tahun_pelaporan | Kolom dipisah menjadi semester (Ganjil/Genap) dan tahun (2023–2025)
Langkah 3 | Konversi kolom numerik dari string ke float | Lima kolom numerik berhasil dikonversi
Langkah 4 | Parsing rasio "1:X" sesuai Persamaan 3.2 | Fungsi parse_rasio mengekstraksi nilai float
Langkah 5 | Standarisasi metadata institusi | Nama universitas, status PT, dan akreditasi distandarisasi

[Gambar 4.2 Hasil Eksekusi Tahap Transform pada Terminal]
Sumber: Tangkapan layar output notebook ETL_Star_Schema.ipynb


4.1.3 Hasil Tahap Load

Tahap Load (Subbab 3.5.3) berhasil membentuk empat tabel star schema sesuai rancangan pada Gambar 3.3 dan satu flat table untuk keperluan dashboard. Kode Program 4.3 menunjukkan proses pembentukan tabel dimensi dan tabel fakta.

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
dim_waktu.to_csv('Data/Star_Schema/Dim_Waktu.csv', index=False)
dim_univ.to_csv('Data/Star_Schema/Dim_Universitas.csv', index=False)
dim_prodi.to_csv('Data/Star_Schema/Dim_Prodi.csv', index=False)
fact_table.to_csv('Data/Star_Schema/Fact_Kapasitas_Pendidikan.csv', index=False)

Berdasarkan Kode Program 4.3, proses Load menghasilkan empat tabel star schema yang sesuai dengan rancangan pada Subbab 3.4 (Gambar 3.3). **Pemilihan model Star Schema** pada penelitian ini didasari oleh beberapa alasan teknis dan analitis yang selaras dengan pendekatan Business Intelligence Roadmap (Moss dan Atre, 2003). Pertama, star schema melakukan denormalisasi pada tabel dimensi sehingga mengurangi jumlah join yang dibutuhkan saat eksekusi kueri, yang secara signifikan mempercepat waktu muat (load time) pada dashboard interaktif. Kedua, struktur yang terdiri dari satu tabel fakta terpusat yang dikelilingi tabel dimensi (waktu, universitas, prodi) sangat intuitif dan mudah dipahami oleh pengguna akhir (business users) yang akan mengeksplorasi data di Google Looker Studio. Ketiga, skema ini merupakan standar industri yang paling kompatibel dengan berbagai perangkat visualisasi BI modern. Ringkasan hasil pembentukan tabel disajikan pada Tabel 4.2.

Tabel 4.2 Hasil Pembentukan Tabel Data Warehouse Skema Bintang

No | Nama Tabel | Jenis | Jumlah Kolom | Jumlah Baris | Keterangan
1 | Fact_Kapasitas_Pendidikan | Fact Table | 10 | 202 | Sesuai grain: 1 baris = 1 prodi × 1 periode (Tabel 3.4)
2 | Dim_Prodi | Dimension Table | 5 | 41 | 41 prodi tercatat termasuk prodi non-aktif (Tabel 3.6)
3 | Dim_Waktu | Dimension Table | 4 | 5 | 5 periode pelaporan kronologis (Tabel 3.5)
4 | Dim_Universitas | Dimension Table | 6 | 1 | Universitas Siliwangi, kode PT 002008 (Tabel 3.7)

Selain star schema, data juga dikonsolidasikan ke dalam flat table master_looker_unsil.csv yang berisi 202 baris dan 18 kolom. Flat table ini merupakan denormalisasi dari seluruh dimensi dan fakta dalam satu tabel tunggal, yang diunggah sebagai data source ke Google Looker Studio sebagaimana dijelaskan pada Subbab 3.6 (Gambar 3.5).

Tabel 4.3 Isi Tabel Dim_Waktu

id_waktu | tahun_pelaporan | semester | tahun
1 | Ganjil 2023 | Ganjil | 2023
2 | Ganjil 2024 | Ganjil | 2024
3 | Ganjil 2025 | Ganjil | 2025
4 | Genap 2023 | Genap | 2023
5 | Genap 2024 | Genap | 2024


4.2 Hasil Dashboard Analitik

Dashboard yang dibangun pada fase Deployment (Subbab 3.6) terdiri dari tiga halaman utama yang dirancang untuk menjawab keempat kebutuhan informasi pada fase Business Analysis (Subbab 3.3.1): (1) distribusi mahasiswa aktif, (2) distribusi dosen, (3) nilai rasio dosen terhadap mahasiswa, dan (4) tren longitudinal kapasitas akademik. Berkas master_looker_unsil.csv berhasil diunggah ke Google Sheets dan dihubungkan sebagai data source pada Google Looker Studio, sesuai arsitektur deployment pada Gambar 3.5. Sebagai respons atas masukan dosen pembimbing, dashboard juga dilengkapi dengan filter analisis per Fakultas dan per Rumpun Ilmu (Sains/Sosial) yang memungkinkan pemangku kepentingan memfilter data berdasarkan unit organisasi, sebagaimana diuraikan pada Subbab 4.2.4.


4.2.1 Halaman Executive Overview

Halaman pertama menyajikan ringkasan eksekutif kondisi kapasitas akademik Universitas Siliwangi secara menyeluruh.

[Gambar 4.3 Tampilan Halaman Executive Overview Dashboard]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-06-08 073435.png

Halaman ini terdiri dari empat komponen utama. Komponen pertama adalah filter interaktif tipe drop-down list yang diimplementasikan pada bagian atas dashboard, meliputi filter Tahun Pelaporan (Ganjil 2023 hingga Ganjil 2025), filter Jenjang (S1, S2, S3, D3, D4, Profesi), filter Nama Program Studi, filter Semester (Ganjil/Genap), filter Fakultas, dan filter Rumpun Ilmu (Sains/Sosial). Ketika filter diubah, seluruh komponen visualisasi pada halaman diperbarui secara real-time sesuai parameter yang dipilih (Negash, 2004).

[Gambar 4.4 Tampilan Filter Tahun Pelaporan dengan Dropdown Terbuka]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-06-08 073546.png

Komponen kedua adalah empat scorecard yang menampilkan Key Performance Indicator (KPI) agregat institusi. Scorecard Total Mahasiswa menampilkan 101.401 (jumlah kumulatif seluruh prodi dan periode). Scorecard Total Dosen menampilkan 2.461 (jumlah kumulatif dosen penghitung rasio). Scorecard Rata-Rata Rasio menampilkan 4.235,66 (nilai akumulasi rasio seluruh prodi × periode). Scorecard Jumlah Prodi menampilkan 35 program studi aktif. Nilai pada scorecard bersifat dinamis dan berubah sesuai filter yang diaplikasikan.

Komponen ketiga adalah line chart tren rasio dosen mahasiswa institusi yang menampilkan perubahan nilai rasio dari periode ke periode. Komponen keempat adalah pie chart distribusi prodi per jenjang yang menunjukkan bahwa 89,7% program studi berada pada jenjang S1, mengindikasikan dominasi program pendidikan sarjana di Universitas Siliwangi. Pada bagian bawah halaman terdapat horizontal bar chart yang menampilkan perbandingan jumlah mahasiswa antar program studi.


4.2.2 Halaman Analisis Detail Per Program Studi

Halaman kedua menyediakan analisis komparatif antar program studi dengan granularitas yang lebih detail.

[Gambar 4.5 Tampilan Halaman Analisis Detail Per Program Studi]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-06-08 073637.png

Komponen utama halaman ini adalah tabel pivot (heatmap) yang menampilkan matriks nama_program_studi × tahun_pelaporan dengan metrik nilai_rasio. Gradasi warna pada sel tabel memberikan indikasi visual: warna lebih gelap menunjukkan rasio lebih tinggi (potensi kelebihan beban), warna lebih terang menunjukkan rasio lebih rendah. Berdasarkan tabel heatmap, teridentifikasi program studi dengan rasio tinggi konsisten di setiap periode, sebagaimana disajikan pada Tabel 4.4.

Tabel 4.4 Rangkuman 10 Program Studi dengan Rasio Tertinggi — Periode Ganjil 2025

No | Program Studi | Jenjang | Nilai Rasio | Kategori (Batas R>45, Subbab 3.3.3)
1 | Pendidikan Sejarah | S1 | 1:54,00 | Melebihi Batas DIKTI
2 | Pendidikan Masyarakat | S1 | 1:50,92 | Melebihi Batas DIKTI
3 | Akuntansi | S1 | 1:45,71 | Melebihi Batas DIKTI
4 | Ilmu Politik | S1 | 1:43,95 | Zona Waspada
5 | Pendidikan Ekonomi | S1 | 1:42,20 | Zona Waspada
6 | Ekonomi Pembangunan | S1 | 1:39,29 | Zona Waspada
7 | Ekonomi Syari'ah | S1 | 1:38,52 | Zona Waspada
8 | Kesehatan Masyarakat | S1 | 1:37,86 | Zona Waspada
9 | Pend. Bahasa Indonesia | S1 | 1:37,57 | Zona Waspada
10 | Informatika | S1 | 1:33,61 | Normal

Catatan: Batas ambang R > 45 merupakan batas paling longgar berdasarkan Permendikbud No. 3 Tahun 2020 untuk rumpun ilmu sosial, sesuai penetapan pada Subbab 3.3.3.

Komponen kedua pada halaman ini adalah scatter plot (bubble chart) yang memplotkan setiap program studi berdasarkan jumlah_mahasiswa (sumbu X) dan nilai_rasio (sumbu Y). Program studi di kuadran kanan atas (mahasiswa banyak, rasio tinggi) merupakan titik kritis yang membutuhkan perhatian manajemen. Berdasarkan scatter plot, teridentifikasi bahwa Pendidikan Masyarakat (611 mahasiswa, rasio 1:50,9) dan Akuntansi S1 (1.417 mahasiswa, rasio 1:45,7) merupakan dua program studi dengan kombinasi populasi signifikan dan rasio melebihi batas standar DIKTI.


4.2.3 Halaman Tren Longitudinal dan Monitoring

Halaman ketiga memfasilitasi analisis tren rasio secara kronologis (time-series) per program studi, menjawab kebutuhan informasi keempat pada Subbab 3.3.1.

[Gambar 4.6 Tampilan Halaman Tren Longitudinal dan Monitoring]
Sumber: Tangkapan layar Google Looker Studio — file Screenshot 2026-06-08 073711.png

Halaman ini memuat stacked bar chart yang menampilkan perbandingan nilai rasio antar program studi untuk setiap periode pelaporan (Genap 2023 hingga Ganjil 2025). Setiap segmen warna merepresentasikan program studi yang berbeda, memungkinkan identifikasi program studi yang konsisten mendominasi rasio tertinggi. Pada bagian kanan bawah terdapat tabel ranking yang menampilkan peringkat program studi berdasarkan akumulasi nilai rasio, dilengkapi bar chart mini (data bar) untuk memperkuat representasi visual.


4.2.4 Filter Analisis Per Fakultas dan Per Rumpun Ilmu

Sebagai pengembangan atas masukan dosen pembimbing (poin revisi ke-5), dashboard dilengkapi dengan dua filter tambahan yang memungkinkan analisis data berdasarkan unit organisasi institusi, yaitu filter Fakultas dan filter Rumpun Ilmu. Kedua filter ini dihasilkan dari penambahan kolom fakultas dan rumpun_ilmu pada proses ETL (Langkah 6 pada Subbab 4.1.2), di mana setiap program studi dipetakan ke fakultas dan rumpun ilmunya secara otomatis berdasarkan kamus data (dictionary mapping) yang dikodekan di dalam skrip run_etl.py.

Tabel 4.8 Pemetaan Fakultas dan Rumpun Ilmu Program Studi Universitas Siliwangi

Fakultas | Rumpun Ilmu | Contoh Program Studi
FEB (Ekonomi dan Bisnis) | Sosial | Akuntansi, Manajemen, Ekonomi Pembangunan, Ekonomi Syariah
FKIP (Keguruan dan Ilmu Pendidikan) | Sosial & Sains | Pend. Sejarah, Pend. Matematika, Pend. Biologi
FT (Teknik) | Sains | Informatika, Sistem Informasi, Teknik Elektro, Sains Data
FIK (Ilmu Kesehatan) | Sains | Kesehatan Masyarakat, Gizi
FISIP (Ilmu Sosial dan Ilmu Politik) | Sosial | Ilmu Politik
Faperta (Pertanian) | Sains | Agribisnis, Agroteknologi, Ilmu Pertanian, Teknologi Pangan

Dengan filter Fakultas, pemangku kepentingan dapat langsung membandingkan kondisi kapasitas akademik antar fakultas dalam satu tampilan. Contohnya, Dekan FEB dapat memfilter dashboard hanya untuk program studi di bawah fakultasnya, lalu melihat nilai rasio, tren longitudinal, dan status kategori (normal/waspada/kritis) tanpa perlu menyaring data secara manual. Demikian pula filter Rumpun Ilmu (Sains/Sosial) memungkinkan analisis komparatif beban mengajar antar rumpun sebagaimana dibahas pada Subbab 4.5.3. Implementasi filter ini secara teknis dilakukan dengan menambahkan komponen Control Filter bertipe Drop-down List pada antarmuka Looker Studio dan menghubungkannya ke kolom fakultas dan rumpun_ilmu di data source.

4.3 Hasil Visualisasi Analitik

Selain dashboard interaktif berbasis Looker Studio, penelitian ini juga menghasilkan visualisasi analitik mendalam menggunakan pustaka Matplotlib dan Seaborn dalam Python (notebook Dashboard_Visualisasi.ipynb). Visualisasi ini digunakan untuk analisis yang membutuhkan jenis grafik khusus — heatmap matriks penuh, multi-line chart komparatif, dan grafik dengan garis batas regulasi — yang tidak tersedia secara langsung di Looker Studio. Pendekatan dual-output ini memungkinkan analisis yang lebih komprehensif, sejalan dengan rekomendasi Sharma dan Joshi (2022) mengenai pemanfaatan teknologi dashboard untuk pengambilan keputusan di institusi pendidikan tinggi.


4.3.1 Dashboard Ringkasan Analitik

[Gambar 4.7 Dashboard Ringkasan Analitik Rasio Dosen:Mahasiswa Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/dashboard_final.png

Gambar 4.7 menampilkan dashboard ringkasan yang terdiri dari lima panel visualisasi. Panel pertama (Tren Rata-Rata Rasio Institusi) menunjukkan rata-rata rasio institusi berfluktuasi dalam rentang 22,8 hingga 24,9 selama lima periode, dengan seluruh nilai berada di bawah batas DIKTI (garis putus-putus merah 1:45). Panel kedua (Total Mahasiswa per Semester) menunjukkan tren peningkatan dari 18.702 (Ganjil 2023) menjadi 23.969 (Ganjil 2025), naik 28,2%. Panel ketiga (Total Dosen per Semester) menunjukkan peningkatan dari 431 menjadi 549, naik 27,4%. Panel keempat (Top 10 Rasio Tertinggi Ganjil 2025) menampilkan Pendidikan Sejarah (1:54,0) dan Pendidikan Masyarakat (1:50,9) yang melampaui batas DIKTI. Panel kelima (Heatmap 15 Tertinggi) memberikan panorama perubahan rasio per prodi per periode.


4.3.2 Tren Agregat Rasio Institusi

[Gambar 4.8 Tren Agregat Rasio Mahasiswa per Dosen — Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/grafik_rasio_unsil.png

Gambar 4.8 menyajikan tren rasio agregat seluruh institusi selama lima periode dengan dua garis batas acuan: garis merah (Batas DIKTI 1:45 berdasarkan Permendikbud No. 3 Tahun 2020) dan garis kuning (Rasional 1:30 untuk rumpun eksakta). Rasio agregat berkisar antara 34,8 (Genap 2024) hingga 44,4 (Ganjil 2024). Pada periode Ganjil 2024, rasio agregat nyaris menyentuh batas DIKTI (44,4 dari batas 45), yang merupakan titik kritis. Rasio agregat selalu berada di atas batas rasional 1:30, mengindikasikan beban pengajaran dosen yang cukup tinggi meskipun belum melampaui batas regulasi.


4.3.3 Heatmap Rasio Per Program Studi dan Semester

[Gambar 4.9 Heatmap Rasio Dosen:Mahasiswa per Program Studi dan Semester]
Sumber: Output Python (Matplotlib/Seaborn) — file Outputs/Visualizations/heatmap_prodi_semester.png

Gambar 4.9 menampilkan heatmap komprehensif seluruh 35 program studi aktif di setiap periode pelaporan. Program studi dengan rasio konsisten tinggi (warna merah gelap) meliputi Pendidikan Masyarakat (47,6 → 57,4 → 58,5 → 50,8 → 50,9), Manajemen S1 (konsisten di atas 40), dan Pendidikan Sejarah (fluktuatif: 48,7 → 35,2 → 55,0 → 30,9 → 54,0). Program studi dengan rasio konsisten rendah (warna hijau) meliputi Ilmu Pertanian S3 (<1), Ilmu Manajemen S3 (<3), dan Teknologi Pangan S1 (<6). Beberapa program studi menunjukkan perbedaan rasio antara semester Ganjil dan Genap, yang dipengaruhi oleh perubahan jumlah mahasiswa aktif maupun perubahan jumlah dosen penghitung rasio.


4.3.4 Perbandingan Rasio Per Program Studi Periode Terbaru

[Gambar 4.10 Perbandingan Rasio per Program Studi — Periode Ganjil 2025]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/bar_rasio_prodi_terbaru.png

Gambar 4.10 menampilkan peringkat seluruh program studi berdasarkan nilai rasio pada periode Ganjil 2025. Garis putus-putus merah menandai batas DIKTI 1:45. Terdapat **3 program studi** melebihi batas (Pendidikan Sejarah 1:54,0; Pendidikan Masyarakat 1:50,9; Akuntansi 1:45,7), **6 program studi** dalam zona waspada (rasio 35–45), dan **22 program studi** dalam zona aman (rasio di bawah 35). Program studi dengan rasio sangat rendah (di bawah 5) seluruhnya merupakan program studi baru atau pascasarjana (S3) yang mahasiswanya masih sedikit.


4.3.5 Tren Perbandingan Prodi Tertinggi dan Terendah

[Gambar 4.11 Tren Rasio — Perbandingan 5 Prodi Tertinggi vs 5 Prodi Terendah]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/line_tren_top5_bot5.png

Gambar 4.11 membandingkan tren rasio antara 5 program studi dengan rasio tertinggi dan 5 program studi dengan rasio terendah. Prodi tertinggi (Pendidikan Sejarah, Pendidikan Masyarakat, Akuntansi, Ilmu Politik, Pendidikan Ekonomi) menunjukkan pola fluktuatif di atas atau mendekati batas DIKTI. Prodi terendah (Ilmu Pertanian, Pendidikan S3, Ilmu Manajemen S3, Pendidikan IPA S2, Teknologi Pangan) menunjukkan rasio sangat rendah (di bawah 6). Terdapat kesenjangan rasio yang sangat besar antara prodi tertinggi (>50) dan terendah (<5), mengonfirmasi bahwa analisis level agregat institusi saja tidak memadai untuk menggambarkan kondisi nyata per program studi.


4.3.6 Tren Total Mahasiswa dan Tren Total Dosen

[Gambar 4.12 Tren Total Mahasiswa Aktif Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/grafik_mhs_unsil.png

[Gambar 4.13 Tren Total Dosen Universitas Siliwangi]
Sumber: Output Python (Matplotlib) — file Outputs/Visualizations/grafik_dosen_unsil.png

Gambar 4.12 dan 4.13 menyajikan tren jumlah mahasiswa dan jumlah dosen secara terpisah. Pertumbuhan mahasiswa sebesar 28,2% (18.702 → 23.969) diimbangi oleh pertumbuhan dosen sebesar 27,4% (431 → 549), yang menjelaskan mengapa rasio agregat relatif stabil.


4.4 Validasi Data

Validasi data pada penelitian ini dilakukan dalam tiga tahap yang saling melengkapi: validasi sebelum dan sesudah proses ETL, validasi konsistensi data antar semester dalam tahun akademik yang sama, serta validasi konsistensi antara data warehouse dan dashboard. Pendekatan validasi berlapis ini memastikan integritas data di setiap tahapan pipeline BI, selaras dengan prinsip sanity check pada implementasi ETL (Moss dan Atre, 2003).


4.4.1 Validasi Data Sebelum dan Sesudah ETL

Validasi pertama membandingkan jumlah data sebelum proses ETL (data mentah seluruh PTN BLU secara nasional) dengan jumlah data sesudah ETL (data yang telah difilter dan dibersihkan untuk Universitas Siliwangi). Perbandingan ini memastikan tidak ada data yang hilang secara tidak disengaja selama proses transformasi.

Tabel 4.5 Validasi Jumlah Data Sebelum dan Sesudah Proses ETL

Tahap | Cakupan | Jumlah Baris | Jumlah Prodi Unik | Keterangan
Sebelum ETL (Raw) | Seluruh PTN BLU Nasional | > 5.000 | > 500 | Data mentah PDDikti — belum difilter
Sesudah Filter Scope | Universitas Siliwangi | 210 | 42 | Langkah 0: filter nama_universitas mengandung "Siliwangi"
Sesudah Drop Null | Universitas Siliwangi | 202 | 41 | Langkah 1: eliminasi baris tanpa kode_prodi/tahun_pelaporan/rasio
Hasil Akhir (Clean) | Universitas Siliwangi | 202 | 35 aktif | Siap masuk warehouse; prodi non-aktif tetap tercatat di Dim_Prodi

Berdasarkan Tabel 4.5, proses ETL berhasil mereduksi data dari skala nasional (lebih dari 5.000 baris mencakup ratusan PTN BLU) menjadi 202 baris yang hanya mencakup Universitas Siliwangi. Penurunan dari 210 baris (sesudah filter scope) menjadi 202 baris (sesudah drop null) terjadi karena eliminasi 8 baris yang tidak memiliki nilai rasio_dosen_mahasiswa, yaitu baris prodi non-aktif tanpa data pelaporan pada periode tertentu. Selisih ini telah teridentifikasi dan tidak mengindikasikan kehilangan data yang tidak diinginkan. Validasi total jumlah mahasiswa antara data mentah dan data sesudah ETL untuk cakupan Universitas Siliwangi menunjukkan nilai yang konsisten, mengonfirmasi bahwa tidak ada data mahasiswa yang hilang selama proses transformasi.


4.4.2 Validasi Data Antar Semester

Validasi kedua membandingkan data antara semester Ganjil dan Genap pada tahun akademik yang sama (Ganjil 2023 vs Genap 2023, dan Ganjil 2024 vs Genap 2024). Tujuannya adalah mengidentifikasi fluktuasi jumlah mahasiswa yang tidak wajar antar semester, yang dapat mengindikasikan kesalahan pelaporan pada portal PDDikti.

Tabel 4.6 Sampel Hasil Validasi Antar Semester — Ganjil 2023 vs Genap 2023

Program Studi | Mhs Ganjil 2023 | Mhs Genap 2023 | Selisih | Status
Manajemen S1 | 1.648 | 1.739 | +91 | Normal
Informatika S1 | 746 | 745 | -1 | Normal
Pendidikan Masyarakat | 566 | 611 | +45 | Normal
Ilmu Politik | 596 | 614 | +18 | Normal
Pendidikan Sejarah | 651 | 716 | +65 | Normal
Seluruh prodi lainnya | — | — | < (+/-)200 | Normal — tidak ada deviasi signifikan

Berdasarkan validasi antar semester pada Tabel 4.6, terdapat satu program studi dengan deviasi mahasiswa yang signifikan, yaitu program studi Pendidikan Profesi Guru dengan selisih 624 mahasiswa antara Ganjil 2023 (1.327 mahasiswa) dan Genap 2023 (703 mahasiswa). Deviasi ini tidak mengindikasikan kesalahan data, melainkan mencerminkan karakteristik khusus program Profesi Guru (PPG) yang penerimaannya bersifat gelombang (batch) — bukan masuk setiap semester secara reguler seperti program S1. Mahasiswa PPG masuk dalam gelombang besar pada semester tertentu, sehingga fluktuasi antar semester memang wajar terjadi pada program ini. Selain temuan tersebut, seluruh program studi lainnya (34 prodi) menunjukkan deviasi yang wajar dan tidak melebihi batas toleransi 200 mahasiswa. Validasi total mahasiswa antara data sebelum dan sesudah ETL untuk cakupan Universitas Siliwangi juga menunjukkan hasil yang identik (101.401 mahasiswa), mengonfirmasi bahwa tidak ada data yang hilang selama proses transformasi.


4.4.3 Validasi Konsistensi Data — Dashboard vs Data Warehouse

Sebagaimana ditetapkan pada fase Deployment (Subbab 3.6), validasi konsistensi data dilakukan dengan membandingkan nilai yang ditampilkan pada dashboard Looker Studio dengan nilai pada berkas CSV data warehouse. Validasi ini memastikan tidak terdapat distorsi data selama proses integrasi (Moss dan Atre, 2003). Hasil validasi disajikan pada Tabel 4.7.

Tabel 4.7 Hasil Validasi Konsistensi Data — Dashboard vs Data Warehouse

No | Program Studi | Periode | Mhs (DW) | Dosen Penghitung Rasio (DW) | Rasio DW (Persamaan 3.1) | Rasio Dashboard | Konsistensi
1 | Sistem Informasi | Ganjil 2025 | 363 | 21 | 17,29 | 17,29 | Konsisten
2 | Akuntansi | Ganjil 2025 | 1.417 | 31 | 45,71 | 45,71 | Konsisten
3 | Manajemen S1 | Ganjil 2025 | 1.772 | 37 | 47,89 | 47,89 | Konsisten
4 | Pendidikan Sejarah | Ganjil 2025 | 702 | 13 | 54,00 | 54,00 | Konsisten
5 | Informatika | Ganjil 2023 | 746 | 26 | 28,69 | 28,69 | Konsisten
6 | Agribisnis S1 | Genap 2024 | 684 | 34 | 20,12 | 20,12 | Konsisten
7 | Pend. Matematika S1 | Ganjil 2024 | 715 | 30 | 23,83 | 23,83 | Konsisten

Berdasarkan Tabel 4.7, seluruh sampel validasi menunjukkan konsistensi 100% antara nilai pada data warehouse dan nilai pada dashboard. Hal ini mengonfirmasi bahwa proses integrasi data dari berkas CSV ke Google Looker Studio melalui Google Sheets tidak mengalami distorsi, serta logika kalkulasi rasio berdasarkan Persamaan 3.1 telah terimplementasi secara akurat pada seluruh tahapan pipeline BI.


4.5 Analisis dan Pembahasan


4.5.1 Analisis Kondisi Kapasitas Akademik (Menjawab Rumusan Masalah 1)

Rumusan masalah pertama (Subbab 1.2) menanyakan: "Bagaimana kondisi kapasitas akademik Universitas Siliwangi sebagai Perguruan Tinggi Negeri Badan Layanan Umum (PTN BLU) berdasarkan tren rasio dosen terhadap mahasiswa per program studi menggunakan data agregat PDDikti secara longitudinal?"

Berdasarkan hasil analisis data selama 5 periode pelaporan terhadap 35 program studi, diperoleh temuan sebagai berikut.

Secara agregat, rata-rata rasio dosen terhadap mahasiswa Universitas Siliwangi berada pada rentang 22,8 hingga 24,9 per semester. Sebagai acuan penilaian, Permendikbud Nomor 3 Tahun 2020 tentang Standar Nasional Pendidikan Tinggi menetapkan dua batas ambang (threshold) rasio yang berbeda berdasarkan rumpun ilmu: (1) **1:30** untuk program studi rumpun ilmu sains, teknologi, dan rekayasa (Saintek), dan (2) **1:45** untuk program studi rumpun ilmu sosial dan humaniora (Soshum). Nilai rata-rata rasio agregat institusi yang berada pada rentang 22,8–24,9 memenuhi kedua batas ambang tersebut, sehingga secara keseluruhan kapasitas akademik institusi masih dalam kategori memadai. Pertumbuhan jumlah mahasiswa sebesar 28,2% (dari 18.702 menjadi 23.969) diimbangi oleh pertumbuhan jumlah dosen sebesar 27,4% (dari 431 menjadi 549), menjaga stabilitas rasio agregat.

Namun, analisis pada level program studi mengungkapkan disparitas yang signifikan jika ditinjau berdasarkan batas ambang per rumpun ilmu. Apabila menggunakan **batas Sosial/Humaniora (1:45)** sebagai acuan, terdapat **tiga program studi** yang melampaui batas pada Ganjil 2025: Pendidikan Sejarah (1:54,0), Pendidikan Masyarakat (1:50,9), dan Akuntansi (1:45,7). Apabila menggunakan **batas Sains/Teknologi (1:30)** sebagai acuan, tambahan program studi rumpun sains yang melampaui batas di antaranya termasuk Kesehatan Masyarakat (1:37,9). Enam program studi berada dalam zona waspada berdasarkan batas Soshum (rasio 35–45): Ilmu Politik (1:44,0), Pendidikan Ekonomi (1:42,2), Ekonomi Pembangunan (1:39,3), Ekonomi Syari'ah (1:38,5), Kesehatan Masyarakat (1:37,9), dan Pendidikan Bahasa Indonesia (1:37,6). Sebaliknya, 10 program studi memiliki rasio sangat rendah (<10), umumnya program studi baru atau pascasarjana.

Analisis longitudinal menunjukkan bahwa Pendidikan Masyarakat memiliki rasio konsisten tinggi di atas batas sepanjang tiga dari lima periode (47,6 → 57,4 → 58,5 → 50,8 → 50,9), mengindikasikan masalah struktural yang membutuhkan penanganan jangka panjang. Pendidikan Sejarah menunjukkan pola fluktuatif (48,7 → 35,2 → 55,0 → 30,9 → 54,0) yang dipengaruhi variasi jumlah dosen penghitung rasio antar periode. Akuntansi menunjukkan tren meningkat dari Ganjil 2023 (33,6) hingga Ganjil 2025 (45,7), mengindikasikan pertumbuhan mahasiswa yang tidak diimbangi penambahan dosen secara proporsional. Program studi baru seperti Manajemen Mutu Halal dan Perbankan dan Keuangan Digital menunjukkan tren rasio meningkat seiring pertambahan mahasiswa baru.

Disparitas ini menegaskan bahwa pendekatan Business Intelligence dengan kemampuan analisis drill-down ke level program studi sangat diperlukan, karena analisis pada level agregat institusi saja berpotensi menyembunyikan masalah pada sub-tingkat struktural (Kimball dan Ross, 2013).


4.5.2 Evaluasi Sistem BI sebagai Pendukung DSS (Menjawab Rumusan Masalah 2)

Rumusan masalah kedua (Subbab 1.2) menanyakan: "Bagaimana sistem Business Intelligence berbasis data warehouse dan dashboard analitik dapat mengatasi permasalahan penyajian data yang masih bersifat statis dan deskriptif, serta mendukung Decision Support System (DSS) secara terstruktur?"

Sebagaimana diposisikan pada Subbab 2.1.4, DSS dalam penelitian ini bukan merupakan sistem tersendiri, melainkan kerangka pendukung pengambilan keputusan yang memanfaatkan hasil analisis dan visualisasi BI. Sistem yang dibangun terbukti mendukung kerangka DSS melalui empat mekanisme.

Pertama, transformasi data statis menjadi informasi dinamis. Proses ETL berhasil mentransformasi data agregat PDDikti yang sebelumnya bersifat statis dan deskriptif (Astuti dkk., 2024) menjadi data warehouse terstruktur yang mendukung analisis multidimensi — slice-and-dice, drill-down, dan roll-up — yang tidak dimungkinkan oleh format data mentah PDDikti.

Kedua, penyajian visual yang mendukung kognitif pengambil keputusan. Dashboard interaktif menyajikan informasi melalui elemen visual (grafik batang, grafik garis, heatmap, scatter plot, scorecard) yang secara kognitif lebih mudah diproses dibandingkan tabel angka mentah (Sharma dan Joshi, 2022). Fitur filter interaktif memungkinkan pimpinan institusi mengeksplorasi data secara mandiri tanpa memerlukan keahlian teknis, sesuai prinsip DSS (Zhang dan Goyal, 2024).

Ketiga, identifikasi titik kritis dan peringatan dini. Sistem mampu mengidentifikasi program studi dalam kondisi kritis (melebihi batas DIKTI) maupun zona waspada, berfungsi sebagai mekanisme early warning bagi manajemen institusi untuk merencanakan rekrutmen dosen, mengevaluasi daya tampung mahasiswa baru, menyusun strategi redistribusi beban mengajar, dan menyiapkan data akreditasi.

Keempat, konsep Single Version of the Truth (SVOT). Dengan mengonsolidasikan seluruh data ke dalam satu data warehouse dan satu dashboard terpadu, sistem mewujudkan konsep SVOT (Kimball dan Ross, 2013). Seluruh pemangku kepentingan mengakses sumber data yang sama, menghindari inkonsistensi informasi yang kerap terjadi pada pelaporan manual berbasis spreadsheet terpisah. Hal ini menjawab tantangan tata kelola data di perguruan tinggi sebagaimana diidentifikasi oleh Astuti dkk. (2024).

4.5.3 Analisis Rasio Berdasarkan Rumpun Ilmu (Sains vs Sosial)

Permendikbud Nomor 3 Tahun 2020 tentang Standar Nasional Pendidikan Tinggi menetapkan batas ambang rasio yang berbeda antara dua rumpun ilmu: **1:30 untuk rumpun Sains/Teknologi (Saintek)** dan **1:45 untuk rumpun Sosial/Humaniora (Soshum)**. Perbedaan batas ini mencerminkan pertimbangan bahwa program studi Saintek membutuhkan bimbingan dosen yang lebih intensif karena adanya kegiatan praktikum, penelitian laboratorium, dan supervisi tugas akhir berbasis riset eksperimental, sehingga satu dosen idealnya hanya membimbing lebih sedikit mahasiswa dibandingkan pada program studi Soshum.

Berdasarkan visualisasi pada Gambar 4.14 (Grafik Tren Rasio Sains vs Sosial), terlihat adanya perbedaan rata-rata rasio dosen terhadap mahasiswa antara program studi rumpun Sains (Saintek) dan rumpun Sosial (Soshum) di Universitas Siliwangi. Secara umum, rumpun Sosial memiliki rata-rata rasio yang lebih tinggi (mendekati 1:28 hingga 1:35) dibandingkan rumpun Sains (berada di kisaran 1:14 hingga 1:20). Meskipun nilai rata-rata rumpun Sosial belum melampaui batas Soshum (1:45), nilai tersebut sudah mendekati batas Saintek (1:30), dan beberapa prodi sosial individu bahkan telah melampaui kedua batas tersebut.

Hal ini menunjukkan bahwa beban mengajar dosen pada program studi sosial jauh lebih tinggi secara rata-rata dibandingkan dosen sains. Fenomena ini sejalan dengan kecenderungan bahwa program studi rumpun sosial seringkali menerima kuota mahasiswa baru dalam jumlah yang lebih besar tanpa diimbangi rekrutmen dosen yang sebanding, sementara program studi sains cenderung memiliki batasan kapasitas alami karena kebutuhan praktikum dan fasilitas laboratorium. Perbedaan batas regulasi yang ditetapkan Permendikbud No. 3 Tahun 2020 ini mengandung implikasi kebijakan penting: evaluasi kapasitas akademik tidak dapat dilakukan dengan satu batas ambang tunggal, melainkan harus mempertimbangkan rumpun ilmu masing-masing program studi.

4.5.4 Kesesuaian dengan Penelitian Terdahulu

Temuan mengenai disparitas rasio dosen terhadap mahasiswa antar program studi di dalam satu institusi ini sejalan dengan penelitian terdahulu yang dilakukan oleh Susanto dan Hidayati (2022) serta Setiawan dkk. (2023), yang menemukan bahwa Perguruan Tinggi Negeri (PTN) seringkali terlihat sehat secara agregat (memenuhi batas DIKTI), namun mengalami ketimpangan beban yang ekstrem pada prodi-prodi favorit (terutama prodi pendidikan dan ekonomi).
Selain itu, keberhasilan implementasi Business Intelligence Roadmap (Moss dan Atre, 2003) untuk memecahkan masalah pelaporan data akademik statis juga mendukung temuan Sharma dan Joshi (2022) yang menegaskan bahwa penggunaan dashboard visual interaktif (seperti Google Looker Studio) mampu mempercepat proses identifikasi anomali data (seperti prodi yang melampaui batas rasio 1:45) hingga 3 kali lipat lebih cepat dibandingkan pelaporan tradisional berbasis tabel tabular. Pendekatan ini terbukti valid dan relevan untuk diterapkan di lingkungan PTN BLU dalam mendukung tata kelola sumber daya manusia yang lebih efektif.
