import sys
sys.path.append(r"d:\Code\Tugas Akhir\Scraping_Scripts")
import scrape_pddikti

import pandas as pd
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def fix_unsil():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)
    uni_name = "Universitas Siliwangi"
    
    try:
        driver.get("https://pddikti.kemdiktisaintek.go.id/perguruan-tinggi")
        inp = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Cari Perguruan Tinggi']")))
        inp.clear()
        inp.send_keys(uni_name)
        time.sleep(1)
        inp.send_keys(Keys.ENTER)
        
        print(f"Mencari {uni_name}...")
        time.sleep(5)
        
        found = False
        btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Lihat Detail')]")
        
        # Try to find the card with "Aktif"
        cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'bg-white') and .//button[contains(text(), 'Lihat Detail')]]")
        target_btn = None
        for card in cards:
            if "Aktif" in card.text:
                target_btn = card.find_element(By.XPATH, ".//button[contains(text(), 'Lihat Detail')]")
                print("Menemukan card dengan badge Aktif!")
                break
                
        if not target_btn and len(btns) > 1:
            target_btn = btns[1]
            print("Fallback ke tombol Lihat Detail kedua")
        elif not target_btn and len(btns) > 0:
            target_btn = btns[0]
            
        if target_btn:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_btn)
            time.sleep(1)
            target_btn.click()
            found = True
            
        if not found:
            print("Gagal menemukan tombol detail.")
            return

        wait.until(EC.url_contains("detail-pt"))
        print("Masuk halaman detail.")
        time.sleep(3)
        
        row_univ, kode_pt, status_pt, akreditasi_pt = scrape_pddikti.scrape_university_metadata(driver, uni_name)
        print("Metadata Berhasil:", kode_pt, status_pt, akreditasi_pt)
        
        prodi_list = scrape_pddikti.scrape_prodi_data(driver, uni_name, kode_pt, status_pt, akreditasi_pt)
        print(f"Berhasil scrape {len(prodi_list)} baris data prodi untuk semua periode yang dipilih!")
        
        # Simpan ke CSV sementara
        with open(r"d:\Code\Tugas Akhir\unsil_univ_new.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row_univ)
            
        with open(r"d:\Code\Tugas Akhir\unsil_prodi_new.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(prodi_list)
            
        print("SELESAI. File tersimpan: unsil_univ_new.csv dan unsil_prodi_new.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    fix_unsil()
