"""
Jalankan ini untuk menjalankan ETL dan menghasilkan semua file output:
  .venv\Scripts\python.exe run_pipeline.py
"""
import pandas as pd
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings('ignore')

ROOT       = os.path.abspath(os.path.dirname(__file__))
PROJECT    = os.path.abspath(os.path.join(ROOT, '..'))   # satu level ke atas = project root

PATH_PRODI  = os.path.join(PROJECT, 'Data', 'Processed', 'unsil_prodi_fresh.csv')
PATH_UNIV   = os.path.join(PROJECT, 'Data', 'Processed', 'unsil_univ_fresh.csv')
PATH_SCHEMA = os.path.join(PROJECT, 'Data', 'Star_Schema')
PATH_MASTER = os.path.join(PROJECT, 'Data', 'Processed', 'master_looker_unsil.csv')
PATH_VIZ    = os.path.join(PROJECT, 'Outputs', 'Visualizations')

os.makedirs(PATH_SCHEMA, exist_ok=True)
os.makedirs(PATH_VIZ, exist_ok=True)


# ─── EXTRACT ──────────────────────────────────────────────────────────────────
print("=" * 60)
print("FASE 1: EXTRACT")
print("=" * 60)

df = pd.read_csv(PATH_PRODI)
print(f"Baris mentah     : {len(df)}")
print(f"Prodi unik       : {df['nama_program_studi'].nunique()}")
print(f"Periode tersedia : {sorted(df['tahun_pelaporan'].unique())}")

# ─── TRANSFORM ────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FASE 2: TRANSFORM")
print("=" * 60)

# 1. Drop null kritis
before = len(df)
df = df.dropna(subset=['kode_prodi', 'tahun_pelaporan', 'rasio_dosen_mahasiswa'])
print(f"[1] Drop null: {before} -> {len(df)} baris")

# 2. Parsing periode
df[['semester', 'tahun']] = df['tahun_pelaporan'].str.split(' ', n=1, expand=True)
print(f"[2] Parsing periode OK")

# 3. Konversi numerik
num_cols = ['jumlah_dosen_penghitung_rasio','dosen_tetap','dosen_tidak_tetap','total_dosen','jumlah_mahasiswa']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')
print(f"[3] Konversi numerik OK")

# 4. Parse rasio string -> float
def parse_rasio(s):
    try:
        if pd.isna(s): return np.nan
        parts = str(s).split(':')
        return float(parts[1]) if len(parts) == 2 else np.nan
    except:
        return np.nan

df['nilai_rasio'] = df['rasio_dosen_mahasiswa'].apply(parse_rasio)
print(f"[4] Parse rasio OK — contoh: {df['rasio_dosen_mahasiswa'].iloc[0]} -> {df['nilai_rasio'].iloc[0]}")

# 5. Fix metadata Unsil (hardcode data resmi karena DOM PDDikti bermasalah)
df['kode_pt'] = '002008'
df['status_pt_univ'] = 'PTN'
df['akreditasi_pt_univ'] = 'Unggul'
df['nama_universitas'] = 'Universitas Siliwangi'
print(f"[5] Fix metadata Unsil: kode_pt=002008, status=PTN, akreditasi=Unggul")

print(f"\n=> Data siap: {len(df)} baris, {df['nama_program_studi'].nunique()} prodi")

# ─── LOAD: STAR SCHEMA ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FASE 3: LOAD — Star Schema")
print("=" * 60)

PERIOD_ORDER = ['Ganjil 2023','Genap 2023','Ganjil 2024','Genap 2024','Ganjil 2025']

# Dim_Waktu
dim_waktu = (df[['tahun_pelaporan','semester','tahun']]
             .drop_duplicates().sort_values('tahun_pelaporan').reset_index(drop=True))
dim_waktu.insert(0, 'id_waktu', dim_waktu.index + 1)
dim_waktu['tahun'] = dim_waktu['tahun'].astype(int)

# Dim_Universitas
dim_univ = pd.DataFrame([{
    'id_universitas': '002008',
    'nama_universitas': 'Universitas Siliwangi',
    'kota': 'Kota Tasikmalaya',
    'provinsi': 'Prov. Jawa Barat',
    'status_pt': 'PTN',
    'akreditasi_institusi': 'Unggul'
}])

# Dim_Prodi (gunakan data periode terbaru sebagai referensi)
latest_p = sorted(df['tahun_pelaporan'].unique())[-1]
df_latest_ref = df[df['tahun_pelaporan'] == latest_p]
dim_prodi = (df_latest_ref[['kode_prodi','nama_program_studi','jenjang','status_prodi','akreditasi_prodi']]
             .drop_duplicates(subset=['kode_prodi']).sort_values('nama_program_studi')
             .reset_index(drop=True).rename(columns={'kode_prodi':'id_prodi'}))

# Fact Table
fact = df.merge(dim_waktu[['id_waktu','tahun_pelaporan']], on='tahun_pelaporan', how='left')
fact_table = fact[['kode_pt','kode_prodi','id_waktu',
                   'jumlah_dosen_penghitung_rasio','dosen_tetap','dosen_tidak_tetap','total_dosen',
                   'jumlah_mahasiswa','rasio_dosen_mahasiswa','nilai_rasio']].rename(
    columns={'kode_pt':'id_universitas','kode_prodi':'id_prodi'})
fact_table = fact_table.dropna(subset=['id_universitas','id_prodi']).reset_index(drop=True)

# Simpan
dim_waktu.to_csv(os.path.join(PATH_SCHEMA, 'Dim_Waktu.csv'), index=False)
dim_univ.to_csv(os.path.join(PATH_SCHEMA, 'Dim_Universitas.csv'), index=False)
dim_prodi.to_csv(os.path.join(PATH_SCHEMA, 'Dim_Prodi.csv'), index=False)
fact_table.to_csv(os.path.join(PATH_SCHEMA, 'Fact_Kapasitas_Pendidikan.csv'), index=False)

print(f"Dim_Waktu        : {len(dim_waktu)} baris")
print(f"Dim_Universitas  : {len(dim_univ)} baris")
print(f"Dim_Prodi        : {len(dim_prodi)} baris")
print(f"Fact Table       : {len(fact_table)} baris")

# Master flat table
master = df[['tahun_pelaporan','semester','tahun','nama_program_studi','jenjang',
             'status_prodi','akreditasi_prodi','nama_universitas',
             'jumlah_mahasiswa','jumlah_dosen_penghitung_rasio','dosen_tetap',
             'dosen_tidak_tetap','total_dosen','rasio_dosen_mahasiswa','nilai_rasio']].copy()
master['kota'] = 'Kota Tasikmalaya'
master['provinsi'] = 'Prov. Jawa Barat'
master['kode_pt'] = '002008'
master = master.sort_values(['tahun_pelaporan','nama_program_studi']).reset_index(drop=True)
master.to_csv(PATH_MASTER, index=False)
print(f"master_looker    : {len(master)} baris tersimpan")

# ─── VISUALISASI ──────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FASE 4: VISUALISASI")
print("=" * 60)

import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                     'axes.titlesize':13,'axes.titleweight':'bold','figure.dpi':120})
COLORS = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd']

df_viz = pd.read_csv(PATH_MASTER)
df_viz['tahun_pelaporan'] = pd.Categorical(df_viz['tahun_pelaporan'], categories=PERIOD_ORDER, ordered=True)
df_viz = df_viz.sort_values('tahun_pelaporan')

inst = df_viz.groupby('tahun_pelaporan', observed=True).agg(
    total_mahasiswa=('jumlah_mahasiswa','sum'),
    total_dosen=('total_dosen','sum'),
    rata_rasio=('nilai_rasio','mean')
).reset_index()

latest = PERIOD_ORDER[-1]
df_lat = df_viz[df_viz['tahun_pelaporan']==latest].groupby('nama_program_studi', observed=True)['nilai_rasio'].mean().reset_index()
df_lat = df_lat.sort_values('nilai_rasio', ascending=True)

# ── 1. Visualisasi Tingkat Institusi ────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16,5))
fig.suptitle('Tren Tingkat Institusi — Universitas Siliwangi', fontsize=15, fontweight='bold')

ax = axes[0]
ax.plot(range(len(inst)), inst['rata_rasio'], marker='o', color=COLORS[0], linewidth=2.5, markersize=9)
ax.axhline(45, color='red', linestyle='--', linewidth=1.5, label='Batas Dikti (1:45)')
ax.set_title('Tren Rata-Rata Rasio'); ax.set_ylabel('Nilai Rasio (1:x)')
ax.set_xticks(range(len(inst))); ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax.legend(fontsize=9); ax.grid(alpha=0.3)
for i, v in enumerate(inst['rata_rasio']): ax.annotate(f'{v:.1f}', (i,v), xytext=(0,8), textcoords='offset points', ha='center', fontsize=9)

ax = axes[1]
bars = ax.bar(range(len(inst)), inst['total_mahasiswa'], color=COLORS[1])
ax.set_title('Total Mahasiswa per Semester'); ax.set_ylabel('Jumlah')
ax.set_xticks(range(len(inst))); ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax.grid(alpha=0.3, axis='y')
for bar, v in zip(bars, inst['total_mahasiswa']): ax.text(bar.get_x()+bar.get_width()/2, v+30, f'{int(v):,}', ha='center', fontsize=9)

ax = axes[2]
bars = ax.bar(range(len(inst)), inst['total_dosen'], color=COLORS[2])
ax.set_title('Total Dosen per Semester'); ax.set_ylabel('Jumlah')
ax.set_xticks(range(len(inst))); ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax.grid(alpha=0.3, axis='y')
for bar, v in zip(bars, inst['total_dosen']): ax.text(bar.get_x()+bar.get_width()/2, v+1, f'{int(v):,}', ha='center', fontsize=9)

plt.tight_layout()
p = os.path.join(PATH_VIZ, 'viz_institusi.png')
plt.savefig(p, bbox_inches='tight', dpi=150); plt.close()
print(f"[SAVED] {p}")

# ── 2. Heatmap ──────────────────────────────────────────────────────────────
pivot = df_viz.pivot_table(index='nama_program_studi', columns='tahun_pelaporan',
                           values='nilai_rasio', aggfunc='mean', observed=True)
pivot = pivot.reindex(columns=PERIOD_ORDER).sort_values(PERIOD_ORDER[-1], ascending=False)

fig, ax = plt.subplots(figsize=(12, max(8, len(pivot)*0.45)))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r', linewidths=0.3,
            cbar_kws={'label':'Nilai Rasio (1:x)'}, ax=ax, vmin=0, vmax=45)
ax.set_title('Heatmap Rasio Dosen:Mahasiswa per Program Studi x Semester\nUniversitas Siliwangi', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Periode'); ax.set_ylabel('Program Studi')
ax.tick_params(axis='x', rotation=30); ax.tick_params(axis='y', rotation=0)
plt.tight_layout()
p = os.path.join(PATH_VIZ, 'heatmap_prodi_semester.png')
plt.savefig(p, bbox_inches='tight', dpi=150); plt.close()
print(f"[SAVED] {p}")

# ── 3. Bar chart prodi terbaru (3-tier: Sains 1:30, Sosial 1:45) ─────────────
fig, ax = plt.subplots(figsize=(10, max(8, len(df_lat)*0.38)))
clrs = ['#d62728' if v > 45 else '#ff7f0e' if v > 30 else '#1f77b4' for v in df_lat['nilai_rasio']]
bars = ax.barh(df_lat['nama_program_studi'], df_lat['nilai_rasio'], color=clrs, edgecolor='white')
ax.axvline(x=45, color='red',    linestyle='--', linewidth=2, label='Batas Sosial/Humaniora (1:45) — Permendikbud No.3/2020')
ax.axvline(x=30, color='orange', linestyle=':',  linewidth=2, label='Batas Sains/Teknologi (1:30) — Permendikbud No.3/2020')
ax.set_title(f'Perbandingan Rasio Dosen:Mahasiswa per Prodi\nPeriode {latest}', fontweight='bold')
ax.set_xlabel('Nilai Rasio (1:x)')
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='x')
for bar, v in zip(bars, df_lat['nilai_rasio']): ax.text(v+0.2, bar.get_y()+bar.get_height()/2, f'{v:.1f}', va='center', fontsize=8)
plt.tight_layout()
p = os.path.join(PATH_VIZ, 'bar_rasio_prodi_terbaru.png')
plt.savefig(p, bbox_inches='tight', dpi=150); plt.close()
print(f"[SAVED] {p}")

# ── 4. Line tren top5 vs bottom5 ────────────────────────────────────────────
top5 = df_lat.nlargest(5,'nilai_rasio')['nama_program_studi'].tolist()
bot5 = df_lat.nsmallest(5,'nilai_rasio')['nama_program_studi'].tolist()
df_sel = df_viz[df_viz['nama_program_studi'].isin(top5+bot5)].groupby(
    ['nama_program_studi','tahun_pelaporan'], observed=True)['nilai_rasio'].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16,6))
clr_r = plt.cm.Reds(np.linspace(0.4,0.9,5))
clr_b = plt.cm.Blues(np.linspace(0.4,0.9,5))
for ax, grp, title, clrmap in zip(axes, [top5,bot5],
    ['5 Prodi Rasio Tertinggi','5 Prodi Rasio Terendah'], [clr_r,clr_b]):
    for i, pr in enumerate(grp):
        sub = df_sel[df_sel['nama_program_studi']==pr]
        ax.plot(sub['tahun_pelaporan'].astype(str), sub['nilai_rasio'], marker='o',
                label=pr, color=clrmap[i], linewidth=2)
    ax.axhline(45, color='red', linestyle='--', linewidth=1.5, label='Batas Dikti')
    ax.set_title(title, fontweight='bold'); ax.set_ylabel('Nilai Rasio (1:x)')
    ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

plt.suptitle('Tren Rasio — Perbandingan Prodi Tertinggi vs Terendah\nUniversitas Siliwangi', fontsize=13, fontweight='bold')
plt.tight_layout()
p = os.path.join(PATH_VIZ, 'line_tren_top5_bot5.png')
plt.savefig(p, bbox_inches='tight', dpi=150); plt.close()
print(f"[SAVED] {p}")

# ── 5. Dashboard Final ───────────────────────────────────────────────────────
fig = plt.figure(figsize=(20,22))
fig.patch.set_facecolor('#f8f9fa')
gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.5, wspace=0.35)
fig.suptitle('DASHBOARD ANALITIK\nRasio Dosen:Mahasiswa Universitas Siliwangi',
             fontsize=18, fontweight='bold', y=0.98)

ax1 = fig.add_subplot(gs[0,0])
ax1.plot(range(len(inst)), inst['rata_rasio'], marker='o', color='#1f77b4', linewidth=2.5, markersize=9)
ax1.axhline(45, color='red', linestyle='--', linewidth=1.5, label='Batas Dikti')
ax1.set_title('Tren Rata-Rata Rasio Institusi')
ax1.set_xticks(range(len(inst))); ax1.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax1.set_ylabel('Nilai Rasio (1:x)'); ax1.legend(fontsize=9); ax1.grid(alpha=0.3)
for i, v in enumerate(inst['rata_rasio']): ax1.annotate(f'{v:.1f}', (i,v), xytext=(0,8), textcoords='offset points', ha='center', fontsize=9)

ax2 = fig.add_subplot(gs[0,1])
bars = ax2.bar(range(len(inst)), inst['total_mahasiswa'], color='#ff7f0e')
ax2.set_title('Total Mahasiswa per Semester')
ax2.set_xticks(range(len(inst))); ax2.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax2.set_ylabel('Jumlah'); ax2.grid(alpha=0.3, axis='y')
for bar, v in zip(bars, inst['total_mahasiswa']): ax2.text(bar.get_x()+bar.get_width()/2, v+30, f'{int(v):,}', ha='center', fontsize=9)

ax3 = fig.add_subplot(gs[1,0])
bars = ax3.bar(range(len(inst)), inst['total_dosen'], color='#2ca02c')
ax3.set_title('Total Dosen per Semester')
ax3.set_xticks(range(len(inst))); ax3.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax3.set_ylabel('Jumlah'); ax3.grid(alpha=0.3, axis='y')
for bar, v in zip(bars, inst['total_dosen']): ax3.text(bar.get_x()+bar.get_width()/2, v+1, f'{int(v):,}', ha='center', fontsize=9)

ax4 = fig.add_subplot(gs[1,1])
top10 = df_lat.nlargest(10,'nilai_rasio')
clrs_10 = ['#d62728' if v > 45 else '#1f77b4' for v in top10['nilai_rasio']]
ax4.barh(top10['nama_program_studi'], top10['nilai_rasio'], color=clrs_10)
ax4.axvline(45, color='red', linestyle='--', linewidth=1.5)
ax4.set_title(f'Top 10 Rasio Tertinggi — {latest}')
ax4.set_xlabel('Nilai Rasio (1:x)'); ax4.grid(alpha=0.3, axis='x')

ax5 = fig.add_subplot(gs[2,:])
pivot_top = pivot.head(15)
sns.heatmap(pivot_top, annot=True, fmt='.1f', cmap='RdYlGn_r', linewidths=0.3,
            cbar_kws={'label':'Rasio (1:x)','shrink':0.6}, ax=ax5, vmin=0, vmax=45)
ax5.set_title('Heatmap Rasio per Prodi x Semester (15 Tertinggi)')
ax5.set_xlabel('Periode', fontweight='bold'); ax5.set_ylabel('')
ax5.tick_params(axis='x', rotation=25); ax5.tick_params(axis='y', rotation=0)

plt.savefig(os.path.join(PATH_VIZ,'dashboard_final.png'), bbox_inches='tight', dpi=150, facecolor=fig.get_facecolor())
plt.close()
print(f"[SAVED] {os.path.join(PATH_VIZ,'dashboard_final.png')}")

# ─── TABEL ANALISIS ───────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FASE 5: TABEL ANALISIS")
print("=" * 60)

df_rank = df_viz[df_viz['tahun_pelaporan']==latest].groupby('nama_program_studi', observed=True).agg(
    jenjang=('jenjang','first'),
    akreditasi=('akreditasi_prodi','first'),
    total_dosen=('total_dosen','mean'),
    jumlah_mahasiswa=('jumlah_mahasiswa','mean'),
    nilai_rasio=('nilai_rasio','mean')
).reset_index()
df_rank['rasio_fmt'] = df_rank['nilai_rasio'].apply(lambda x: f'1:{x:.2f}')
df_rank['status_dikti'] = df_rank['nilai_rasio'].apply(lambda x: 'MELEBIHI BATAS' if x > 45 else 'Normal')
df_rank = df_rank.sort_values('nilai_rasio', ascending=False).reset_index(drop=True)
df_rank.index += 1

print(f"\n[TABEL] Ranking Prodi — Periode {latest}:")
print(df_rank[['nama_program_studi','jenjang','akreditasi','total_dosen','jumlah_mahasiswa','rasio_fmt','status_dikti']].to_string())

pelanggaran = df_rank[df_rank['nilai_rasio'] > 45]
print(f"\n[TABEL] Prodi Melebihi Batas Dikti (>1:45): {len(pelanggaran)} prodi")
if len(pelanggaran) > 0:
    print(pelanggaran[['nama_program_studi','jenjang','rasio_fmt']].to_string())

# Simpan tabel ke CSV
df_rank.to_csv(os.path.join(ROOT, 'Outputs', 'tabel_ranking_prodi.csv'), index=True)
print(f"\n[SAVED] {os.path.join(ROOT, 'Outputs', 'tabel_ranking_prodi.csv')}")

print("\n" + "=" * 60)
print("PIPELINE SELESAI!")
print("=" * 60)
print(f"Data : {PATH_MASTER}")
print(f"Star Schema : {PATH_SCHEMA}/")
print(f"Visualisasi : {PATH_VIZ}/")
