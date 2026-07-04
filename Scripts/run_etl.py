import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

ROOT = r'd:\Code\Tugas Akhir'
PATH_RAW_PRODI  = os.path.join(ROOT, 'Data', 'Processed', 'unsil_prodi_fresh.csv')
PATH_RAW_UNIV   = os.path.join(ROOT, 'Data', 'Processed', 'unsil_univ_fresh.csv')
PATH_OUT_SCHEMA = os.path.join(ROOT, 'Data', 'Star_Schema')
PATH_OUT_MASTER = os.path.join(ROOT, 'Data', 'Processed', 'master_looker_unsil.csv')
os.makedirs(PATH_OUT_SCHEMA, exist_ok=True)

# ============================================================
# EXTRACT
# ============================================================
print("=" * 60)
print("TAHAP EXTRACT")
print("=" * 60)
df_prodi_raw = pd.read_csv(PATH_RAW_PRODI)
df_univ_raw  = pd.read_csv(PATH_RAW_UNIV)
print("File prodi   :", len(df_prodi_raw), "baris")
print("Kolom        :", df_prodi_raw.columns.tolist())
print("Periode      :", sorted(df_prodi_raw['tahun_pelaporan'].unique()))
print("Prodi unik   :", df_prodi_raw['nama_program_studi'].nunique())
print("File univ    :", len(df_univ_raw), "baris")

# ============================================================
# TRANSFORM
# ============================================================
print()
print("=" * 60)
print("TAHAP TRANSFORM")
print("=" * 60)

df = df_prodi_raw.copy()
total_sebelum = len(df)

# Langkah 0: filter Universitas Siliwangi
df = df[df['nama_universitas'].str.contains('Siliwangi', case=False, na=False)].copy()
df['kode_pt'] = '002008'
print("[0] Filter scope:", total_sebelum, "->", len(df), "baris |", df['nama_program_studi'].nunique(), "prodi unik")

# Langkah 1: hapus null kritis
before = len(df)
df = df.dropna(subset=['kode_prodi', 'tahun_pelaporan', 'rasio_dosen_mahasiswa'])
print("[1] Drop null kritis:", before, "->", len(df), "baris")

# Langkah 2: parsing tahun_pelaporan
df[['semester', 'tahun']] = df['tahun_pelaporan'].str.split(' ', n=1, expand=True)
print("[2] Parsing periode:", sorted(df['tahun_pelaporan'].unique()))

# Langkah 3: konversi numerik
num_cols = ['jumlah_dosen_penghitung_rasio','dosen_tetap','dosen_tidak_tetap','total_dosen','jumlah_mahasiswa']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
print("[3] Konversi numerik: OK")

# Langkah 4: parsing rasio
def parse_rasio(s):
    try:
        if pd.isna(s): return np.nan
        parts = str(s).split(':')
        return float(parts[1]) if len(parts) == 2 else np.nan
    except:
        return np.nan

df['nilai_rasio'] = df['rasio_dosen_mahasiswa'].apply(parse_rasio)
n_nan = df['nilai_rasio'].isna().sum()
print("[4] Parse rasio:", len(df)-n_nan, "baris OK,", n_nan, "baris NaN")

# Langkah 5: standarisasi metadata
df['nama_universitas']   = 'Universitas Siliwangi'
df['status_pt_univ']     = 'PTN'
df['akreditasi_pt_univ'] = 'Unggul'
df['kode_pt']            = '002008'
print("[5] Standarisasi metadata: OK")

# Langkah 6: Mapping Fakultas dan Rumpun Ilmu
FAKULTAS_MAP = {
    'Agribisnis': ('Faperta', 'Sains'),
    'Agroteknologi': ('Faperta', 'Sains'),
    'Akuntansi': ('FEB', 'Sosial'),
    'Ekonomi Pembangunan': ('FEB', 'Sosial'),
    'Ekonomi Syari\'ah': ('FEB', 'Sosial'),
    'Gizi': ('FIK', 'Sains'),
    'Ilmu Manajemen': ('FEB', 'Sosial'),
    'Ilmu Pertanian': ('Faperta', 'Sains'),
    'Ilmu Politik': ('FISIP', 'Sosial'),
    'Informatika': ('FT', 'Sains'),
    'Kesehatan Masyarakat': ('FIK', 'Sains'),
    'Manajemen': ('FEB', 'Sosial'),
    'Manajemen Mutu Halal': ('FEB', 'Sosial'),
    'Pendidikan': ('FKIP', 'Sosial'),
    'Pendidikan Bahasa Indonesia': ('FKIP', 'Sosial'),
    'Pendidikan Bahasa Inggris': ('FKIP', 'Sosial'),
    'Pendidikan Biologi': ('FKIP', 'Sains'),
    'Pendidikan Ekonomi': ('FKIP', 'Sosial'),
    'Pendidikan Fisika': ('FKIP', 'Sains'),
    'Pendidikan Geografi': ('FKIP', 'Sosial'),
    'Pendidikan Ilmu Pengetahuan Alam': ('FKIP', 'Sains'),
    'Pendidikan Jasmani': ('FKIP', 'Sosial'),
    'Pendidikan Kependudukan & Lingkungan Hidup': ('FKIP', 'Sosial'),
    'Pendidikan Masyarakat': ('FKIP', 'Sosial'),
    'Pendidikan Matematika': ('FKIP', 'Sains'),
    'Pendidikan Profesi Guru': ('FKIP', 'Sosial'),
    'Pendidikan Sejarah': ('FKIP', 'Sosial'),
    'Perbankan dan Keuangan': ('FEB', 'Sosial'),
    'Perbankan dan Keuangan Digital': ('FEB', 'Sosial'),
    'Sains Data': ('FT', 'Sains'),
    'Sistem Informasi': ('FT', 'Sains'),
    'Teknik Elektro': ('FT', 'Sains'),
    'Teknik Sipil': ('FT', 'Sains'),
    'Hukum Bisnis': ('FEB', 'Sosial'),
    'Teknologi Pangan dan Hasil Pertanian': ('Faperta', 'Sains')
}
df['fakultas'] = df['nama_program_studi'].apply(lambda x: FAKULTAS_MAP.get(x, ('Lainnya', 'Lainnya'))[0])
df['rumpun_ilmu'] = df['nama_program_studi'].apply(lambda x: FAKULTAS_MAP.get(x, ('Lainnya', 'Lainnya'))[1])
print("[6] Mapping Fakultas dan Rumpun Ilmu: OK")
print("Transformasi selesai:", len(df), "baris siap diproses.")

# ============================================================
# LOAD: Star Schema
# ============================================================
print()
print("=" * 60)
print("TAHAP LOAD")
print("=" * 60)

# Dim_Waktu
dim_waktu = (df[['tahun_pelaporan','semester','tahun']]
    .drop_duplicates().sort_values('tahun_pelaporan').reset_index(drop=True))
dim_waktu.insert(0, 'id_waktu', dim_waktu.index + 1)
dim_waktu['tahun'] = dim_waktu['tahun'].astype(int)
print("Dim_Waktu:", len(dim_waktu), "baris")
print(dim_waktu.to_string(index=False))

# Dim_Universitas
dim_univ = pd.DataFrame([{
    'id_universitas'      : '002008',
    'nama_universitas'    : 'Universitas Siliwangi',
    'kota'               : 'Kota Tasikmalaya',
    'provinsi'           : 'Prov. Jawa Barat',
    'status_pt'          : 'PTN',
    'akreditasi_institusi': 'Unggul'
}])
print("\nDim_Universitas:", len(dim_univ), "baris")
print(dim_univ.to_string(index=False))

# Dim_Prodi
latest_period = df['tahun_pelaporan'].max()
dim_prodi = (df[df['tahun_pelaporan']==latest_period]
    [['kode_prodi','nama_program_studi','fakultas','rumpun_ilmu','jenjang','status_prodi','akreditasi_prodi']]
    .drop_duplicates(subset=['kode_prodi'])
    .sort_values('nama_program_studi').reset_index(drop=True)
    .rename(columns={'kode_prodi':'id_prodi'}))
print("\nDim_Prodi:", len(dim_prodi), "program studi (referensi periode:", latest_period, ")")

# Fact Table
fact = df.merge(dim_waktu[['id_waktu','tahun_pelaporan']], on='tahun_pelaporan', how='left')
fact_table = fact[[
    'kode_pt','kode_prodi','id_waktu',
    'jumlah_dosen_penghitung_rasio','dosen_tetap','dosen_tidak_tetap','total_dosen',
    'jumlah_mahasiswa','rasio_dosen_mahasiswa','nilai_rasio'
]].rename(columns={'kode_pt':'id_universitas','kode_prodi':'id_prodi'})
fact_table = fact_table.dropna(subset=['id_universitas','id_prodi']).reset_index(drop=True)
print("Fact_Kapasitas_Pendidikan:", len(fact_table), "baris |", fact_table['id_waktu'].nunique(), "periode |", fact_table['id_prodi'].nunique(), "prodi")

# Flat table — kolom fakultas & rumpun_ilmu diletakkan di AKHIR
# agar urutan kolom lama (yang sudah ada di Google Sheets) tidak berubah
master = df[[
    'tahun_pelaporan','semester','tahun',
    'nama_program_studi','jenjang','status_prodi','akreditasi_prodi',
    'nama_universitas','jumlah_mahasiswa','jumlah_dosen_penghitung_rasio',
    'dosen_tetap','dosen_tidak_tetap','total_dosen','rasio_dosen_mahasiswa','nilai_rasio'
]].copy()
master['kota']      = 'Kota Tasikmalaya'
master['provinsi']  = 'Prov. Jawa Barat'
master['kode_pt']   = '002008'
# Tambahkan fakultas & rumpun_ilmu di akhir (kolom baru)
master['fakultas']    = df['fakultas']
master['rumpun_ilmu'] = df['rumpun_ilmu']
master = master.sort_values(['tahun_pelaporan','nama_program_studi']).reset_index(drop=True)

# Simpan semua
dim_waktu.to_csv(os.path.join(PATH_OUT_SCHEMA,'Dim_Waktu.csv'), index=False)
dim_univ.to_csv(os.path.join(PATH_OUT_SCHEMA,'Dim_Universitas.csv'), index=False)
dim_prodi.to_csv(os.path.join(PATH_OUT_SCHEMA,'Dim_Prodi.csv'), index=False)
fact_table.to_csv(os.path.join(PATH_OUT_SCHEMA,'Fact_Kapasitas_Pendidikan.csv'), index=False)
master.to_csv(PATH_OUT_MASTER, index=False)

print()
print("HASIL SIMPAN:")
for f in ['Dim_Waktu.csv','Dim_Universitas.csv','Dim_Prodi.csv','Fact_Kapasitas_Pendidikan.csv']:
    rows = pd.read_csv(os.path.join(PATH_OUT_SCHEMA,f)).shape[0]
    print("  Star_Schema/" + f + ":", rows, "baris")
rows_master = pd.read_csv(PATH_OUT_MASTER).shape[0]
print("  Processed/master_looker_unsil.csv:", rows_master, "baris")

print()
print("=" * 60)
print("TREN INSTITUSI (untuk Tabel 4.6 di BAB IV)")
print("=" * 60)
ORDER = ['Ganjil 2023','Genap 2023','Ganjil 2024','Genap 2024','Ganjil 2025']
df['tahun_pelaporan'] = pd.Categorical(df['tahun_pelaporan'], categories=ORDER, ordered=True)
inst = df.groupby('tahun_pelaporan', observed=True).agg(
    total_mahasiswa=('jumlah_mahasiswa','sum'),
    total_dosen=('total_dosen','sum'),
    rata_rasio=('nilai_rasio','mean')
).reset_index()
inst['rata_rasio'] = inst['rata_rasio'].round(2)
print(inst.to_string(index=False))

print()
print("=" * 60)
print("RANKING PRODI GANJIL 2025 (untuk Tabel 4.5 di BAB IV)")
print("=" * 60)
latest = df[df['tahun_pelaporan']=='Ganjil 2025']
rank = latest.groupby('nama_program_studi', observed=True).agg(
    jenjang=('jenjang','first'),
    dosen_penghitung=('jumlah_dosen_penghitung_rasio','mean'),
    mahasiswa=('jumlah_mahasiswa','mean'),
    rasio=('nilai_rasio','mean')
).reset_index().sort_values('rasio', ascending=False).reset_index(drop=True)
rank.index += 1
rank['rasio_fmt'] = rank['rasio'].apply(lambda x: "1:%.2f" % x if pd.notna(x) else "-")
rank['status'] = rank['rasio'].apply(lambda x: "MELEBIHI BATAS" if pd.notna(x) and x>45 else ("NaN" if pd.isna(x) else "Normal"))
print(rank[['nama_program_studi','jenjang','dosen_penghitung','mahasiswa','rasio_fmt','status']].to_string())

print()
print("=" * 60)
print("VALIDASI DATA (DATA QUALITY CHECK)")
print("=" * 60)
print("1. Validasi Total Mahasiswa Sebelum vs Sesudah ETL")
total_mhs_sebelum = pd.to_numeric(df_prodi_raw[df_prodi_raw['nama_universitas'].str.contains('Siliwangi', case=False, na=False)]['jumlah_mahasiswa'], errors='coerce').sum()
total_mhs_sesudah = df['jumlah_mahasiswa'].sum()
print(f"Total mahasiswa awal Unsil : {total_mhs_sebelum:,.0f}")
print(f"Total mahasiswa sesudah ETL: {total_mhs_sesudah:,.0f}")
if total_mhs_sebelum == total_mhs_sesudah:
    print("-> VALID! Tidak ada data mahasiswa yang hilang.")
else:
    print("-> WARNING! Ada perbedaan jumlah mahasiswa.")

print("\n2. Validasi Antar Semester (Ganjil 2023 vs Genap 2023)")
df_ganjil = df[df['tahun_pelaporan'] == 'Ganjil 2023']
df_genap = df[df['tahun_pelaporan'] == 'Genap 2023']
merged_sem = df_ganjil.merge(df_genap, on='kode_prodi', suffixes=('_ganjil', '_genap'))
if len(merged_sem) > 0:
    diff = merged_sem['jumlah_mahasiswa_ganjil'] - merged_sem['jumlah_mahasiswa_genap']
    print(f"Jumlah prodi yang divalidasi: {len(merged_sem)}")
    print(f"Total deviasi mahasiswa (Ganjil - Genap): {diff.sum():,.0f}")
    anomali = merged_sem[diff.abs() > 200]
    if len(anomali) > 0:
         print(f"-> Ditemukan {len(anomali)} prodi dengan deviasi > 200 mahasiswa:")
         for _, row in anomali.iterrows():
              print(f"   - {row['nama_program_studi_ganjil']}: Ganjil ({row['jumlah_mahasiswa_ganjil']}) vs Genap ({row['jumlah_mahasiswa_genap']})")
    else:
         print("-> VALID! Tidak ditemukan anomali deviasi signifikan antar semester yang sama.")
else:
    print("-> Tidak dapat melakukan perbandingan Ganjil vs Genap 2023.")

print()
print("ETL SELESAI - TIDAK ADA ERROR")

