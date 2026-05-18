"""
Script scraping KHUSUS Universitas Siliwangi dari PDDikti.
Output: Data/Processed/unsil_prodi_fresh.csv dan Data/Processed/unsil_univ_fresh.csv

Jalankan dari root folder: .venv\Scripts\python.exe Scripts/Scraping/scrape_unsil_only.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# ─── Output paths (relatif ke root project) ───────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_UNIV  = os.path.join(ROOT, "Data", "Processed", "unsil_univ_fresh.csv")
OUT_PRODI = os.path.join(ROOT, "Data", "Processed", "unsil_prodi_fresh.csv")

TARGET_PERIODS = ["Ganjil 2025", "Genap 2024", "Ganjil 2024", "Genap 2023", "Ganjil 2023"]
UNI_NAME = "Universitas Siliwangi"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _fresh_selects(driver, wait):
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
        time.sleep(0.5)
        return driver.find_elements(By.TAG_NAME, "select")
    except:
        return []

def select_with_retry(driver, wait, idx, text, by_value=False, retries=3):
    for attempt in range(retries):
        try:
            sels = _fresh_selects(driver, wait)
            if len(sels) > idx:
                s = Select(sels[idx])
                if by_value:
                    s.select_by_value(text)
                else:
                    s.select_by_visible_text(text)
                return True
        except StaleElementReferenceException:
            time.sleep(1)
        except Exception as e:
            print(f"      ⚠ Gagal select '{text}' attempt {attempt+1}: {e}")
            time.sleep(1)
    return False

def scrape_metadata(driver, uni_name):
    """Scrape metadata universitas dari halaman detail."""
    print("  [Metadata] Mengambil data universitas...")
    kota = provinsi = kode_pt = status_pt = akreditasi = "-"

    try:
        prov_elm = driver.find_element(By.XPATH, "//*[contains(text(),'Prov.')]")
        parts = prov_elm.text.strip().split(",")
        if len(parts) >= 1: kota     = parts[0].strip()
        if len(parts) >= 2: provinsi = parts[1].strip()
    except: pass

    try:
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        for i, d in enumerate(all_divs):
            t = d.text.strip()
            if t == "Kode" and kode_pt == "-" and i+1 < len(all_divs):
                v = all_divs[i+1].text.strip()
                if len(v) <= 10: kode_pt = v
            elif t == "Status" and status_pt == "-" and i+1 < len(all_divs):
                v = all_divs[i+1].text.strip()
                if len(v) <= 20: status_pt = v
            elif t == "Akreditasi" and akreditasi == "-" and i+1 < len(all_divs):
                v = all_divs[i+1].text.strip()
                if len(v) <= 30: akreditasi = v
    except: pass

    email = website = "-"
    try:
        email = driver.find_element(By.XPATH, "//a[contains(@href,'mailto:')]").text.strip()
    except: pass
    try:
        website = driver.find_element(
            By.XPATH, "//a[contains(@href,'http') and not(contains(@href,'google'))]"
        ).text.strip()
    except: pass

    alamat = "-"
    try:
        alamat = driver.find_element(
            By.XPATH, "//*[contains(text(),'Alamat')]/following-sibling::div"
        ).text.strip()
    except: pass

    print(f"  [OK] Kode={kode_pt} | Status={status_pt} | Akreditasi={akreditasi}")
    row = [uni_name, kota, provinsi, kode_pt, status_pt, akreditasi,
           "-", "-", "-", "-", "-", email, website, alamat]
    return row, kode_pt, status_pt, akreditasi

def scrape_prodi(driver, uni_name, kode_pt, status_pt, akreditasi_pt):
    """Scrape semua prodi untuk setiap periode."""
    wait = WebDriverWait(driver, 15)
    all_rows = []

    # Tunggu tabel muncul
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
    except:
        print("  ⚠ Tabel prodi tidak ditemukan!")
        return []

    # Set tampilkan = semua
    ok = select_with_retry(driver, wait, 0, "semua", by_value=True)
    if ok:
        time.sleep(3)
    else:
        print("  ⚠ Gagal pilih 'semua', lanjut dengan default.")

    for period in TARGET_PERIODS:
        print(f"  >> Periode: {period}")

        ok = select_with_retry(driver, wait, 1, period, by_value=False)
        if not ok:
            print(f"  ⚠ Skip {period} — tidak tersedia.")
            continue
        time.sleep(4)

        page_num = 1
        period_count = 0

        while True:
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
                rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

                page_count = 0
                for r in rows:
                    try:
                        cols = r.find_elements(By.TAG_NAME, "td")
                        if len(cols) < 5:
                            continue
                        txts = [c.text.strip() for c in cols]
                        off = 1 if (len(txts[0]) <= 3 and txts[0].isdigit()) else 0

                        row_data = [
                            uni_name, kode_pt, status_pt, akreditasi_pt, period,
                            txts[0+off],   # kode_prodi
                            txts[1+off],   # nama_program_studi
                            txts[2+off],   # status_prodi
                            txts[3+off],   # jenjang
                            txts[4+off],   # akreditasi_prodi
                            txts[5+off],   # jumlah_dosen_penghitung_rasio
                            txts[6+off],   # dosen_tetap
                            txts[7+off],   # dosen_tidak_tetap
                            txts[8+off],   # total_dosen
                            txts[9+off],   # jumlah_mahasiswa
                            txts[10+off],  # rasio_dosen_mahasiswa
                        ]
                        all_rows.append(row_data)
                        page_count += 1
                    except (IndexError, StaleElementReferenceException):
                        pass

                period_count += page_count
                print(f"    Halaman {page_num}: {page_count} prodi")

            except Exception as e:
                print(f"    ⚠ Error halaman {page_num}: {e}")

            # Next page?
            has_next = False
            try:
                next_btn = driver.find_element(By.XPATH, "//button[./*[name()='svg']][last()]")
                disabled = "disabled" in (next_btn.get_attribute("class") or "")
                if next_btn.is_enabled() and not disabled:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_btn)
                    time.sleep(0.5)
                    next_btn.click()
                    time.sleep(2)
                    page_num += 1
                    has_next = True
            except: pass

            if not has_next:
                break

        print(f"  ✅ Total {period_count} prodi untuk {period}")

    return all_rows

def main():
    os.makedirs(os.path.join(ROOT, "Data", "Processed"), exist_ok=True)

    print(f"=== SCRAPING ULANG: {UNI_NAME} ===")
    print(f"Output: {OUT_UNIV}")
    print(f"        {OUT_PRODI}")
    print(f"Periode: {TARGET_PERIODS}\n")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait  = WebDriverWait(driver, 25)

    try:
        # ── Buka PDDikti ────────────────────────────────────────────────────
        driver.get("https://pddikti.kemdiktisaintek.go.id/perguruan-tinggi")

        inp = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[placeholder*='Cari Perguruan Tinggi']")
        ))
        inp.clear()
        inp.send_keys(UNI_NAME)
        time.sleep(1)
        inp.send_keys(Keys.ENTER)

        print("Mencari Universitas Siliwangi...")
        time.sleep(5)

        # ── Klik Lihat Detail ────────────────────────────────────────────────
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Lihat Detail')]")
        ))
        btns = driver.find_elements(By.XPATH, "//button[contains(text(),'Lihat Detail')]")

        target_btn = None
        # Cari card dengan "Aktif" lebih dulu
        cards = driver.find_elements(
            By.XPATH, "//div[contains(@class,'bg-white') and .//button[contains(text(),'Lihat Detail')]]"
        )
        for card in cards:
            if "Aktif" in card.text:
                target_btn = card.find_element(By.XPATH, ".//button[contains(text(),'Lihat Detail')]")
                print("Menemukan card Aktif!")
                break

        if not target_btn and btns:
            target_btn = btns[0]
            print(f"Fallback: klik tombol pertama ({len(btns)} tombol ditemukan)")

        if not target_btn:
            print("❌ Gagal menemukan tombol Lihat Detail!")
            return

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target_btn)
        time.sleep(1)
        target_btn.click()

        wait.until(EC.url_contains("detail-pt"))
        print("Masuk halaman detail PT.\n")
        time.sleep(3)

        # ── Scrape ──────────────────────────────────────────────────────────
        row_univ, kode_pt, status_pt, akreditasi_pt = scrape_metadata(driver, UNI_NAME)
        prodi_list = scrape_prodi(driver, UNI_NAME, kode_pt, status_pt, akreditasi_pt)

        # ── Simpan ──────────────────────────────────────────────────────────
        with open(OUT_UNIV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "nama_universitas","kota","provinsi","kode_pt","status_pt","akreditasi_institusi",
                "tanggal_berdiri","no_sk_pendirian","tanggal_sk_pendirian",
                "telepon_1","telepon_2","email","website","alamat_lengkap"
            ])
            w.writerow(row_univ)

        with open(OUT_PRODI, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "nama_universitas","kode_pt","status_pt_univ","akreditasi_pt_univ","tahun_pelaporan",
                "kode_prodi","nama_program_studi","status_prodi","jenjang","akreditasi_prodi",
                "jumlah_dosen_penghitung_rasio","dosen_tetap","dosen_tidak_tetap","total_dosen",
                "jumlah_mahasiswa","rasio_dosen_mahasiswa"
            ])
            w.writerows(prodi_list)

        print(f"\n✅ SELESAI!")
        print(f"   Universitas : 1 baris → {OUT_UNIV}")
        print(f"   Prodi       : {len(prodi_list)} baris → {OUT_PRODI}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
