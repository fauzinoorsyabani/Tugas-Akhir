import pandas as pd
import numpy as np
import os

print("Memulai proses ETL...")

# 1. Extract
print("1. Extracting data...")
df_univ = pd.read_csv('universitas_raw.csv')
df_prodi = pd.read_csv('prodi_raw.csv')

# --- Filter khusus Universitas Siliwangi ---
print("1b. Filtering data hanya untuk Universitas Siliwangi...")
df_univ = df_univ[df_univ['nama_universitas'].str.contains('Universitas Siliwangi', case=False, na=False)]
df_prodi = df_prodi[df_prodi['nama_universitas'].str.contains('Universitas Siliwangi', case=False, na=False)]

print(f"Total baris universitas (Unsil): {len(df_univ)}")
print(f"Total baris prodi (Unsil): {len(df_prodi)}")

# 2. Transform - Cleaning & Formatting
print("2. Transforming - Cleaning & Formatting...")
df_prodi = df_prodi.dropna(subset=['kode_prodi', 'rasio_dosen_mahasiswa', 'tahun_pelaporan'])
df_prodi[['semester', 'tahun']] = df_prodi['tahun_pelaporan'].str.split(' ', n=1, expand=True)

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

df_prodi['nilai_rasio'] = df_prodi['rasio_dosen_mahasiswa'].apply(hitung_nilai_rasio)

# 3. Transform - Pembentukan Star Schema
print("3. Membentuk Star Schema...")

# Dim_Waktu
dim_waktu = df_prodi[['tahun_pelaporan', 'semester', 'tahun']].drop_duplicates().reset_index(drop=True)
dim_waktu['id_waktu'] = dim_waktu.index + 1
dim_waktu = dim_waktu[['id_waktu', 'tahun_pelaporan', 'semester', 'tahun']]

# Dim_Universitas
dim_univ = df_univ[['kode_pt', 'nama_universitas', 'kota', 'provinsi', 'status_pt', 'akreditasi_institusi']].drop_duplicates().reset_index(drop=True)
dim_univ = dim_univ.rename(columns={'kode_pt': 'id_universitas'})

# Dim_Prodi
dim_prodi = df_prodi[['kode_prodi', 'nama_program_studi', 'jenjang', 'status_prodi', 'akreditasi_prodi']].drop_duplicates(subset=['kode_prodi']).reset_index(drop=True)
dim_prodi = dim_prodi.rename(columns={'kode_prodi': 'id_prodi'})

# Fact Table
fact_table = df_prodi.merge(dim_waktu, on='tahun_pelaporan', how='left')
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

# 4. Load
print("4. Loading ke file CSV...")
if not os.path.exists('Star_Schema'):
    os.makedirs('Star_Schema')

dim_waktu.to_csv('Star_Schema/Dim_Waktu.csv', index=False)
dim_univ.to_csv('Star_Schema/Dim_Universitas.csv', index=False)
dim_prodi.to_csv('Star_Schema/Dim_Prodi.csv', index=False)
fact_table.to_csv('Star_Schema/Fact_Kapasitas_Pendidikan.csv', index=False)

print("✅ Proses ETL Selesai! Data Star Schema di-load ke folder 'Star_Schema'.")
