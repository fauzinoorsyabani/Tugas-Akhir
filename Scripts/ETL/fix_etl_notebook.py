"""
Script untuk memperbaiki ETL_Star_Schema.ipynb:
1. Tambah cell "Langkah 0: Filter Scope" (filter data ke Universitas Siliwangi saja)
2. Fix cell Dim_Universitas: hardcode Kota Tasikmalaya, Prov. Jawa Barat

Jalankan: python Scripts/ETL/fix_etl_notebook.py
"""
import json
import os
import copy

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NB_PATH = os.path.join(ROOT, "Notebooks", "ETL_Star_Schema.ipynb")
NB_OUT  = os.path.join(ROOT, "Notebooks", "ETL_Star_Schema.ipynb")

print(f"Membaca: {NB_PATH}")
with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# ─── 1. Temukan index cell yang akan dimodifikasi ──────────────────────────────

idx_raw_stats    = None  # cell setelah ini akan ditambahkan filter scope
idx_transform_md = None  # markdown "## 2. TRANSFORM" → akan diganti
idx_transform_1  = None  # code cell transform → baris pertama "df = df_prodi_raw.copy()" akan diganti
idx_dim_univ     = None  # cell Dim_Universitas → akan di-replace

for i, cell in enumerate(cells):
    cid = cell.get("id", "")
    if cid == "cell-raw-stats":
        idx_raw_stats = i
    if cid == "transform-md":
        idx_transform_md = i
    if cid == "cell-transform-1":
        idx_transform_1 = i
    if cid == "cell-dim-univ":
        idx_dim_univ = i

print(f"  cell-raw-stats   @ index {idx_raw_stats}")
print(f"  transform-md     @ index {idx_transform_md}")
print(f"  cell-transform-1 @ index {idx_transform_1}")
print(f"  cell-dim-univ    @ index {idx_dim_univ}")

assert all(x is not None for x in [idx_raw_stats, idx_transform_md, idx_transform_1, idx_dim_univ]), \
    "Gagal menemukan satu atau lebih cell target. Cek ID cell di notebook."

# ─── 2. Buat cell baru: Markdown pengantar Transform ──────────────────────────

new_md_transform = {
    "cell_type": "markdown",
    "id": "transform-md",
    "metadata": {},
    "source": [
        "---\n",
        "## 2. TRANSFORM — Cleaning & Normalisasi\n",
        "\n",
        "Sebelum transformasi utama, dilakukan **penyaringan cakupan (*scope filtering*)**\n",
        "untuk membatasi data hanya pada Universitas Siliwangi.\n",
        "Hal ini diperlukan karena data mentah mencakup seluruh PTN BLU sebagai sumber yang lebih luas.\n",
        "\n",
        "Tahap transformasi terdiri atas:\n",
        "0. **Filter scope** — ambil hanya data Universitas Siliwangi\n",
        "1. Hapus baris dengan data kritis yang kosong\n",
        "2. Parsing kolom `tahun_pelaporan` → `semester` + `tahun`\n",
        "3. Konversi kolom numerik (`jumlah_mahasiswa`, `total_dosen`, dll.)\n",
        "4. Parsing kolom `rasio_dosen_mahasiswa` → nilai numerik `nilai_rasio`\n",
        "5. Standarisasi metadata universitas (kode_pt, status, akreditasi)"
    ]
}

# ─── 3. Buat cell baru: Code filter scope ─────────────────────────────────────

new_code_filter = {
    "cell_type": "code",
    "execution_count": None,
    "id": "cell-filter-scope",
    "metadata": {},
    "outputs": [],
    "source": [
        "# ── LANGKAH 0: Filter scope penelitian → Universitas Siliwangi ──────────────\n",
        "print('=' * 60)\n",
        "print('LANGKAH 0: FILTER SCOPE — Universitas Siliwangi')\n",
        "print('=' * 60)\n",
        "\n",
        "df = df_prodi_raw.copy()\n",
        "\n",
        "total_sebelum = len(df)\n",
        "univ_sebelum  = df['nama_universitas'].nunique() if 'nama_universitas' in df.columns else '?'\n",
        "\n",
        "# Filter: hanya baris yang nama_universitas mengandung 'Siliwangi'\n",
        "df = df[\n",
        "    df['nama_universitas'].str.contains('Siliwangi', case=False, na=False)\n",
        "].copy()\n",
        "\n",
        "# Hardcode kode_pt resmi Unsil (antisipasi inkonsistensi DOM scraping PDDikti)\n",
        "df['kode_pt'] = '002008'\n",
        "\n",
        "print(f'Data masuk  : {total_sebelum:,} baris | {univ_sebelum} universitas')\n",
        "print(f'Data keluar : {len(df):,} baris | {df[\"nama_program_studi\"].nunique()} prodi unik')\n",
        "print(f'Universitas : {df[\"nama_universitas\"].unique()}')\n",
        "print(f'Periode     : {sorted(df[\"tahun_pelaporan\"].unique())}')\n",
        "print('\\n[OK] Filter scope selesai — data sudah dibatasi ke Universitas Siliwangi.')"
    ]
}

# ─── 4. Buat cell markdown pemisah sebelum Langkah 1–5 ───────────────────────

new_md_steps = {
    "cell_type": "markdown",
    "id": "transform-steps-md",
    "metadata": {},
    "source": [
        "### Langkah 1–5: Cleaning & Normalisasi"
    ]
}

# ─── 5. Fix cell transform-1: hapus baris "df = df_prodi_raw.copy()" ──────────

cell_transform = cells[idx_transform_1]
new_source = []
for line in cell_transform["source"]:
    if line.strip() == "df = df_prodi_raw.copy()":
        # Ganti dengan komentar yang menjelaskan df sudah dari Langkah 0
        new_source.append("# df sudah difilter ke Unsil di Langkah 0 (cell-filter-scope)\n")
    else:
        new_source.append(line)
cell_transform["source"] = new_source
print("  [OK] cell-transform-1: baris 'df = df_prodi_raw.copy()' diganti komentar")

# ─── 6. Fix cell-dim-univ: hardcode data resmi Unsil ─────────────────────────

cells[idx_dim_univ]["source"] = [
    "# Dim_Universitas — hardcode data resmi Unsil\n",
    "# Alasan: data kota/provinsi dari scraping DOM PDDikti tidak reliabel\n",
    "# (df_univ_raw.iloc[0] bisa berisi PT lain jika CSV berisi data nasional PTN BLU)\n",
    "dim_univ = pd.DataFrame([{\n",
    "    'id_universitas'      : '002008',\n",
    "    'nama_universitas'    : 'Universitas Siliwangi',\n",
    "    'kota'               : 'Kota Tasikmalaya',\n",
    "    'provinsi'           : 'Prov. Jawa Barat',\n",
    "    'status_pt'          : 'PTN',\n",
    "    'akreditasi_institusi': 'Unggul'\n",
    "}])\n",
    "\n",
    "print('[Dim_Universitas] — data resmi Universitas Siliwangi')\n",
    "display(dim_univ)"
]
print("  [OK] cell-dim-univ: Dim_Universitas di-hardcode ke data resmi Unsil")

# ─── 7. Susun ulang cells: sisipkan 3 cell baru setelah cell-raw-stats ────────
# Hapus cell transform-md lama (akan diganti dengan yang baru)

cells_new = []
for i, cell in enumerate(cells):
    if i == idx_raw_stats:
        cells_new.append(cell)
        # Sisipkan setelah cell-raw-stats:
        cells_new.append(new_md_transform)   # Markdown "## 2. TRANSFORM"
        cells_new.append(new_code_filter)    # Code filter scope
        cells_new.append(new_md_steps)       # Markdown "### Langkah 1–5"
    elif cell.get("id") == "transform-md":
        pass  # Skip cell transform-md lama (sudah diganti di atas)
    else:
        cells_new.append(cell)

nb["cells"] = cells_new

# ─── 8. Simpan ────────────────────────────────────────────────────────────────

with open(NB_OUT, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\nNotebook berhasil diperbarui: {NB_OUT}")
print("   Perubahan:")
print("   1. Ditambahkan cell 'Langkah 0: Filter Scope' (filter ke Universitas Siliwangi)")
print("   2. Dim_Universitas di-hardcode: Kota Tasikmalaya, Prov. Jawa Barat")
print("   3. Baris 'df = df_prodi_raw.copy()' di Transform diganti komentar")
print("\n   Selanjutnya: upload ulang notebook ke Google Colab dan jalankan Run All.")
