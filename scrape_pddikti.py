import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# --- KONFIGURASI ZONA ---

# Zona I (14 Univ) - Belum discrape
ZONA_1 = [
    "Institut Seni Indonesia Surakarta",
    "Politeknik Negeri Lampung",
    "Politeknik Negeri Pontianak",
    "Politeknik Negeri Sriwijaya",
    "Universitas Bengkulu",
    "Universitas Halu Oleo",
    "Universitas Jambi",
    "Universitas Lampung",
    "Universitas Mataram",
    "Universitas Negeri Gorontalo",
    "Universitas Nusa Cendana",
    "Universitas Tadulako",
    "Universitas Tanjungpura",
    "Universitas Tidar"
]

# Zona II (28 Univ) - SUDAH SELESAI (Load dari file)
# Tidak dimasukkan ke antrian scrape

# Zona III (11 Univ) - Belum discrape
ZONA_3 = [
    "Politeknik Manufaktur Bandung",
    "Politeknik Negeri Bali",
    "Politeknik Negeri Bandung",
    "Politeknik Negeri Batam",
    "Politeknik Negeri Jakarta",
    "Universitas Mulawarman",
    "Universitas Negeri Manado",
    "Universitas Pembangunan Nasional Veteran Jakarta",
    "Universitas Pembangunan Nasional Veteran Yogyakarta",
    "Universitas Sam Ratulangi",
    "Universitas Udayana"
]

# Gabungan Target Scrape Baru
TARGET_UNIVERSITIES = ZONA_1 + ZONA_3

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_university(driver, uni_name):
    print(f"\n--- Memproses: {uni_name} ---")
    wait = WebDriverWait(driver, 25)
    
    # 1. Buka Halaman Pencarian
    for retry in range(3):
        try:
            driver.get("https://pddikti.kemdiktisaintek.go.id/perguruan-tinggi")
            
            # Cari Input
            search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Cari Perguruan Tinggi']")))
            search_box.clear()
            search_box.send_keys(uni_name)
            time.sleep(1)
            search_box.send_keys(Keys.ENTER)
            
            print(f"   Sedang mencari {uni_name}...")
            time.sleep(4)
            
            # Klik Detail
            detail_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Lihat Detail')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", detail_btn)
            time.sleep(1)
            detail_btn.click()
            
            wait.until(EC.url_contains("detail-pt"))
            break 
        except Exception as e:
            print(f"   ⚠️ Percobaan search ke-{retry+1} gagal: {str(e)[:100]}")
            time.sleep(2)
            if retry == 2:
                print(f"   ❌ Gagal masuk ke halaman detail {uni_name}")
                return []

    # 4. Scrape Data Program Studi
    all_rows = []
    page = 1
    
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(3) 
    
    while True:
        rows_collected = 0
        current_page_data = []
        
        for _ in range(5):
            try:
                rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                current_page_data = []
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 5: 
                        row_txt = [c.text.strip() for c in cols]
                        if row_txt[0] or row_txt[1]: 
                            final_row = [uni_name] + row_txt
                            current_page_data.append(final_row)
            
                if len(current_page_data) > 0:
                    break 
                else:
                    time.sleep(2) 
            except StaleElementReferenceException:
                time.sleep(1)
                
        all_rows.extend(current_page_data)
        rows_collected = len(current_page_data)
        print(f"   > Halaman {page}: {rows_collected} data.")

        has_next = False
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            valid_next_btn = None
            svg_buttons = [b for b in buttons if b.find_elements(By.TAG_NAME, "svg")]
            
            if svg_buttons:
                last_btn = svg_buttons[-1]
                if last_btn.is_enabled() and "disabled" not in last_btn.get_attribute("class"):
                    valid_next_btn = last_btn

            if valid_next_btn:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", valid_next_btn)
                time.sleep(1)
                valid_next_btn.click()
                page += 1
                has_next = True
                print("     Klik Next...")
                time.sleep(5) 
            else:
                pass
                
        except Exception as e:
            pass
        
        if not has_next:
            break
            
    print(f"   ✅ Selesai {uni_name}: Total {len(all_rows)} baris.")
    return all_rows

def main():
    driver = setup_driver()
    new_data = []
    
    print(f"\n=== MULAI SCRAPING ZONA I & III ({len(TARGET_UNIVERSITIES)} Universitas) ===")
    print("Zona II akan dilewati dan diload dari file yang sudah ada.")
    
    try:
        for i, uni in enumerate(TARGET_UNIVERSITIES, 1):
            print(f"\n[{i}/{len(TARGET_UNIVERSITIES)}] Processing...")
            uni_data = scrape_university(driver, uni)
            new_data.extend(uni_data)
            
            if len(new_data) > 0:
                try:
                     df_temp = pd.DataFrame(new_data)
                     df_temp.to_excel("checkpoint_zona_1_3.xlsx", index=False)
                except:
                     pass
            
    finally:
        driver.quit()
    
    # --- PROSES PENGGABUNGAN DATA ---
    print("\n--- MENGGABUNGKAN DATA SEMUA ZONA ---")
    
    columns = [
        "Nama Universitas", "Kode", "Program Studi", "Status", "Jenjang", "Akreditasi",
        "Dosen Penghitung Rasio", "Dosen Tetap", "Dosen Tidak Tetap", "Total Dosen", 
        "Jumlah Mahasiswa", "Rasio Dosen/Mhs"
    ]
    
    # 1. Olah Data Baru (Zona 1 & 3)
    final_new_data = []
    if new_data:
        for row in new_data:
            cleaned = row[:12]
            while len(cleaned) < 12:
                cleaned.append("")
            final_new_data.append(cleaned)
        df_new = pd.DataFrame(final_new_data, columns=columns)
        print(f"✅ Data Baru (Zona I & III): {len(df_new)} baris.")
    else:
        df_new = pd.DataFrame(columns=columns)
        print("⚠️ Tidak ada data baru yang berhasil discrape.")

    # 2. Load Data Lama (Zona 2)
    old_file = "Data_PTN_BLU_Zona_II_Final.xlsx"
    if os.path.exists(old_file):
        try:
            df_old = pd.read_excel(old_file)
            # Pastikan kolom sesuai
            df_old.columns = columns[:len(df_old.columns)] 
            print(f"✅ Data Lama (Zona II) diload: {len(df_old)} baris.")
        except Exception as e:
            print(f"❌ Gagal load file lama: {e}")
            df_old = pd.DataFrame(columns=columns)
    else:
        print(f"⚠️ File {old_file} tidak ditemukan. Hasil hanya akan berisi data baru.")
        df_old = pd.DataFrame(columns=columns)

    # 3. Gabung
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    
    output_file = "Data_PTN_BLU_Gabungan_Final.xlsx"
    try:
        df_combined.to_excel(output_file, index=False)
        print(f"\n🎉 SUKSES TOTAL! Data Lengkap (Zona I, II, III) tersimpan di:\n{output_file}")
        print(f"Total Baris Gabungan: {len(df_combined)}")
    except PermissionError:
        output_file_backup = "Data_PTN_BLU_Gabungan_Final_BACKUP.xlsx"
        df_combined.to_excel(output_file_backup, index=False)
        print(f"\n❌ File utama terkunci. Data disimpan ke {output_file_backup}")

if __name__ == "__main__":
    main()
