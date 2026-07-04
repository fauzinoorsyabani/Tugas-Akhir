import json, os

NB_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(".")), "Code", "Tugas Akhir", "Notebooks", "Dashboard_Visualisasi.ipynb"))
NB_PATH = r"d:\Code\Tugas Akhir\Notebooks\Dashboard_Visualisasi.ipynb"

with open(NB_PATH, encoding="utf-8") as f:
    nb = json.load(f)

nb["cells"][2]["source"] = [
    "# LOCAL MODE\n",
    "print(\"Mode: Lokal\")"
]

nb["cells"][4]["source"] = [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.gridspec as gridspec\n",
    "import seaborn as sns\n",
    "import os, warnings\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "\n",
    "ROOT     = r\"d:\\Code\\Tugas Akhir\"\n",
    "PATH_CSV = os.path.join(ROOT, \"Data\", \"Processed\", \"master_looker_unsil.csv\")\n",
    "PATH_VIZ = os.path.join(ROOT, \"Outputs\", \"Visualizations\")\n",
    "os.makedirs(PATH_VIZ, exist_ok=True)\n",
    "\n",
    "PERIOD_ORDER = [\"Ganjil 2023\", \"Genap 2023\", \"Ganjil 2024\", \"Genap 2024\", \"Ganjil 2025\"]\n",
    "COLORS = [\"#1f77b4\", \"#ff7f0e\", \"#2ca02c\", \"#d62728\", \"#9467bd\"]\n",
    "\n",
    "df = pd.read_csv(PATH_CSV)\n",
    "df[\"tahun_pelaporan\"] = pd.Categorical(df[\"tahun_pelaporan\"], categories=PERIOD_ORDER, ordered=True)\n",
    "df = df.sort_values(\"tahun_pelaporan\")\n",
    "\n",
    "print(f\"Data loaded: {len(df)} baris | {df.nama_program_studi.nunique()} prodi | {df.tahun_pelaporan.nunique()} periode\")\n",
    "print(f\"Kolom baru: {[c for c in df.columns if c in ['fakultas','rumpun_ilmu']]}\")\n",
    "print(f\"NaN rasio: {df.nilai_rasio.isna().sum()} baris\")"
]

src10 = "".join(nb["cells"][10]["source"])
src10 = src10.replace(
    "plt.cm.Reds(np.linspace(0.4,0.9,5)), plt.cm.Blues(np.linspace(0.4,0.9,5))",
    "plt.colormaps[\"Reds\"](np.linspace(0.4,0.9,5)), plt.colormaps[\"Blues\"](np.linspace(0.4,0.9,5))"
)
nb["cells"][10]["source"] = [src10]

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook patched OK.")
