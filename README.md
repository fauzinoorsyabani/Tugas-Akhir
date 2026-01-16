# PDDikti Scraper

Ini script buat scraping data program studi dari website PDDikti (Pangkalan Data Pendidikan Tinggi). Basically ngambil semua data prodi dari PTN-BLU se-Indonesia.

## What's This?

Script Python yang nge-scrape data program studi dari [pddikti.kemdiktisaintek.go.id](https://pddikti.kemdiktisaintek.go.id/perguruan-tinggi) using Selenium. Data yang diambil meliputi:

- Kode & Nama Program Studi
- Status & Jenjang
- Akreditasi
- Data Dosen (tetap, tidak tetap, rasio)
- Jumlah Mahasiswa
- Rasio Dosen/Mahasiswa

## Target Universities

Script ini nge-scrape **53 PTN-BLU** yang dibagi jadi 3 zona:

### Zona I (14 Universities)

ISI Surakarta, Poltek Lampung, Poltek Pontianak, Poltek Sriwijaya, Unib, Unhalu, Unja, Unila, Unram, UNG, Undana, Untad, Untan, Untidar

### Zona II (28 Universities)

Data udah ada di file `Data_PTN_BLU_Zona_II_Final.xlsx` - bakal di-merge otomatis

### Zona III (11 Universities)

Polman Bandung, Poltek Bali, Poltek Bandung, Poltek Batam, PNJ, Unmul, Unima, UPN Veteran Jakarta, UPN Veteran Yogyakarta, Unsrat, Unud

## Setup

### Requirements

```bash
pip install pandas selenium webdriver-manager openpyxl
```

### Dependencies

- Python 3.x
- Chrome Browser (karena pake ChromeDriver)
- Internet connection yang stabil

## How to Use

1. **Clone or download** file `scrape_pddikti.py`

2. **Pastikan ada file Zona II** (kalau mau merge):

   ```
   Data_PTN_BLU_Zona_II_Final.xlsx
   ```

3. **Run the script**:

   ```bash
   python scrape_pddikti.py
   ```

4. **Tunggu prosesnya** - bakal lumayan lama karena scraping 25 universitas dengan banyak halaman per universitas

5. **Check hasilnya** di file:
   - `Data_PTN_BLU_Gabungan_Final.xlsx` (hasil final gabungan semua zona)
   - `checkpoint_zona_1_3.xlsx` (auto-save progress biar ga ilang kalo crash)

## Features

- **Auto-checkpoint**: Progress ke-save otomatis per universitas (jaga-jaga kalo crash)
- **Retry mechanism**: Kalau gagal search/klik, bakal retry sampe 3x
- **Pagination handling**: Otomatis lanjut ke halaman berikutnya sampe habis
- **Data merging**: Otomatis gabungin data lama (Zona II) sama data baru
- **Error handling**: Handle stale elements, timeouts, dll

## Output Format

Excel file dengan kolom:

| Column                 | Description                    |
| ---------------------- | ------------------------------ |
| Nama Universitas       | Nama PT                        |
| Kode                   | Kode Prodi                     |
| Program Studi          | Nama Prodi                     |
| Status                 | Status Prodi                   |
| Jenjang                | D3/S1/S2/S3                    |
| Akreditasi             | Akreditasi Prodi               |
| Dosen Penghitung Rasio | Jumlah dosen untuk rasio       |
| Dosen Tetap            | Jumlah dosen tetap             |
| Dosen Tidak Tetap      | Jumlah dosen tidak tetap       |
| Total Dosen            | Total semua dosen              |
| Jumlah Mahasiswa       | Total mahasiswa aktif          |
| Rasio Dosen/Mhs        | Rasio dosen terhadap mahasiswa |

## Notes

- Script ini relatively **slow** karena harus wait buat loading page (anti-detection)
- Kalau koneksi internet lo lemot, might need to increase sleep time
- File Excel harus **ditutup** sebelum run script (biar ga permission error)
- Progress di-save real-time, jadi aman kalo tiba-tiba mati listrik or something

## Troubleshooting

**"Permission Error" waktu save Excel?**

- Tutup file Excel yang lagi kebuka
- Script bakal auto-save ke file BACKUP

**Script stuck di loading?**

- Check koneksi internet
- Mungkin website PDDikti lagi down/slow
- Increase wait time di code

**ChromeDriver error?**

- Update Chrome browser lo
- Script pake webdriver-manager, jadi auto-update kok

## Progress Tracking

Script bakal print progress real-time:

```
[1/25] Processing...
--- Memproses: Institut Seni Indonesia Surakarta ---
   Sedang mencari...
   > Halaman 1: 10 data.
   > Halaman 2: 10 data.
   ...
   ✅ Selesai: Total 45 baris.
```

## License & Disclaimer

Data scraped dari website publik PDDikti Kemdikbudristek. Use responsibly, jangan spam website-nya!

---

**Happy Scraping!**

Kalau ada issue or mau improve script, feel free to contribute or reach out!
