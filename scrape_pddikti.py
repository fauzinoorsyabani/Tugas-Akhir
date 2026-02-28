import pandas as pd
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# --- KONFIGURASI ZONA ---
ZONA_1 = [
    "Institut Seni Indonesia Surakarta", "Politeknik Negeri Lampung", "Politeknik Negeri Pontianak",
    "Politeknik Negeri Sriwijaya", "Universitas Bengkulu", "Universitas Halu Oleo", "Universitas Jambi",
    "Universitas Lampung", "Universitas Mataram", "Universitas Negeri Gorontalo", "Universitas Nusa Cendana",
    "Universitas Tadulako", "Universitas Tanjungpura", "Universitas Tidar"
]

ZONA_2 = [
    "Institut Seni Indonesia Padang Panjang", "Politeknik Elektronika Negeri Surabaya", "Politeknik Negeri Jember",
    "Politeknik Negeri Malang", "Politeknik Negeri Medan", "Politeknik Negeri Padang", "Politeknik Negeri Semarang",
    "Politeknik Negeri Ujung Pandang", "Politeknik Perkapalan Negeri Surabaya", "Universitas Bangka Belitung",
    "Universitas Cenderawasih", "Universitas Jember", "Universitas Jenderal Soedirman", "Universitas Khairun",
    "Universitas Lambung Mangkurat", "Universitas Malikussaleh", "Universitas Musamus", "Universitas Negeri Makassar",
    "Universitas Negeri Medan", "Universitas Palangka Raya", "Universitas Pattimura",
    "Universitas Pembangunan Nasional Veteran Jawa Timur", "Universitas Pendidikan Ganesha", "Universitas Riau",
    "Universitas Siliwangi", "Universitas Singaperbangsa Karawang", "Universitas Sultan Ageng Tirtayasa",
    "Universitas Trunojoyo Madura"
]

ZONA_3 = [
    "Politeknik Manufaktur Bandung", "Politeknik Negeri Bali", "Politeknik Negeri Bandung", "Politeknik Negeri Batam",
    "Politeknik Negeri Jakarta", "Universitas Mulawarman", "Universitas Negeri Manado",
    "Universitas Pembangunan Nasional Veteran Jakarta", "Universitas Pembangunan Nasional Veteran Yogyakarta",
    "Universitas Sam Ratulangi", "Universitas Udayana"
]

TARGET_UNIVERSITIES = sorted(ZONA_1 + ZONA_2 + ZONA_3)

# --- FILE OUTPUT ---
FILE_UNIV = "universitas_raw.csv"
FILE_PRODI = "prodi_raw.csv"

def setup_files():
    # Setup CSV Universitas
    if not os.path.exists(FILE_UNIV):
        with open(FILE_UNIV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "nama_universitas", "kota", "provinsi",
                "kode_pt", "status_pt", "akreditasi_institusi",
                "tanggal_berdiri", "no_sk_pendirian", "tanggal_sk_pendirian",
                "telepon_1", "telepon_2", "email", "website",
                "alamat_lengkap"
            ])
            
    # Setup CSV Prodi WITH NEW COLUMNS
    if not os.path.exists(FILE_PRODI):
        with open(FILE_PRODI, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "nama_universitas", "kode_pt", "status_pt_univ", "akreditasi_pt_univ", "tahun_pelaporan",
                "kode_prodi", "nama_program_studi", "status_prodi", "jenjang", "akreditasi_prodi",
                "jumlah_dosen_penghitung_rasio", "dosen_tetap", "dosen_tidak_tetap", "total_dosen",
                "jumlah_mahasiswa", "rasio_dosen_mahasiswa"
            ])

def save_univ_data(data):
    with open(FILE_UNIV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def save_prodi_data(data_list):
    with open(FILE_PRODI, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data_list)

def get_text_safe(driver, xpath):
    try:
        elm = driver.find_element(By.XPATH, xpath)
        return elm.text.strip()
    except:
        return "-"

def get_metadata_robust(driver, label_keyword):
    """
    Mencari nilai metadata dengan berbagai strategi karena struktur DOM sering berubah.
    """
    wait = WebDriverWait(driver, 1)
    value = "-"
    
    # Strategy 1: Find element with exact text 'Label' and get next sibling div
    # <div class="text-sm">Label</div> <div class="font-bold">Value</div>
    try:
        # Cari semua elemen yg contain text Label
        # Filter yang text-nya pendek (kurang dari 20 chars) untuk menghindari match paragraf
        candidates = driver.find_elements(By.XPATH, f"//*[contains(text(), '{label_keyword}')]")
        
        for cand in candidates:
            if len(cand.text) < 30 and label_keyword.lower() in cand.text.lower():
                # Coba ambil sibling
                try:
                    sib = cand.find_element(By.XPATH, "following-sibling::div")
                    if sib.text.strip():
                        return sib.text.strip()
                except: pass
                
                # Coba ambil parent -> following sibling (Grid Layout)
                try:
                    parent_sib = cand.find_element(By.XPATH, "./../following-sibling::div")
                    if parent_sib.text.strip():
                        return parent_sib.text.strip()
                except: pass
    except:
        pass
        
    return value

def scrape_university_metadata(driver, uni_name):
    print(f"   [Metadata] Scrape...")
    
    # --- Identitas ---
    kota = "-"
    provinsi = "-"
    try:
        prov_elm = driver.find_element(By.XPATH, "//*[contains(text(), 'Prov.')]")
        raw_loc = prov_elm.text.strip()
        parts = raw_loc.split(',')
        if len(parts) >= 1: kota = parts[0].strip()
        if len(parts) >= 2: provinsi = parts[1].strip()
    except:
        pass

    # --- Header Information (SPECIFIC XPATH) ---
    # Based on screenshot: Kode, Status, Akreditasi are in left column
    # Structure: <div class="text-sm text-gray-500">Kode</div> followed by <div class="font-semibold">002008</div>
    
    kode_pt = "-"
    status_pt = "-"
    akreditasi = "-"
    
    # Strategy: Find exact text match for label, then get next element
    try:
        # Find all divs, look for exact "Kode" text
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        for i, div in enumerate(all_divs):
            text = div.text.strip()
            
            # Check for Kode
            if text == "Kode" and kode_pt == "-":
                try:
                    # Next div should be the value
                    if i + 1 < len(all_divs):
                        kode_pt = all_divs[i + 1].text.strip()
                        if len(kode_pt) > 10:  # Too long, not a code
                            kode_pt = "-"
                except:
                    pass
            
            # Check for Status
            elif text == "Status" and status_pt == "-":
                try:
                    if i + 1 < len(all_divs):
                        status_pt = all_divs[i + 1].text.strip()
                        if len(status_pt) > 20:  # Too long
                            status_pt = "-"
                except:
                    pass
            
            # Check for Akreditasi
            elif text == "Akreditasi" and akreditasi == "-":
                try:
                    if i + 1 < len(all_divs):
                        akreditasi = all_divs[i + 1].text.strip()
                        if len(akreditasi) > 30:  # Too long
                            akreditasi = "-"
                except:
                    pass
        
        print(f"   📌 Metadata: Kode={kode_pt}, Status={status_pt}, Akreditasi={akreditasi}")
        
    except Exception as e:
        print(f"   ⚠️ Error extracting metadata: {e}")

    
    # --- Legalitas ---
    tgl_berdiri = get_metadata_robust(driver, "Tanggal Berdiri")
    no_sk = get_metadata_robust(driver, "No SK Pendirian") # Might need fuzzy match
    tgl_sk = get_metadata_robust(driver, "Tanggal SK Pendirian")
    
    # --- Kontak ---
    telp_1 = "-"
    telp_2 = "-"
    email = "-"
    website = "-"
    
    try:
        try:
             email = driver.find_element(By.XPATH, "//a[contains(@href,'mailto:')]").text.strip()
        except: pass
        
        try:
             website = driver.find_element(By.XPATH, "//a[contains(@href,'http') and not(contains(@href, 'google'))]").text.strip()
        except: pass
    except: pass

    # --- Alamat ---
    alamat = "-"
    try:
        alamat = driver.find_element(By.XPATH, "//*[contains(text(), 'Alamat')]/following-sibling::div").text.strip()
    except:
        pass

    row = [
        uni_name, kota, provinsi,
        kode_pt, status_pt, akreditasi,
        tgl_berdiri, no_sk, tgl_sk,
        telp_1, telp_2, email, website,
        alamat
    ]
    return row, kode_pt, status_pt, akreditasi

def _get_fresh_selects(driver, wait, timeout=10):
    """Ambil ulang selects untuk menghindari stale element."""
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
        time.sleep(0.5)
        return driver.find_elements(By.TAG_NAME, "select")
    except:
        return []


def select_option_with_retry(driver, wait, select_index, identifier, by_value=False, retries=3):
    """Pilih opsi select dengan retry untuk menghindari stale element."""
    for attempt in range(retries):
        try:
            selects = _get_fresh_selects(driver, wait)
            if len(selects) > select_index:
                sel = Select(selects[select_index])
                if by_value:
                    sel.select_by_value(identifier)
                else:
                    sel.select_by_visible_text(identifier)
                return True
        except StaleElementReferenceException:
            print(f"       ⚠️ Stale element pada select, retry {attempt+1}/{retries}...")
            time.sleep(1)
        except Exception as e:
            print(f"       ⚠️ Gagal pilih opsi '{identifier}' (attempt {attempt+1}): {e}")
            time.sleep(1)
    return False


def scrape_prodi_data(driver, uni_name, kode_pt, status_pt, akreditasi_pt):
    print(f"   [Prodi] Scrape dengan Periode & Tampilkan Semua...")
    wait = WebDriverWait(driver, 15)

    # 1. Scroll to Program Studi section
    try:
        # Wait for table to appear first
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
        header = driver.find_element(By.XPATH, "//*[contains(text(), 'Program Studi')]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
        time.sleep(2)
    except:
        print("     ⚠️ Tidak menemukan section Program Studi / tabel belum muncul")
        return []

    # SET TAMPILKAN TO "semua" (select index 0)
    ok = select_option_with_retry(driver, wait, 0, "semua", by_value=True)
    if ok:
        time.sleep(3)  # tunggu tabel di-reload
    else:
        print("     ⚠️ Gagal memilih 'semua', lanjut dengan default.")

    TARGET_PERIODS = ["Ganjil 2025", "Genap 2024", "Ganjil 2024", "Genap 2023", "Ganjil 2023"]
    all_rows_data = []

    for period in TARGET_PERIODS:
        print(f"     >> Scraping Periode: {period}")

        # Pilih periode (select index 1)
        ok = select_option_with_retry(driver, wait, 1, period, by_value=False)
        if not ok:
            print(f"     ⚠️ Skip periode {period} (tidak tersedia / gagal dipilih).")
            continue
        time.sleep(4)  # tunggu tabel di-reload setelah ganti periode

        page_num = 1
        period_count = 0

        while True:
            # Scrape current page rows
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
                rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

                # Cek jika tidak ada data
                if len(rows) <= 1:
                    first_cols = rows[0].find_elements(By.TAG_NAME, "td") if rows else []
                    if len(first_cols) < 5:
                        print(f"       -> Tidak ada data untuk {period}.")
                        break

                page_count = 0
                for r in rows:
                    try:
                        cols = r.find_elements(By.TAG_NAME, "td")
                        if len(cols) < 5:
                            continue
                        txts = [c.text.strip() for c in cols]

                        # Handling "No" column
                        offset = 1 if (len(txts[0]) <= 3 and txts[0].isdigit()) else 0

                        k_prodi  = txts[0 + offset]
                        n_prodi  = txts[1 + offset]
                        s_prodi  = txts[2 + offset]
                        jenjang  = txts[3 + offset]
                        akr_prodi= txts[4 + offset]
                        d_r      = txts[5 + offset]
                        d_t      = txts[6 + offset]
                        d_tt     = txts[7 + offset]
                        d_tot    = txts[8 + offset]
                        mhs      = txts[9 + offset]
                        rasio    = txts[10 + offset]

                        row_data = [
                            uni_name, kode_pt, status_pt, akreditasi_pt, period,
                            k_prodi, n_prodi, s_prodi, jenjang, akr_prodi,
                            d_r, d_t, d_tt, d_tot, mhs, rasio
                        ]
                        all_rows_data.append(row_data)
                        page_count += 1
                    except (IndexError, StaleElementReferenceException):
                        pass

                period_count += page_count
                print(f"       -> Halaman {page_num}: {page_count} prodi.")

            except Exception as e:
                print(f"       ⚠️ Eror scrape halaman {page_num}: {e}")

            # CHECK NEXT BUTTON
            has_next = False
            try:
                next_btn = driver.find_element(By.XPATH, "//button[./*[name()='svg']][last()]")
                is_disabled = ("disabled" in (next_btn.get_attribute("class") or ""))
                if next_btn.is_enabled() and not is_disabled:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                    time.sleep(0.5)
                    next_btn.click()
                    time.sleep(2)
                    page_num += 1
                    has_next = True
            except NoSuchElementException:
                pass
            except Exception as e:
                print(f"       ⚠️ Eror klik Next: {e}")

            if not has_next:
                break

        print(f"     ✅ Total {period_count} prodi untuk {period}.")

    return all_rows_data

def process_uni(driver, uni_name):
    wait = WebDriverWait(driver, 20)
    driver.get("https://pddikti.kemdiktisaintek.go.id/perguruan-tinggi")
    
    try:
        inp = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Cari Perguruan Tinggi']")))
        inp.clear()
        inp.send_keys(uni_name)
        time.sleep(1)
        inp.send_keys(Keys.ENTER)
        
        print(f"   Mencari {uni_name}...")
        time.sleep(5)  # Wait for search results
        
        # SIMPLIFIED: Just click first "Lihat Detail" button
        found = False
        try:
            # Wait for buttons to appear
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Lihat Detail')]")))
            
            # Get all detail buttons
            btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Lihat Detail')]")
            
            if len(btns) > 0:
                print(f"   Menemukan {len(btns)} tombol 'Lihat Detail'")
                
                # Click the first one (usually the most relevant)
                target_btn = btns[0]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_btn)
                time.sleep(1)
                
                print("   Mengklik tombol 'Lihat Detail'...")
                target_btn.click()
                found = True
            else:
                print("   ⚠️ Tidak menemukan tombol 'Lihat Detail'")
                
        except Exception as e:
            print(f"   ⚠️ Error saat mencari/klik tombol: {e}")
        
        if not found:
            print(f"❌ Gagal menemukan tombol detail untuk {uni_name}")
            return

        wait.until(EC.url_contains("detail-pt"))
        time.sleep(3)
        
        # Scrape Metadata (Returns 3 extra fields)
        row_univ, kode_pt, status_pt, akreditasi_pt = scrape_university_metadata(driver, uni_name)
        save_univ_data(row_univ)
        
        # Scrape Prodi (Pass new metadata)
        prodi_list = scrape_prodi_data(driver, uni_name, kode_pt, status_pt, akreditasi_pt)
        save_prodi_data(prodi_list)
        
        print(f"✅ OK: {uni_name} - {len(prodi_list)} Prodi.")
        
    except Exception as e:
        print(f"❌ ERROR {uni_name}: {e}")
        # Lanjut ke universitas berikutnya, jangan crash total
        try:
            driver.get("about:blank")
            time.sleep(1)
        except:
            pass

def get_scraped_universities():
    """Ambil daftar universitas yang sudah ada di file CSV (untuk resume)."""
    if not os.path.exists(FILE_PRODI):
        return set()
    try:
        scraped = set()
        with open(FILE_PRODI, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    scraped.add(row[0])  # nama_universitas di kolom pertama
        return scraped
    except:
        return set()


def main():
    setup_files()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Cek universitas yang sudah di-scrape (fitur RESUME)
    already_scraped = get_scraped_universities()
    if already_scraped:
        print(f"=== RESUME MODE: {len(already_scraped)} universitas sudah di-scrape, akan dilanjutkan ===")
    
    print("=== START SCRAPE (MULTI-PERIODE + RESUME) ===")
    try:
        for i, uni in enumerate(TARGET_UNIVERSITIES, 1):
            if uni in already_scraped:
                print(f"\n[{i}/{len(TARGET_UNIVERSITIES)}] SKIP (sudah ada): {uni}")
                continue
            print(f"\n[{i}/{len(TARGET_UNIVERSITIES)}] {uni}")
            process_uni(driver, uni)
    finally:
        driver.quit()
        print("\n=== FINISHED ===")

if __name__ == "__main__":
    main()
