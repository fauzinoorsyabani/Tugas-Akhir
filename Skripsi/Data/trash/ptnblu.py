from pddiktipy import api
from pprint import pprint

# Cari data perguruan tinggi
with api() as client:
    # Cari PT
    hasil = client.search_pt('Unika Soegijapranata')
    pprint(hasil)
    
    # Cari mahasiswa
    mahasiswa = client.search_mahasiswa('nama mahasiswa')
    pprint(mahasiswa)
    
    # Cari dosen
    dosen = client.search_dosen('nama dosen')
    pprint(dosen)