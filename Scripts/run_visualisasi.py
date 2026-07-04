import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

ROOT        = r'd:\Code\Tugas Akhir'
PATH_MASTER = os.path.join(ROOT, 'Data', 'Processed', 'master_looker_unsil.csv')
PATH_VIZ    = os.path.join(ROOT, 'Outputs', 'Visualizations')
os.makedirs(PATH_VIZ, exist_ok=True)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'axes.titlesize': 13, 'axes.titleweight': 'bold',
                     'figure.dpi': 120})
COLORS = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd']
PERIOD_ORDER = ['Ganjil 2023','Genap 2023','Ganjil 2024','Genap 2024','Ganjil 2025']

df = pd.read_csv(PATH_MASTER)
df['tahun_pelaporan'] = pd.Categorical(df['tahun_pelaporan'], categories=PERIOD_ORDER, ordered=True)
df = df.sort_values('tahun_pelaporan')
print("Data loaded:", len(df), "baris |", df['nama_program_studi'].nunique(), "prodi |", df['tahun_pelaporan'].nunique(), "periode")
print("NaN nilai_rasio:", df['nilai_rasio'].isna().sum(), "baris (prodi 0 mahasiswa, dikecualikan dari rata-rata)")

# ============================================================
# GRAFIK 1: Tren Institusi (3 panel)
# ============================================================
print("\nMembuat Grafik 1: Tren Institusi...")
inst = df.groupby('tahun_pelaporan', observed=True).agg(
    total_mahasiswa=('jumlah_mahasiswa','sum'),
    total_dosen=('total_dosen','sum'),
    rata_rasio=('nilai_rasio','mean')
).reset_index()

print("Tabel Tren Institusi:")
inst_display = inst.copy()
inst_display['rata_rasio'] = inst_display['rata_rasio'].round(2)
print(inst_display.to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Tren Tingkat Institusi - Universitas Siliwangi', fontsize=15, fontweight='bold', y=1.02)

ax = axes[0]
ax.plot(range(len(inst)), inst['rata_rasio'], marker='o', color=COLORS[0], linewidth=2.5, markersize=8)
ax.axhline(y=45, color='red', linestyle='--', linewidth=1.5, label='Batas Dikti Sosial (1:45)')
ax.axhline(y=30, color='orange', linestyle=':', linewidth=1.5, label='Batas Dikti Sains (1:30)')
ax.set_title('Tren Rata-Rata Rasio Dosen:Mahasiswa')
ax.set_ylabel('Nilai Rasio (1:x)')
ax.set_xticks(range(len(inst)))
ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
for i, v in enumerate(inst['rata_rasio']):
    ax.annotate("%.1f" % v, (i, v), textcoords='offset points', xytext=(0,8), ha='center', fontsize=9)

ax = axes[1]
bars = ax.bar(range(len(inst)), inst['total_mahasiswa'], color=COLORS[1], edgecolor='white')
ax.set_title('Total Mahasiswa Aktif per Semester')
ax.set_ylabel('Jumlah Mahasiswa')
ax.set_xticks(range(len(inst)))
ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax.grid(True, axis='y', alpha=0.3)
for bar, v in zip(bars, inst['total_mahasiswa']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50, '%d' % int(v), ha='center', va='bottom', fontsize=9)

ax = axes[2]
bars = ax.bar(range(len(inst)), inst['total_dosen'], color=COLORS[2], edgecolor='white')
ax.set_title('Total Dosen Tetap per Semester')
ax.set_ylabel('Jumlah Dosen')
ax.set_xticks(range(len(inst)))
ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
ax.grid(True, axis='y', alpha=0.3)
for bar, v in zip(bars, inst['total_dosen']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, '%d' % int(v), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
out1 = os.path.join(PATH_VIZ, 'viz_institusi.png')
plt.savefig(out1, bbox_inches='tight', dpi=150)
plt.close()
print("SAVED:", out1)

# ============================================================
# GRAFIK 2: Heatmap
# ============================================================
print("\nMembuat Grafik 2: Heatmap Prodi x Semester...")
pivot = df.pivot_table(index='nama_program_studi', columns='tahun_pelaporan',
                       values='nilai_rasio', aggfunc='mean', observed=True)
pivot = pivot.reindex(columns=PERIOD_ORDER)
pivot = pivot.sort_values(PERIOD_ORDER[-1], ascending=False)

fig, ax = plt.subplots(figsize=(12, max(8, len(pivot)*0.4)))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r', linewidths=0.3,
            cbar_kws={'label':'Nilai Rasio (1:x)'}, ax=ax, vmin=0, vmax=45)
ax.set_title('Heatmap Rasio Dosen:Mahasiswa per Program Studi x Semester\nUniversitas Siliwangi', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Periode Pelaporan', fontweight='bold')
ax.set_ylabel('Program Studi', fontweight='bold')
ax.tick_params(axis='x', rotation=30)
ax.tick_params(axis='y', rotation=0)
plt.tight_layout()
out2 = os.path.join(PATH_VIZ, 'heatmap_prodi_semester.png')
plt.savefig(out2, bbox_inches='tight', dpi=150)
plt.close()
print("SAVED:", out2)

# ============================================================
# GRAFIK 3: Bar Prodi Terbaru — 3-tier batas (Sains 1:30, Sosial 1:45)
# ============================================================
print("\nMembuat Grafik 3: Bar Chart Prodi Ganjil 2025...")
latest = PERIOD_ORDER[-1]
df_latest = df[df['tahun_pelaporan']==latest].copy()
df_latest = df_latest.groupby('nama_program_studi', observed=True)['nilai_rasio'].mean().reset_index()
df_latest = df_latest.dropna(subset=['nilai_rasio'])
df_latest = df_latest.sort_values('nilai_rasio', ascending=True)

fig, ax = plt.subplots(figsize=(10, max(8, len(df_latest)*0.35)))
colors = ['#d62728' if v > 45 else '#ff7f0e' if v > 30 else '#1f77b4' for v in df_latest['nilai_rasio']]
bars = ax.barh(df_latest['nama_program_studi'], df_latest['nilai_rasio'], color=colors, edgecolor='white')
ax.axvline(x=45, color='red', linestyle='--', linewidth=2, label='Batas Sosial/Humaniora (1:45) — Permendikbud No.3/2020')
ax.axvline(x=30, color='orange', linestyle=':', linewidth=2, label='Batas Sains/Teknologi (1:30) — Permendikbud No.3/2020')
ax.set_title('Perbandingan Rasio Dosen:Mahasiswa per Prodi\nPeriode %s' % latest, fontweight='bold')
ax.set_xlabel('Nilai Rasio (1:x)')
ax.legend(fontsize=8)
ax.grid(True, axis='x', alpha=0.3)
for bar, v in zip(bars, df_latest['nilai_rasio']):
    ax.text(v+0.2, bar.get_y()+bar.get_height()/2, '%.1f' % v, va='center', fontsize=8)
plt.tight_layout()
out3 = os.path.join(PATH_VIZ, 'bar_rasio_prodi_terbaru.png')
plt.savefig(out3, bbox_inches='tight', dpi=150)
plt.close()
print("SAVED:", out3)

# ============================================================
# GRAFIK 4: Line Tren Top5 vs Bot5
# ============================================================
print("\nMembuat Grafik 4: Line Tren Top5 vs Bot5...")
top5 = df_latest.nlargest(5, 'nilai_rasio')['nama_program_studi'].tolist()
bot5 = df_latest.nsmallest(5, 'nilai_rasio')['nama_program_studi'].tolist()
sel  = top5 + bot5

df_sel = df[df['nama_program_studi'].isin(sel)].copy()
df_sel = df_sel.groupby(['nama_program_studi','tahun_pelaporan'], observed=True)['nilai_rasio'].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
for ax, group, title, cmap_name in zip(
    axes,
    [top5, bot5],
    ['5 Prodi Rasio TERTINGGI (Beban Terberat)', '5 Prodi Rasio TERENDAH (Beban Teringan)'],
    ['Reds', 'Blues']
):
    clist = plt.colormaps[cmap_name](np.linspace(0.4, 0.9, 5))
    for i, prodi in enumerate(group):
        sub = df_sel[df_sel['nama_program_studi']==prodi]
        ax.plot(sub['tahun_pelaporan'].astype(str), sub['nilai_rasio'],
                marker='o', label=prodi, color=clist[i], linewidth=2)
    ax.axhline(45, color='red', linestyle='--', linewidth=1.5, label='Batas Sosial (1:45)')
    ax.axhline(30, color='orange', linestyle=':', linewidth=1.5, label='Batas Sains (1:30)')
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel('Nilai Rasio (1:x)')
    ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
    ax.legend(fontsize=8, loc='best')
    ax.grid(True, alpha=0.3)

plt.suptitle('Tren Rasio Dosen:Mahasiswa - Perbandingan Prodi Ekstrem\nUniversitas Siliwangi', fontsize=13, fontweight='bold')
plt.tight_layout()
out4 = os.path.join(PATH_VIZ, 'line_tren_top5_bot5.png')
plt.savefig(out4, bbox_inches='tight', dpi=150)
plt.close()
print("SAVED:", out4)

# ============================================================
# GRAFIK 5: Dashboard Final (5 panel)
# ============================================================
print("\nMembuat Grafik 5: Dashboard Final...")
fig = plt.figure(figsize=(20, 22))
fig.patch.set_facecolor('#f8f9fa')
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)
fig.suptitle('DASHBOARD ANALITIK\nRasio Dosen:Mahasiswa Universitas Siliwangi', fontsize=18, fontweight='bold', y=0.98)

ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(range(len(inst)), inst['rata_rasio'], marker='o', color='#1f77b4', linewidth=2.5, markersize=9)
ax1.axhline(45, color='red', linestyle='--', linewidth=1.5, label='Batas Sosial (1:45)')
ax1.axhline(30, color='orange', linestyle=':', linewidth=1.5, label='Batas Sains (1:30)')
ax1.set_title('Tren Rata-Rata Rasio Institusi', pad=10)
ax1.set_xticks(range(len(inst))); ax1.set_xticklabels(PERIOD_ORDER, rotation=25, ha='right')
ax1.set_ylabel('Nilai Rasio (1:x)'); ax1.legend(fontsize=8); ax1.grid(alpha=0.3)
for i, v in enumerate(inst['rata_rasio']): ax1.annotate("%.1f" % v, (i,v), xytext=(0,8), textcoords='offset points', ha='center', fontsize=9)

ax2 = fig.add_subplot(gs[0, 1])
ax2.bar(range(len(inst)), inst['total_mahasiswa'], color='#ff7f0e', edgecolor='white')
ax2.set_title('Total Mahasiswa per Semester', pad=10)
ax2.set_xticks(range(len(inst))); ax2.set_xticklabels(PERIOD_ORDER, rotation=25, ha='right')
ax2.set_ylabel('Jumlah'); ax2.grid(alpha=0.3, axis='y')
for i, v in enumerate(inst['total_mahasiswa']): ax2.text(i, v+30, '%d' % int(v), ha='center', fontsize=9)

ax3 = fig.add_subplot(gs[1, 0])
ax3.bar(range(len(inst)), inst['total_dosen'], color='#2ca02c', edgecolor='white')
ax3.set_title('Total Dosen per Semester', pad=10)
ax3.set_xticks(range(len(inst))); ax3.set_xticklabels(PERIOD_ORDER, rotation=25, ha='right')
ax3.set_ylabel('Jumlah'); ax3.grid(alpha=0.3, axis='y')
for i, v in enumerate(inst['total_dosen']): ax3.text(i, v+1, '%d' % int(v), ha='center', fontsize=9)

ax4 = fig.add_subplot(gs[1, 1])
top10 = df_latest.nlargest(10, 'nilai_rasio')
clrs  = ['#d62728' if v > 45 else '#ff7f0e' if v > 30 else '#1f77b4' for v in top10['nilai_rasio']]
ax4.barh(top10['nama_program_studi'], top10['nilai_rasio'], color=clrs)
ax4.axvline(45, color='red', linestyle='--', linewidth=1.5, label='Batas Sosial (1:45)')
ax4.axvline(30, color='orange', linestyle=':', linewidth=1.5, label='Batas Sains (1:30)')
ax4.set_title('Top 10 Prodi Rasio Tertinggi (Ganjil 2025)', pad=10)
ax4.set_xlabel('Nilai Rasio (1:x)'); ax4.grid(alpha=0.3, axis='x')
ax4.legend(fontsize=8)

ax5 = fig.add_subplot(gs[2, :])
pivot_dash = pivot.head(15)
sns.heatmap(pivot_dash, annot=True, fmt='.1f', cmap='RdYlGn_r', linewidths=0.3,
            cbar_kws={'label':'Rasio (1:x)', 'shrink':0.6}, ax=ax5, vmin=0, vmax=45)
ax5.set_title('Heatmap Rasio per Prodi x Semester (15 Tertinggi)', pad=10)
ax5.set_xlabel('Periode', fontweight='bold'); ax5.set_ylabel('')
ax5.tick_params(axis='x', rotation=20); ax5.tick_params(axis='y', rotation=0)

out5 = os.path.join(PATH_VIZ, 'dashboard_final.png')
plt.savefig(out5, bbox_inches='tight', dpi=150, facecolor=fig.get_facecolor())
plt.close()
print("SAVED:", out5)

# ============================================================
# GRAFIK 6: Sains vs Sosial — dengan kedua garis batas DIKTI
# ============================================================
print("\nMembuat Grafik 6: Perbandingan Sains vs Sosial...")
if 'rumpun_ilmu' in df.columns:
    sains_sosial = df.groupby(['tahun_pelaporan', 'rumpun_ilmu'], observed=True)['nilai_rasio'].mean().unstack()

    fig, ax = plt.subplots(figsize=(10, 6))
    if 'Sains' in sains_sosial.columns:
        ax.plot(sains_sosial.index.astype(str), sains_sosial['Sains'], marker='o', color='#2ca02c', linewidth=2.5, label='Rumpun Sains', markersize=8)
    if 'Sosial' in sains_sosial.columns:
        ax.plot(sains_sosial.index.astype(str), sains_sosial['Sosial'], marker='s', color='#1f77b4', linewidth=2.5, label='Rumpun Sosial', markersize=8)

    # Dua garis batas berbeda sesuai Permendikbud No.3 Tahun 2020
    ax.axhline(45, color='red',    linestyle='--', linewidth=1.8, label='Batas Sosial/Humaniora (1:45) — Permendikbud No.3/2020')
    ax.axhline(30, color='orange', linestyle=':',  linewidth=1.8, label='Batas Sains/Teknologi (1:30) — Permendikbud No.3/2020')

    ax.set_title('Tren Rata-Rata Rasio Dosen:Mahasiswa\nRumpun Sains vs Sosial — Universitas Siliwangi', fontweight='bold', fontsize=13)
    ax.set_ylabel('Nilai Rasio (1:x)')
    ax.set_xticklabels(PERIOD_ORDER, rotation=30, ha='right')
    ax.legend(fontsize=8.5)
    ax.grid(True, alpha=0.3)

    for col, marker_offset in zip(['Sains', 'Sosial'], [8, -15]):
        if col in sains_sosial.columns:
            for i, v in enumerate(sains_sosial[col]):
                if pd.notna(v):
                    ax.annotate("%.1f" % v, (i, v), xytext=(0, marker_offset), textcoords='offset points', ha='center', fontsize=9)

    plt.tight_layout()
    out6 = os.path.join(PATH_VIZ, 'line_tren_sains_vs_sosial.png')
    plt.savefig(out6, bbox_inches='tight', dpi=150)
    plt.close()
    print("SAVED:", out6)
else:
    print("Kolom 'rumpun_ilmu' tidak ditemukan, lewati Grafik 6.")

print()
print("=" * 60)
print("SEMUA GRAFIK SELESAI DIBUAT - TIDAK ADA ERROR")
print("=" * 60)
print("Output files:")
for f in ['viz_institusi.png','heatmap_prodi_semester.png','bar_rasio_prodi_terbaru.png','line_tren_top5_bot5.png','dashboard_final.png', 'line_tren_sains_vs_sosial.png']:
    full = os.path.join(PATH_VIZ, f)
    if os.path.exists(full):
        size = os.path.getsize(full)
        print("  %s (%.1f KB)" % (f, size/1024))
