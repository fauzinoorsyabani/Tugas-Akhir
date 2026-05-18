import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output dir if not exists
out_dir = 'Outputs/Visualizations'
os.makedirs(out_dir, exist_ok=True)

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# Read data
fact = pd.read_csv('Data/Star_Schema/Fact_Kapasitas_Pendidikan.csv')
dim_waktu = pd.read_csv('Data/Star_Schema/Dim_Waktu.csv')
dim_prodi = pd.read_csv('Data/Star_Schema/Dim_Prodi.csv')

# Merge
df = fact.merge(dim_waktu, on='id_waktu').merge(dim_prodi, on='id_prodi')

# 1. Total Mahasiswa per Periode
# Need to sort chronologically: Tahun, then Semester (Ganjil first, then Genap)
dim_waktu['sem_order'] = dim_waktu['semester'].map({'Ganjil': 1, 'Genap': 2})
dim_waktu = dim_waktu.sort_values(['tahun', 'sem_order'])
ordered_periods = dim_waktu['tahun_pelaporan'].tolist()

agg = df.groupby('tahun_pelaporan').agg(
    total_mhs=('jumlah_mahasiswa', 'sum'),
    total_dosen=('total_dosen', 'sum')
).reindex(ordered_periods).reset_index()

# Hitung rasio agregat
agg['rasio'] = agg['total_mhs'] / agg['total_dosen']

# Plot 1: Total Mahasiswa
plt.figure(figsize=(10, 5), dpi=300)
plt.plot(agg['tahun_pelaporan'], agg['total_mhs'], marker='o', color='blue', linewidth=2)
plt.title('Tren Jumlah Mahasiswa Aktif Universitas Siliwangi', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Total Mahasiswa Aktif')
plt.xlabel('Tahun Pelaporan (Semester)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{out_dir}/grafik_mhs_unsil.png')
plt.close()

# Plot 2: Total Dosen
plt.figure(figsize=(10, 5), dpi=300)
plt.plot(agg['tahun_pelaporan'], agg['total_dosen'], marker='s', color='green', linewidth=2)
plt.title('Tren Total Dosen Universitas Siliwangi', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Total Dosen (Tetap + Tidak Tetap)')
plt.xlabel('Tahun Pelaporan (Semester)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{out_dir}/grafik_dosen_unsil.png')
plt.close()

# Plot 3: Tren Rasio Agregat
plt.figure(figsize=(10, 5), dpi=300)
bars = plt.bar(agg['tahun_pelaporan'], agg['rasio'], color=sns.color_palette("viridis", len(agg)))

# Add horizontal lines for threshold
plt.axhline(y=45, color='red', linestyle='--', label='Batas SN-Dikti (1:45)')
plt.axhline(y=30, color='orange', linestyle='--', label='Rasional (1:30)')

plt.title('Tren Agregat Rasio Mahasiswa per Dosen (Universitas Siliwangi)', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Rasio (1 Dosen : X Mahasiswa)')
plt.xlabel('Tahun Pelaporan (Semester)')
plt.xticks(rotation=45)
plt.ylim(0, max(agg['rasio']) + 10)
plt.legend()

# Add value labels
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 1), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{out_dir}/grafik_rasio_unsil.png')
plt.close()

# Plot 4: Top 10 Prodi Rasio Tertinggi (Periode Terakhir: Ganjil 2025)
latest_period = 'Ganjil 2025'
df_latest = df[df['tahun_pelaporan'] == latest_period].copy()
df_latest = df_latest.sort_values('nilai_rasio', ascending=False).head(10)

plt.figure(figsize=(12, 6), dpi=300)
bars2 = plt.barh(df_latest['nama_program_studi'], df_latest['nilai_rasio'], color=sns.color_palette("rocket", len(df_latest)))
plt.axvline(x=45, color='red', linestyle='--', label='Batas SN-Dikti (1:45)')

plt.title(f'10 Program Studi dengan Rasio Tertinggi (Terpadat)\nPeriode: {latest_period}', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Nilai Rasio (Mahasiswa per Dosen)')
plt.ylabel('Program Studi')
plt.gca().invert_yaxis()  # Highest at top
plt.legend(loc='lower right')

for bar in bars2:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, round(width, 1), ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{out_dir}/grafik_top10_rasio_prodi.png')
plt.close()

print("✅ Semua visualisasi berhasil dibuat ulang dengan data UNSIL!")
