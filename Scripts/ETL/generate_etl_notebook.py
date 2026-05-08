import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("# ETL Proses: PDDikti ke Star Schema\nProses ini akan mengubah data mentah dari hasil scraping menjadi bentuk Star Schema (Fact & Dimension tables)."))

# Extract
cells.append(nbf.v4.new_markdown_cell("## 1. Extract\nMembaca data raw dari file `universitas_raw.csv` dan `prodi_raw.csv`."))
cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np

# Baca data
df_univ = pd.read_csv('universitas_raw.csv')
df_prodi = pd.read_csv('prodi_raw.csv')

# --- Filter khusus Universitas Siliwangi ---
print("1b. Filtering data hanya untuk Universitas Siliwangi...")
df_univ = df_univ[df_univ['nama_universitas'].str.contains('Universitas Siliwangi', case=False, na=False)]
df_prodi = df_prodi[df_prodi['nama_universitas'].str.contains('Universitas Siliwangi', case=False, na=False)]

print(f"Total baris universitas (Unsil): {len(df_univ)}")
print(f"Total baris prodi (Unsil): {len(df_prodi)}")"""))

# Transform - Cleaning
cells.append(nbf.v4.new_markdown_cell("## 2. Transform - Cleaning & Formatting\nMembersihkan data yang kosong atau format tidak sesuai."))
cells.append(nbf.v4.new_code_cell("""# Menghapus duplikat atau data kosong jika ada
df_prodi = df_prodi.dropna(subset=['kode_prodi', 'rasio_dosen_mahasiswa', 'tahun_pelaporan'])

# Split tahun_pelaporan menjadi Semester dan Tahun
# Contoh format awal: "Ganjil 2024" atau "Genap 2023"
df_prodi[['semester', 'tahun']] = df_prodi['tahun_pelaporan'].str.split(' ', n=1, expand=True)

# Ekstrak nilai rasio (dari format "1:15.5" menjadi angka numerik 15.5)
def hitung_nilai_rasio(rasio_str):
    try:
        if pd.isna(rasio_str):
            return np.nan
        parts = str(rasio_str).split(':')
        if len(parts) == 2:
            return float(parts[1])
        return np.nan
    except:
        return np.nan

df_prodi['nilai_rasio'] = df_prodi['rasio_dosen_mahasiswa'].apply(hitung_nilai_rasio)"""))

# Transform - Dimensi Waktu
cells.append(nbf.v4.new_markdown_cell("## 3. Pembentukan Star Schema\n### Dimensi Waktu (Dim_Waktu)"))
cells.append(nbf.v4.new_code_cell("""dim_waktu = df_prodi[['tahun_pelaporan', 'semester', 'tahun']].drop_duplicates().reset_index(drop=True)
dim_waktu['id_waktu'] = dim_waktu.index + 1
dim_waktu = dim_waktu[['id_waktu', 'tahun_pelaporan', 'semester', 'tahun']]
display(dim_waktu.head())"""))

# Transform - Dimensi Universitas
cells.append(nbf.v4.new_markdown_cell("### Dimensi Universitas (Dim_Universitas)"))
cells.append(nbf.v4.new_code_cell("""dim_univ = df_univ[['kode_pt', 'nama_universitas', 'kota', 'provinsi', 'status_pt', 'akreditasi_institusi']].drop_duplicates().reset_index(drop=True)
dim_univ = dim_univ.rename(columns={'kode_pt': 'id_universitas'})
display(dim_univ.head())"""))

# Transform - Dimensi Prodi
cells.append(nbf.v4.new_markdown_cell("### Dimensi Program Studi (Dim_Prodi)"))
cells.append(nbf.v4.new_code_cell("""dim_prodi = df_prodi[['kode_prodi', 'nama_program_studi', 'jenjang', 'status_prodi', 'akreditasi_prodi']].drop_duplicates(subset=['kode_prodi']).reset_index(drop=True)
dim_prodi = dim_prodi.rename(columns={'kode_prodi': 'id_prodi'})
display(dim_prodi.head())"""))

# Transform - Fact Table
cells.append(nbf.v4.new_markdown_cell("### Tabel Fakta (Fact_Kapasitas_Pendidikan)"))
cells.append(nbf.v4.new_code_cell("""# Merge dataframe prodi dengan dim_waktu untuk mendapatkan foreign key 'id_waktu'
fact_table = df_prodi.merge(dim_waktu, on='tahun_pelaporan', how='left')

# Pilih kolom-kolom untuk Fact Table beserta foreign key:
fact_table = fact_table[[
    'kode_pt', 'kode_prodi', 'id_waktu', 
    'jumlah_dosen_penghitung_rasio', 'dosen_tetap', 'dosen_tidak_tetap', 'total_dosen',
    'jumlah_mahasiswa', 'rasio_dosen_mahasiswa', 'nilai_rasio'
]]

fact_table = fact_table.rename(columns={
    'kode_pt': 'id_universitas',
    'kode_prodi': 'id_prodi',
})

fact_table = fact_table.dropna(subset=['id_universitas', 'id_prodi'])
display(fact_table.head())"""))

# Load
cells.append(nbf.v4.new_markdown_cell("## 4. Load\nMenyimpan hasil ETL ke dalam format Data Warehouse Star Schema (CSV)."))
cells.append(nbf.v4.new_code_cell("""import os
if not os.path.exists('Star_Schema'):
    os.makedirs('Star_Schema')

dim_waktu.to_csv('Star_Schema/Dim_Waktu.csv', index=False)
dim_univ.to_csv('Star_Schema/Dim_Universitas.csv', index=False)
dim_prodi.to_csv('Star_Schema/Dim_Prodi.csv', index=False)
fact_table.to_csv('Star_Schema/Fact_Kapasitas_Pendidikan.csv', index=False)

print("✅ Proses ETL Selesai! Data Star Schema di-load ke folder 'Star_Schema'.")"""))

nb.cells = cells

with open('ETL_Star_Schema.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
