BAB IV
HASIL DAN PEMBAHASAN
4.1	Hasil Proses ETL (Extract, Transform, Load)
Proses ETL (Extract, Transform, Load) yang diimplementasikan pada fase Construction sebagaimana dijelaskan pada Subbab 3.5 digunakan untuk mengolah data hasil web scraping dari portal PDDikti menjadi data yang terstruktur dan siap digunakan dalam data warehouse. Tahapan ETL meliputi proses ekstraksi data mentah, transformasi data, dan pemuatan data ke dalam skema bintang (star schema). Hasil dari masing-masing tahapan dijelaskan pada subbab berikut.
4.1.1	Hasil Tahap Extract
Tahap Extract bertujuan untuk membaca data mentah hasil web scraping yang tersimpan dalam berkas CSV. Sumber data terdiri atas dua berkas, yaitu unsil_prodi_fresh.csv yang memuat data program studi dan unsil_univ_fresh.csv yang memuat informasi institusi perguruan tinggi. Proses pembacaan data dilakukan menggunakan pustaka Pandas pada Python sebagaimana ditunjukkan pada Kode Program 4.1.
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
Berdasarkan hasil eksekusi pada Kode Program 4.1, data mentah dapat dibaca dan dimuat ke dalam lingkungan kerja Python untuk diproses pada tahap berikutnya. Pada tahap ini, data masih mencakup seluruh data hasil scraping dan belum dilakukan penyaringan berdasarkan ruang lingkup penelitian. Oleh karena itu, proses pembatasan data pada Universitas Siliwangi dilakukan pada tahap transformasi.
 
Gambar 4. 1 Hasil Eksekusi Tahap Extract pada Terminal
4.1.2	Hasil Tahap Transform
Tahap Transform bertujuan untuk menyesuaikan struktur dan kualitas data agar sesuai dengan kebutuhan analisis. Transformasi dilakukan melalui beberapa langkah yang meliputi penyaringan data sesuai ruang lingkup penelitian, penanganan nilai yang tidak lengkap, pemisahan atribut waktu, konversi tipe data numerik, ekstraksi nilai rasio, dan standarisasi metadata institusi. Implementasi proses transformasi ditunjukkan pada Kode Program 4.2.
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

Langkah pertama dilakukan dengan menyaring data sehingga hanya mencakup Universitas Siliwangi sesuai fokus penelitian. Setelah proses penyaringan, dilakukan pembersihan data dengan menghapus rekaman yang tidak memiliki atribut penting seperti kode program studi, periode pelaporan, maupun rasio dosen terhadap mahasiswa.
Selanjutnya, atribut tahun_pelaporan dipisahkan menjadi atribut semester dan tahun untuk memudahkan analisis berdasarkan dimensi waktu. Beberapa atribut numerik kemudian dikonversi ke format numerik agar dapat digunakan dalam proses perhitungan dan visualisasi.
Transformasi berikutnya dilakukan pada atribut rasio dosen terhadap mahasiswa yang semula berbentuk teks dengan format 1:X. Nilai tersebut diekstraksi menjadi bentuk numerik sehingga dapat digunakan dalam analisis kuantitatif dan perbandingan antar program studi. Pada tahap akhir dilakukan standarisasi metadata institusi agar seluruh data menggunakan representasi yang konsisten. Ringkasan hasil transformasi disajikan pada Tabel 4.1.
Tabel 4. 1 Ringkasan Hasil Proses Transformasi Data
Langkah	Proses	Hasil
Langkah 0	Scope filtering ke Universitas Siliwangi	Data terfilter dari seluruh PTN BLU nasional menjadi hanya data Universitas Siliwangi (Kode PT: 002008).
Langkah 1	Penghapusan data tidak lengkap (missing value)	Baris data yang tidak memiliki nilai pada atribut kritis seperti kode_prodi, tahun_pelaporan, atau rasio_dosen_mahasiswa dieliminasi dari dataset.
Langkah 2	Parsing atribut tahun_pelaporan	Kolom tahun_pelaporan dipisahkan menjadi dua atribut baru, yaitu semester (Ganjil/Genap) dan tahun (2023–2025).
Langkah 3	Konversi tipe data numerik	Kolom numerik yang semula bertipe string berhasil dikonversi menjadi tipe numerik (float), meliputi jumlah mahasiswa, jumlah dosen tetap, jumlah dosen tidak tetap, jumlah mahasiswa baru, dan jumlah lulusan.
Langkah 4	Parsing rasio dosen–mahasiswa berdasarkan Persamaan 3.2	Fungsi parse_rasio() digunakan untuk mengekstraksi nilai numerik dari format rasio "1:X" menjadi nilai float. Nilai "-" dari sumber PDDikti dikonversi menjadi NaN.
Langkah 5	Standarisasi metadata institusi	Informasi institusi seperti nama perguruan tinggi, status PTN BLU, dan akreditasi institusi "Unggul" distandarisasi untuk menjaga konsistensi data.

Hasil transformasi menghasilkan 202 rekaman data yang merepresentasikan 35 program studi aktif pada lima periode pelaporan, yaitu Ganjil 2023, Genap 2023, Ganjil 2024, Genap 2024, dan Ganjil 2025. Data tersebut selanjutnya digunakan sebagai sumber pembentukan data warehouse.	 
Gambar 4. 2 Hasil Eksekusi Tahap Transform pada Terminal

4.1.3	Hasil Tahap Load
Tahap Load merupakan proses pemuatan data hasil transformasi ke dalam struktur data warehouse yang telah dirancang pada Subbab 3.4. Struktur yang digunakan dalam penelitian ini adalah skema bintang (star schema) yang terdiri atas satu tabel fakta dan tiga tabel dimensi. Implementasi pembentukan tabel data warehouse ditunjukkan pada Kode Program 4.3.
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

Pada tahap ini dibentuk empat tabel utama, yaitu Dim_Waktu, Dim_Universitas, Dim_Prodi, dan Fact_Kapasitas_Pendidikan. Tabel dimensi digunakan untuk menyimpan informasi deskriptif, sedangkan tabel fakta digunakan untuk menyimpan ukuran kuantitatif yang menjadi objek analisis.
Selain pembentukan skema bintang, data juga dikonsolidasikan ke dalam satu tabel denormalisasi (flat table) yang digunakan sebagai sumber data pada dashboard Google Looker Studio. Pendekatan ini dipilih untuk mempermudah proses integrasi dan visualisasi data. Ringkasan hasil pembentukan tabel data warehouse disajikan pada Tabel 4.2.
Tabel 4. 2 Hasil Pembentukan Tabel Data Warehouse Skema Bintang 
No	Nama Tabel	Jenis Tabel	Jumlah Kolom	Jumlah Baris	Keterangan
1	Fact_Kapasitas_Pendidikan	Fact Table	10	202	Merekam data kapasitas akademik setiap program studi pada setiap periode pelaporan
2	Dim_Prodi	Dimension Table	5	41	Menyimpan informasi identitas program studi
3	Dim_Waktu	Dimension Table	4	5	Menyimpan informasi semester dan tahun pelaporan
4	Dim_Universitas	Dimension Table	6	1	Menyimpan informasi institusi Universitas Siliwangi

Tabel 4. 3 Isi Tabel Dim_Waktu
id_waktu	tahun_pelaporan	semester	tahun
1	Ganjil 2023	Ganjil	2023
2	Genap 2023	Genap	2023
3	Ganjil 2024	Ganjil	2024
4	Genap 2024	Genap	2024
5	Ganjil 2025	Ganjil	2025

Berdasarkan hasil proses ETL, data mentah hasil web scraping berhasil ditransformasikan menjadi data terstruktur yang siap digunakan untuk kebutuhan analisis dan visualisasi. Struktur data warehouse yang terbentuk menjadi fondasi bagi pembangunan dashboard analitik yang dibahas pada subbab berikutnya.
4.2	Hasil Dashboard Analitik
4.2.1	Halaman Executive Overview
Halaman Executive Overview merupakan halaman utama dashboard yang dirancang untuk memberikan gambaran umum mengenai kondisi kapasitas akademik Universitas Siliwangi berdasarkan data yang telah diolah pada data warehouse.
 
Gambar 4. 3 Tampilan Halaman Executive Overview Dashboard Looker Studio

Pada bagian atas dashboard tersedia beberapa filter interaktif yang terdiri atas filter Tahun Pelaporan, Jenjang, Nama Program Studi, dan Semester. Filter tersebut memungkinkan pengguna menampilkan informasi sesuai kebutuhan analisis sehingga visualisasi yang ditampilkan dapat difokuskan pada periode maupun program studi tertentu.
 
Gambar 4. 4 Tampilan Filter Tahun Pelaporan dengan Dropdown Terbuka

Selain filter, halaman ini dilengkapi dengan beberapa scorecard yang menampilkan ringkasan indikator utama kapasitas akademik, meliputi jumlah mahasiswa, jumlah dosen, rasio dosen terhadap mahasiswa, dan jumlah program studi yang tercakup dalam data. Ringkasan nilai scorecard disajikan pada Tabel 4.4.
Tabel 4. 4 Nilai Scorecard Dashboard Looker Studio
No	Scorecard	Nilai	Keterangan
1	Total Mahasiswa	101.401	Jumlah kumulatif mahasiswa aktif dari seluruh program studi dan periode pelaporan (18.702 + 17.141 + 23.357 + 18.232 + 23.969).
2	Total Dosen	2.461	Jumlah kumulatif dosen dari seluruh program studi pada seluruh periode pelaporan.
3	Rasio Dosen–Mahasiswa	Bervariasi	Nilai rata-rata rasio dosen terhadap mahasiswa pada setiap program studi. Data engan nilai "-" tidak dihitung dalam proses agregasi.
4	Jumlah Program Studi	35	Total program studi yang tercatat dalam data warehouse Universitas Siliwangi.

Berdasarkan Tabel 4.4, dashboard mampu menyajikan informasi ringkas mengenai kondisi kapasitas akademik Universitas Siliwangi dalam satu tampilan. Informasi tersebut dapat digunakan sebagai titik awal analisis sebelum pengguna melakukan eksplorasi lebih lanjut melalui filter dan visualisasi yang tersedia.
Visualisasi utama pada halaman ini berupa line chart yang menampilkan perubahan rasio dosen terhadap mahasiswa antar periode pelaporan. Grafik tersebut memudahkan pengguna dalam mengamati pola perubahan rasio secara longitudinal.
Dashboard juga menampilkan pie chart yang menggambarkan distribusi program studi berdasarkan jenjang pendidikan. Visualisasi ini memberikan gambaran mengenai komposisi program studi yang dimiliki Universitas Siliwangi berdasarkan kategori jenjang pendidikan. Hasil visualisasi menunjukkan bahwa sebagian besar program studi yang tercakup dalam data berada pada jenjang Sarjana (S1).
Pada bagian bawah halaman ditampilkan horizontal bar chart yang memperlihatkan distribusi jumlah mahasiswa pada setiap program studi. Visualisasi ini membantu pengguna membandingkan jumlah mahasiswa antar program studi secara lebih mudah melalui representasi grafis.

4.2.2	Halaman Analisis Detail Per Program Studi
Halaman kedua menyediakan analisis komparatif antar program studi.
 
Gambar 4. 5 Tampilan Halaman Analisis Detail Per Program Studi

Komponen utama halaman ini adalah tabel pivot (heatmap) matriks nama_program_studi × tahun_pelaporan dengan metrik nilai_rasio. Gradasi warna memberikan indikasi visual kondisi rasio: warna lebih gelap menunjukkan rasio lebih tinggi.
Pada tabel heatmap, beberapa sel menampilkan kosong (blank) alih-alih angka. Hal ini disebabkan oleh nilai NaN pada kolom nilai_rasio di data warehouse untuk program studi yang memiliki jumlah_mahasiswa = 0 dan rasio_dosen_mahasiswa = "-" di PDDikti. Program studi yang teridentifikasi memiliki sel kosong di beberapa periode meliputi: Pendidikan Kependudukan & Lingkungan Hidup, Sains Data, Hukum Bisnis, dan Pendidikan Profesi Guru. Kondisi ini bukan kesalahan sistem, melainkan mencerminkan kondisi aktual dari sumber data PDDikti di mana program studi tersebut belum atau tidak memiliki data mahasiswa aktif pada periode tertentu.
Berdasarkan Tabel 4.5, terdapat empat program studi yang memiliki nilai rasio di atas ambang batas yang digunakan dalam penelitian, yaitu Pendidikan Sejarah (1:54,00), Pendidikan Masyarakat (1:50,92), Manajemen (1:47,89), dan Akuntansi (1:45,71). Temuan ini menunjukkan adanya variasi rasio dosen terhadap mahasiswa antar program studi yang tidak terlihat pada analisis tingkat institusi.
Tabel 4. 5 10 Program Studi dengan Rasio Tertinggi Periode Ganjil 2025
No	Program Studi	Jenjang	Dosen Penghitung Rasio	Mahasiswa Aktif	Nilai Rasio	Status
1	Pendidikan Sejarah	S1	13	702	1:54,00	Melebihi Batas DIKTI
2	Pendidikan Masyarakat	S1	12	611	1:50,92	Melebihi Batas DIKTI
3	Manajemen	S1/S2	37	1.772	1:47,89	Melebihi Batas DIKTI
4	Akuntansi	S1	31	1.417	1:45,71	Melebihi Batas DIKTI
5	Ilmu Politik	S1	21	923	1:43,95	Zona Waspada
6	Pendidikan Ekonomi	S1	15	633	1:42,20	Zona Waspada
7	Pendidikan Geografi	S1	15	619	1:41,27	Zona Waspada
8	Pendidikan Jasmani	S1	37	1.492	1:40,32	Zona Waspada
9	Ekonomi Pembangunan	S1	35	1.375	1:39,29	Normal
10	Ekonomi Syari'ah	S1	21	809	1:38,52	Normal

Batas ambang R > 45 berdasarkan Permendikbud No. 3 Tahun 2020 untuk rumpun ilmu sosial (Subbab 3.3.3). Kolom "Dosen Penghitung Rasio" menggunakan jumlah_dosen_penghitung_rasio dari PDDikti, bukan total_dosen, sesuai formula pada Persamaan 3.1.
Scatter plot (bubble chart) pada bagian bawah halaman memplotkan setiap program studi berdasarkan jumlah_mahasiswa (sumbu X) dan nilai_rasio (sumbu Y). Program studi yang berada pada kuadran kanan atas menunjukkan kombinasi jumlah mahasiswa dan nilai rasio yang relatif lebih tinggi dibandingkan program studi lainnya sehingga dapat menjadi fokus pengamatan dalam evaluasi kapasitas akademik.
4.2.3	Halaman Tren Longitudinal dan Monitoring
Halaman ketiga memfasilitasi analisis tren rasio secara kronologis (time-series) per program studi.
 
Gambar 4. 6  Tampilan Halaman Tren Longitudinal dan Monitoring


Halaman ini memuat stacked bar chart yang menampilkan perbandingan nilai rasio antar program studi pada setiap periode pelaporan. Visualisasi ini memungkinkan pengguna mengamati perubahan kontribusi masing-masing program studi terhadap distribusi rasio secara keseluruhan dari waktu ke waktu.
Selain itu, tersedia tabel peringkat (ranking table) yang menyajikan urutan program studi berdasarkan nilai rasio yang diperoleh. Tabel tersebut dilengkapi dengan data bar untuk memperkuat representasi visual sehingga pengguna dapat mengidentifikasi program studi dengan nilai rasio relatif tinggi maupun rendah secara lebih cepat.
Melalui kombinasi kedua visualisasi tersebut, pengguna dapat melakukan pemantauan perkembangan rasio dosen terhadap mahasiswa secara longitudinal serta membandingkan kondisi antar program studi pada berbagai periode pelaporan.
4.3	Hasil Visualisasi Analitik
Selain dashboard Looker Studio, penelitian ini menghasilkan visualisasi analitik menggunakan pustaka Matplotlib dan Seaborn Python (Notebooks/Dashboard_Visualisasi.ipynb). Visualisasi ini digunakan untuk analisis yang memerlukan heatmap matriks penuh, multi-line chart komparatif, dan grafik dengan garis batas regulasi yang tidak tersedia di Looker Studio. Pendekatan dual-output ini sejalan dengan Sharma dan Joshi (2022).
Mengenai konsistensi angka antara Looker Studio dan Python: Kedua platform menggunakan sumber data yang sama yaitu master_looker_unsil.csv. Python menggunakan fungsi mean() yang secara default mengabaikan NaN (skipna=True), sedangkan Looker Studio secara otomatis mengabaikan sel kosong dalam perhitungan metrik agregat. Oleh karena itu, nilai rata-rata rasio yang ditampilkan keduanya konsisten. Perbedaan yang mungkin terlihat hanya pada tampilan sel kosong (NaN di Python = blank di Looker) dan format desimal (Python menggunakan titik, Looker menyesuaikan locale).
4.3.1	Tren Tingkat Institusi
Kode Program 4.4 menunjukkan implementasi visualisasi tren tingkat institusi yang menghasilkan tiga panel grafik.
Kode Program 4.4 Visualisasi Tren Institusi Sumber: Notebooks/Dashboard_Visualisasi.ipynb
# Agregasi institusi per periode
inst = df.groupby('tahun_pelaporan', observed=True).agg(
    total_mahasiswa=('jumlah_mahasiswa','sum'),
    total_dosen=('total_dosen','sum'),
    rata_rasio=('nilai_rasio','mean')
).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Tren Tingkat Institusi — Universitas Siliwangi', fontsize=15, fontweight='bold')

# Panel kiri: Line chart tren rasio
ax = axes[0]
ax.plot(inst['tahun_pelaporan'], inst['rata_rasio'],
        marker='o', color=COLORS[0], linewidth=2.5, markersize=8)
ax.axhline(y=45, color='red', linestyle='--', linewidth=1.5, label='Batas Dikti (1:45)')
ax.set_title('Tren Rata-Rata Rasio Dosen:Mahasiswa')
ax.set_ylabel('Nilai Rasio (1:x)')
ax.legend()

# Panel tengah: Bar chart total mahasiswa
ax = axes[1]
ax.bar(inst['tahun_pelaporan'], inst['total_mahasiswa'], color=COLORS[1])
ax.set_title('Total Mahasiswa Aktif per Semester')

# Panel kanan: Bar chart total dosen
ax = axes[2]
ax.bar(inst['tahun_pelaporan'], inst['total_dosen'], color=COLORS[2])
ax.set_title('Total Dosen Tetap per Semester')

plt.savefig(os.path.join(PATH_VIZ, 'viz_institusi.png'), bbox_inches='tight', dpi=150)
plt.show()

 
Gambar 4. 7 Tren Tingkat Institusi Rata-Rata Rasio, Mahasiswa dan Dosen

Berdasarkan hasil agregasi Python pada data aktual (master_looker_unsil.csv), tren institusi selama lima periode disajikan pada Tabel 4.6. Tabel 4. 6 Data Aktual Tren Institusi Universitas Siliwangi
Periode	Total Mahasiswa	Total Dosen	Rata-Rata Rasio
Ganjil 2023	18.702	431	24,91
Genap 2023	17.141	431	24,78
Ganjil 2024	23.357	526	24,58
Genap 2024	18.232	524	22,84
Ganjil 2025	23.969	549	24,09

Berdasarkan Tabel 4.6 dan Gambar 4.7, jumlah mahasiswa aktif mengalami fluktuasi selama periode pengamatan dengan nilai tertinggi pada Ganjil 2025 sebanyak 23.969 mahasiswa. Jumlah dosen juga menunjukkan peningkatan dari 431 dosen pada Ganjil 2023 menjadi 549 dosen pada Ganjil 2025. Meskipun terjadi peningkatan jumlah mahasiswa, rata-rata rasio dosen terhadap mahasiswa tetap berada pada rentang 22,84–24,91 sehingga tidak menunjukkan perubahan yang signifikan. Temuan ini mengindikasikan bahwa pertumbuhan jumlah mahasiswa diikuti oleh peningkatan jumlah dosen sehingga rasio institusi relatif stabil selama periode pengamatan.
4.3.2	Heatmap Rasio Per Program Studi dan Semester
Kode Program 4.5 Heatmap Rasio per Program Studi × Semester
# Heatmap rasio per prodi × per semester
pivot = df.pivot_table(
    index='nama_program_studi',
    columns='tahun_pelaporan',
    values='nilai_rasio',
    aggfunc='mean',
    observed=True
)
pivot = pivot.reindex(columns=PERIOD_ORDER)
pivot = pivot.sort_values(PERIOD_ORDER[-1], ascending=False)  # urut berdasarkan Ganjil 2025

fig, ax = plt.subplots(figsize=(12, max(8, len(pivot)*0.4)))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.3, cbar_kws={'label':'Nilai Rasio (1:x)'},
            ax=ax, vmin=0, vmax=45)
ax.set_title('Heatmap Rasio Dosen:Mahasiswa per Program Studi × Semester\nUniversitas Siliwangi',
             fontsize=14, fontweight='bold')
plt.savefig(os.path.join(PATH_VIZ, 'heatmap_prodi_semester.png'), bbox_inches='tight', dpi=150)

 
Gambar 4. 8 Heatmap Rasio Dosen:Mahasiswa per Program Studi & Semester

Heatmap menggunakan skala warna RdYlGn_r (merah = rasio tinggi, hijau = rasio rendah) dengan rentang vmin=0 hingga vmax=45. Program studi dengan rasio di atas 45 ditampilkan dengan warna merah penuh (saturasi maksimum). Sel yang menampilkan NaN dikosongkan secara otomatis oleh Seaborn. Temuan dari heatmap disajikan pada Tabel 4.7.
Tabel 4. 7 Rangkuman Pola Longitudinal Program Studi Terpilih
Program Studi	Ganjil 2023	Genap 2023	Ganjil 2024	Genap 2024	Ganjil 2025	Pola
Pendidikan Masyarakat	47,6	57,4	58,5	50,8	50,9	Konsisten tinggi (selalu >45)
Pendidikan Sejarah	48,7	35,2	55,0	30,9	54,0	Fluktuatif (naik-turun ekstrem)
Manajemen	>40	>40	>40	>40	47,9	Tren meningkat
Akuntansi	>40	>35	>40	>35	45,7	Mendekati batas
Ilmu Pertanian S3	NaN	NaN	<1	<1	0,67	Prodi baru, mahasiswa sangat sedikit
Sains Data	NaN	NaN	NaN	NaN	NaN	Belum ada mahasiswa terdaftar

Berdasarkan Tabel 4.7, Program Studi Pendidikan Masyarakat menunjukkan rasio yang secara konsisten berada di atas ambang batas pada seluruh periode pengamatan. Sebaliknya, Program Studi Pendidikan Sejarah menunjukkan pola fluktuatif yang cukup besar antar periode. Temuan ini menunjukkan bahwa kondisi rasio dosen terhadap mahasiswa tidak bersifat seragam antar program studi dan memerlukan analisis longitudinal untuk memahami perubahannya dari waktu ke waktu.
4.3.3	Perbandingan Rasio Per Program Studi Periode Terbaru
Kode Program 4.6 Bar Chart Perbandingan Rasio Periode Ganjil 2025 Sumber: Notebooks/Dashboard_Visualisasi.ipynb\
# Bar chart perbandingan rasio antar prodi — periode terbaru (Ganjil 2025)
latest = PERIOD_ORDER[-1]  # 'Ganjil 2025'
df_latest = df[df['tahun_pelaporan']==latest].copy()
df_latest = df_latest.groupby('nama_program_studi', observed=True)['nilai_rasio'].mean().reset_index()
df_latest = df_latest.sort_values('nilai_rasio', ascending=True)

# Warna merah untuk yang melebihi batas DIKTI
colors = ['#d62728' if v > 45 else '#1f77b4' for v in df_latest['nilai_rasio']]
bars = ax.barh(df_latest['nama_program_studi'], df_latest['nilai_rasio'], color=colors)
ax.axvline(x=45, color='red', linestyle='--', linewidth=2, label='Batas Dikti (1:45)')
plt.savefig(os.path.join(PATH_VIZ, 'bar_rasio_prodi_terbaru.png'), bbox_inches='tight', dpi=150)

 
Gambar 4. 9 Perbandingan Rasio per Program Studi — Periode Ganjil 2025

Berdasarkan Gambar 4.9, terdapat tiga program studi yang memiliki nilai rasio di atas batas 1:45, yaitu Pendidikan Sejarah, Pendidikan Masyarakat, dan Akuntansi. Sementara itu, sebagian besar program studi berada di bawah ambang batas tersebut dengan variasi nilai rasio yang cukup besar. Visualisasi ini memudahkan identifikasi program studi yang memiliki rasio relatif tinggi pada periode pelaporan terbaru.

4.3.4	Tren Perbandingan 5 Prodi Tertinggi vs 5 Prodi Terendah
Kode Program 4.7 Line Chart Tren Prodi Ekstrem
# Identifikasi 5 prodi tertinggi dan 5 prodi terendah berdasarkan periode terbaru
top5 = df_latest.nlargest(5, 'nilai_rasio')['nama_program_studi'].tolist()
bot5 = df_latest.nsmallest(5, 'nilai_rasio')['nama_program_studi'].tolist()

df_sel = df[df['nama_program_studi'].isin(top5 + bot5)].copy()
df_sel = df_sel.groupby(['nama_program_studi','tahun_pelaporan'], observed=True)['nilai_rasio'].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
# Panel kiri: 5 prodi rasio tertinggi
# Panel kanan: 5 prodi rasio terendah
# Garis batas DIKTI ditambahkan pada kedua panel
plt.savefig(os.path.join(PATH_VIZ, 'line_tren_top5_bot5.png'), bbox_inches='tight', dpi=150)

 
Gambar 4. 10 Tren Rasio Perbandingan 5 Prodi Tertinggi vs 5 Prodi Terendah
Gambar 4.10 menunjukkan perbedaan pola yang cukup jelas antara kelompok program studi dengan rasio tertinggi dan terendah. Program studi pada kelompok tertinggi cenderung berada dekat atau melampaui batas 1:45 pada beberapa periode, sedangkan kelompok terendah memiliki nilai rasio yang jauh di bawah ambang batas. Perbedaan tersebut menunjukkan adanya variasi distribusi mahasiswa dan dosen antar program studi.
4.3.5	Dashboard Final (Ringkasan Semua Panel)
Kode Program 4.8 Dashboard Final — Layout 5 Panel
fig = plt.figure(figsize=(20, 22))
fig.patch.set_facecolor('#f8f9fa')
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)
fig.suptitle('DASHBOARD ANALITIK\nRasio Dosen:Mahasiswa Universitas Siliwangi',
             fontsize=18, fontweight='bold', y=0.98)

# Panel 1 (gs[0,0]): Line tren rata-rata rasio institusi + garis batas DIKTI
# Panel 2 (gs[0,1]): Bar chart total mahasiswa per semester
# Panel 3 (gs[1,0]): Bar chart total dosen per semester
# Panel 4 (gs[1,1]): Horizontal bar — Top 10 prodi rasio tertinggi (Ganjil 2025)
# Panel 5 (gs[2,:]): Heatmap 15 prodi rasio tertinggi × 5 semester

plt.savefig(os.path.join(PATH_VIZ, 'dashboard_final.png'),
            bbox_inches='tight', dpi=150, facecolor=fig.get_facecolor())

 
Gambar 4. 11 Dashboard Final 5 Panel Analitik Terpadu

Dashboard final mengintegrasikan lima visualisasi utama dalam satu tampilan sehingga pengguna dapat melakukan analisis pada tingkat institusi maupun program studi secara bersamaan. Kombinasi line chart, bar chart, heatmap, dan perbandingan rasio memungkinkan identifikasi tren, perbandingan antar program studi, serta pemantauan rasio dosen terhadap mahasiswa secara lebih komprehensif dibandingkan penyajian data dalam bentuk tabel.
4.4	Validasi Konsistensi Data	
Sebagaimana ditetapkan pada fase Deployment (Subbab 3.6), validasi dilakukan dengan membandingkan nilai pada dashboard Looker Studio dengan nilai pada berkas CSV data warehouse (Moss dan Atre, 2003). Hasil validasi disajikan pada Tabel 4.8.
Tabel 4. 8 Hasil Validasi Konsistensi
No	Program Studi	Periode	Dosen Penghitung Rasio (CSV)	Mhs Aktif (CSV)	Rasio CSV (Persamaan 3.1)	Rasio Looker	Konsistensi
1	Sistem Informasi	Ganjil 2025	21	363	1:17,29	1:17,29	Konsisten
2	Akuntansi	Ganjil 2025	31	1.417	1:45,71	1:45,71	Konsisten
3	Manajemen	Ganjil 2025	37	1.772	1:47,89	1:47,89	Konsisten
4	Pendidikan Sejarah	Ganjil 2025	13	702	1:54,00	1:54,00	Konsisten
5	Informatika	Ganjil 2023	26	746	1:28,69	1:28,69	Konsisten
6	Agribisnis	Genap 2024	34	684	1:20,12	1:20,12	Konsisten
7	Pend. Matematika	Ganjil 2024	30	715	1:23,83	1:23,83	Konsisten

Berdasarkan hasil validasi pada Tabel 4.8, seluruh sampel yang diuji menunjukkan kesesuaian antara nilai pada data warehouse dan nilai yang ditampilkan pada dashboard Looker Studio. Hasil tersebut menunjukkan bahwa proses integrasi data mampu mempertahankan konsistensi informasi yang digunakan dalam analisis. Selain itu, nilai rasio yang ditampilkan pada dashboard konsisten dengan hasil perhitungan berdasarkan Persamaan 3.1.
Penjelasan Mengenai Inkonsistensi yang Mungkin Terlihat di Looker Studio:
Terdapat beberapa kondisi tampilan di Looker Studio yang mungkin terlihat berbeda dari data aktual, namun sebenarnya bukan merupakan kesalahan:
(1) Sel kosong atau blank pada tabel dan heatmap: Muncul karena nilai rasio_dosen_mahasiswa di PDDikti adalah "-" untuk program studi yang jumlah mahasiswanya = 0. Fungsi parse_rasio menghasilkan NaN untuk format non-valid, dan Looker Studio menampilkan NaN sebagai blank. Program studi yang teridentifikasi: Hukum Bisnis (Ganjil 2025), Sains Data (seluruh periode kecuali ada mahasiswa), Pendidikan Kependudukan & Lingkungan Hidup, dan Pendidikan Profesi Guru (Ganjil 2025 memiliki 3.489 mahasiswa namun tidak memiliki rasio karena format data PDDikti tidak standar untuk jenis Profesi).
(2) Nilai scorecard "Total Mahasiswa" berbeda tergantung filter aktif: Ini adalah perilaku normal filter interaktif. Tanpa filter, Looker menghitung total seluruh 201 baris data (5 periode × ~35 prodi) sehingga angka menjadi kumulatif lintas periode.
(3) Rata-rata rasio di Looker berbeda dengan rata-rata manual: Looker menggunakan rata-rata dari semua baris yang lolos filter (NaN diabaikan). Jika filter periode diubah, perhitungan berubah. Angka ini konsisten dengan hasil Python pada Tabel 4.6.
4.5	Analisis dan Pembahasan
4.5.1	Analisis Kondisi Kapasitas Akademik
Subbab ini membahas kondisi kapasitas akademik Universitas Siliwangi berdasarkan analisis rasio dosen terhadap mahasiswa pada tingkat institusi maupun program studi selama periode pengamatan.
Berdasarkan data aktual pada Tabel 4.6, rata-rata rasio institusi berada pada rentang 22,84 (Genap 2024) hingga 24,91 (Ganjil 2023). Seluruh nilai rata-rata agregat berada di bawah batas DIKTI (1:45), menunjukkan bahwa rasio agregat institusi masih berada di bawah ambang batas yang digunakan dalam penelitian. Pertumbuhan mahasiswa sebesar 28,2% (18.702 → 23.969 dari Ganjil 2023 ke Ganjil 2025) diimbangi pertumbuhan dosen 27,4% (431 → 549), menjaga kestabilan rasio agregat.
Namun, analisis pada tingkat program studi menunjukkan adanya variasi rasio yang cukup besar antar program studi. Pada periode Ganjil 2025 terdapat tiga program studi yang memiliki nilai rasio di atas ambang batas yang digunakan dalam penelitian, yaitu Pendidikan Sejarah (1:54,00), Pendidikan Masyarakat (1:50,92), dan Akuntansi (1:45,71). Selain itu, beberapa program studi lain memiliki nilai rasio yang relatif tinggi dan berada pada rentang 35–45, seperti Ilmu Politik, Pendidikan Ekonomi, Ekonomi Pembangunan, Ekonomi Syariah, Kesehatan Masyarakat, dan Pendidikan Bahasa Indonesia.
Temuan tersebut menunjukkan bahwa kondisi kapasitas akademik tidak terdistribusi secara merata pada seluruh program studi. Meskipun kondisi institusi secara agregat masih berada di bawah ambang batas yang digunakan dalam penelitian, beberapa program studi menunjukkan nilai rasio yang relatif lebih tinggi dibandingkan program studi lainnya.
Analisis longitudinal (Tabel 4.7) menunjukkan bahwa Program Studi Pendidikan Masyarakat memiliki nilai rasio yang relatif tinggi secara konsisten pada seluruh periode pengamatan (47,6 → 57,4 → 58,5 → 50,8 → 50,9). Sementara itu, Program Studi Pendidikan Sejarah menunjukkan pola fluktuatif (48,7 → 35,2 → 55,0 → 30,9 → 54,0) yang mengindikasikan adanya perubahan rasio antar periode pelaporan. Temuan ini menunjukkan bahwa analisis pada tingkat institusi saja belum cukup untuk menggambarkan kondisi kapasitas akademik secara menyeluruh karena terdapat variasi yang cukup besar pada tingkat program studi.
4.5.2	Evaluasi Sistem BI sebagai Pendukung DSS
Subbab ini membahas bagaimana implementasi Business Intelligence melalui data warehouse dan dashboard analitik mampu menyediakan informasi yang lebih terstruktur dan mudah diakses dibandingkan penyajian data dalam bentuk tabel statis.
Sebagaimana diposisikan pada Subbab 2.1.4, DSS bukan merupakan sistem tersendiri melainkan kerangka pendukung pengambilan keputusan. Implementasi Business Intelligence dalam penelitian ini menunjukkan potensi untuk mendukung proses pengambilan keputusan melalui empat mekanisme utama.
Pertama, transformasi data statis menjadi informasi dinamis. Proses ETL mentransformasi data PDDikti yang bersifat statis (Astuti dkk., 2024) menjadi data warehouse yang mendukung operasi slice-and-dice, drill-down, dan roll-up.
Kedua, penyajian visual yang mendukung kognitif pengambil keputusan. Dashboard interaktif menyajikan informasi melalui grafik batang, grafik garis, heatmap, scatter plot, dan scorecard yang lebih mudah diinterpretasikan dibanding tabel angka mentah (Sharma dan Joshi, 2022). Fitur filter interaktif memungkinkan eksplorasi mandiri tanpa keahlian teknis (Zhang dan Goyal, 2024).
Ketiga, penyediaan informasi pendukung evaluasi kapasitas akademik. Sistem mampu mengidentifikasi program studi yang memiliki nilai rasio relatif tinggi dibandingkan program studi lainnya. Informasi tersebut dapat digunakan sebagai bahan pendukung dalam evaluasi kapasitas akademik, perencanaan kebutuhan dosen, serta pemantauan distribusi mahasiswa dan dosen pada tingkat program studi.
Keempat, Single Version of the Truth (SVOT). Dengan mengonsolidasikan seluruh data ke dalam satu data warehouse dan satu dashboard, seluruh pemangku kepentingan mengakses sumber data yang sama (Kimball dan Ross, 2013), 
membantu mengurangi potensi inkonsistensi informasi sebagaimana diidentifikasi oleh Astuti dkk. (2024).
