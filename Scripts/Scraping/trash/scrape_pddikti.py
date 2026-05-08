"""
Script untuk scraping data PDDikti menggunakan library pddiktipy
Simpan sebagai: scrape_pddikti.py
"""

from pddiktipy import api
import pandas as pd
from pprint import pprint
import json

def cari_perguruan_tinggi(nama_pt):
    """Cari data Perguruan Tinggi"""
    print(f"\n{'='*60}")
    print(f"Mencari data: {nama_pt}")
    print(f"{'='*60}\n")
    
    with api() as client:
        hasil = client.search_pt(nama_pt)
        
        if hasil:
            print(f"✓ Ditemukan {len(hasil)} hasil\n")
            
            # Tampilkan hasil
            for i, pt in enumerate(hasil, 1):
                print(f"{i}. {pt.get('nama', 'N/A')}")
                print(f"   Kode: {pt.get('kode', 'N/A')}")
                print(f"   Akreditasi: {pt.get('akreditasi', 'N/A')}")
                print()
            
            # Simpan ke Excel
            df = pd.DataFrame(hasil)
            filename = f"data_pt_{nama_pt.replace(' ', '_')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"✓ Data disimpan ke: {filename}\n")
            
            return hasil
        else:
            print("✗ Tidak ada data ditemukan\n")
            return None

def cari_mahasiswa(nama):
    """Cari data Mahasiswa"""
    print(f"\n{'='*60}")
    print(f"Mencari mahasiswa: {nama}")
    print(f"{'='*60}\n")
    
    with api() as client:
        hasil = client.search_mahasiswa(nama)
        
        if hasil:
            print(f"✓ Ditemukan {len(hasil)} mahasiswa\n")
            
            for i, mhs in enumerate(hasil, 1):
                print(f"{i}. {mhs.get('nama', 'N/A')}")
                print(f"   NIM: {mhs.get('nim', 'N/A')}")
                print(f"   PT: {mhs.get('nama_pt', 'N/A')}")
                print(f"   Prodi: {mhs.get('nama_prodi', 'N/A')}")
                print()
            
            # Simpan ke Excel
            df = pd.DataFrame(hasil)
            filename = f"data_mahasiswa_{nama.replace(' ', '_')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"✓ Data disimpan ke: {filename}\n")
            
            return hasil
        else:
            print("✗ Tidak ada data ditemukan\n")
            return None

def cari_dosen(nama):
    """Cari data Dosen"""
    print(f"\n{'='*60}")
    print(f"Mencari dosen: {nama}")
    print(f"{'='*60}\n")
    
    with api() as client:
        hasil = client.search_dosen(nama)
        
        if hasil:
            print(f"✓ Ditemukan {len(hasil)} dosen\n")
            
            for i, dsn in enumerate(hasil, 1):
                print(f"{i}. {dsn.get('nama', 'N/A')}")
                print(f"   NIDN: {dsn.get('nidn', 'N/A')}")
                print(f"   PT: {dsn.get('nama_pt', 'N/A')}")
                print()
            
            # Simpan ke Excel
            df = pd.DataFrame(hasil)
            filename = f"data_dosen_{nama.replace(' ', '_')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"✓ Data disimpan ke: {filename}\n")
            
            return hasil
        else:
            print("✗ Tidak ada data ditemukan\n")
            return None

def cari_semua(keyword):
    """Cari semua data (PT, Mahasiswa, Dosen, Prodi)"""
    print(f"\n{'='*60}")
    print(f"Mencari SEMUA data dengan keyword: {keyword}")
    print(f"{'='*60}\n")
    
    with api() as client:
        hasil = client.search_all(keyword)
        
        print("\n=== HASIL PENCARIAN ===")
        print(json.dumps(hasil, indent=2, ensure_ascii=False))
        
        # Simpan ke JSON
        filename = f"data_all_{keyword.replace(' ', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(hasil, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Data disimpan ke: {filename}\n")
        
        return hasil

# ============================================
# CONTOH PENGGUNAAN
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("SCRAPER DATA PDDIKTI KEMDIKBUD")
    print("="*60)
    
    # Pilih menu
    print("\nPilih jenis pencarian:")
    print("1. Cari Perguruan Tinggi")
    print("2. Cari Mahasiswa")
    print("3. Cari Dosen")
    print("4. Cari Semua Data")
    
    pilihan = input("\nMasukkan pilihan (1-4): ")
    
    if pilihan == "1":
        nama = input("Masukkan nama Perguruan Tinggi: ")
        cari_perguruan_tinggi(nama)
        
    elif pilihan == "2":
        nama = input("Masukkan nama Mahasiswa: ")
        cari_mahasiswa(nama)
        
    elif pilihan == "3":
        nama = input("Masukkan nama Dosen: ")
        cari_dosen(nama)
        
    elif pilihan == "4":
        keyword = input("Masukkan keyword pencarian: ")
        cari_semua(keyword)
        
    else:
        print("Pilihan tidak valid!")
    
    print("\n" + "="*60)
    print("SELESAI")
    print("="*60)