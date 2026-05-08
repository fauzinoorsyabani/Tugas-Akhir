import pandas as pd
import os

def generate_master_table():
    print("Memulai penggabungan data untuk Google Looker Studio...")
    
    # Path ke file Star Schema
    base_path = 'd:/Code/Tugas Akhir/Data/Star_Schema'
    
    # Load Data
    fact = pd.read_csv(os.path.join(base_path, 'Fact_Kapasitas_Pendidikan.csv'))
    dim_prodi = pd.read_csv(os.path.join(base_path, 'Dim_Prodi.csv'))
    dim_waktu = pd.read_csv(os.path.join(base_path, 'Dim_Waktu.csv'))
    dim_univ = pd.read_csv(os.path.join(base_path, 'Dim_Universitas.csv'))
    
    # Join Fact with Dimensions
    # 1. Join with Prodi
    master = fact.merge(dim_prodi, on='id_prodi', how='left')
    
    # 2. Join with Waktu
    master = master.merge(dim_waktu, on='id_waktu', how='left')
    
    # 3. Join with Universitas
    master = master.merge(dim_univ, on='id_universitas', how='left')
    
    # Re-order and select columns for Dashboard
    # We want a clean set of columns
    final_cols = [
        'tahun_pelaporan', 'semester', 'tahun',
        'nama_program_studi', 'jenjang', 'status_prodi', 'akreditasi_prodi',
        'nama_universitas', 'kota', 'provinsi',
        'jumlah_mahasiswa', 'jumlah_dosen_penghitung_rasio', 'total_dosen',
        'rasio_dosen_mahasiswa', 'nilai_rasio'
    ]
    
    # Ensure all columns exist (some might have slightly different names)
    master_final = master[[c for c in final_cols if c in master.columns]]
    
    # Sort by Time and Prodi
    # Map semester to numerical for sorting
    semester_map = {'Ganjil': 1, 'Genap': 2}
    master_final['sem_num'] = master_final['semester'].map(semester_map)
    master_final = master_final.sort_values(by=['tahun', 'sem_num', 'nama_program_studi'])
    master_final = master_final.drop(columns=['sem_num'])
    
    # Save to Processed folder
    output_dir = 'd:/Code/Tugas Akhir/Data/Processed'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'master_looker_unsil.csv')
    master_final.to_csv(output_path, index=False)
    
    print(f"DONE: Berhasil membuat Master Table: {output_path}")
    print(f"Total Baris: {len(master_final)}")
    
if __name__ == "__main__":
    generate_master_table()
