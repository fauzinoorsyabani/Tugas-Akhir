import pandas as pd
df = pd.read_csv('prodi_raw.csv')
print(df[['tahun_pelaporan', 'rasio_dosen_mahasiswa', 'jumlah_mahasiswa', 'total_dosen']].head(5))
print("\n-----\n")
print(df.dtypes)
