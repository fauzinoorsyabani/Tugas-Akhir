import requests
from pathlib import Path

urls = [
    # 1. Business Intelligence Framework for Performance Measurement in Higher Education Study Programs
    ("BI_Framework_IAPS40_Untar.pdf", "https://journal.untar.ac.id/index.php/jmistki/article/download/8877/6090"),
    # 2. Another from Untar
    ("BI_Untar_12612.pdf", "https://journal.untar.ac.id/index.php/jmistki/article/download/12612/13146"),
    # 3. Roadmap for Implementing BI Systems in HEI (MDPI)
    ("Roadmap_Implementing_BI_HEI_MDPI.pdf", "https://www.mdpi.com/2071-1050/13/2/747/pdf"),
    # 4. Pemanfaatan BI di PT (Ma Chung)
    ("Pemanfaatan_BI_PT_MaChung.pdf", "https://machung.ac.id/wp-content/uploads/2021/04/Pemanfaatan-Business-Intelligence-di-Perguruan-Tinggi.pdf"),
    # 5. Application of BI in Alumni Data (Unud)
    ("BI_Alumni_Data_Unud.pdf", "https://ojs.unud.ac.id/index.php/merpati/article/download/74889/41066/"),
    # 6. Implementasi BI Prediksi Kelulusan (UMRI)
    ("BI_Prediksi_Kelulusan_UMRI.pdf", "https://jurnal.umri.ac.id/index.php/generics/article/download/2836/2189/"),
    # 7. Penerapan BI UPA TIK (Unima)
    ("Penerapan_BI_UPA_TIK_Unima.pdf", "https://jti.teknikinformatika.org/index.php/jti/article/download/434/96/"),
    # 8. Jurnal dari STMIK Royal
    ("BI_STMIK_Royal.pdf", "https://jurnal.stmikroyal.ac.id/index.php/jurteksi/article/download/2143/1151"),
    # 9. SaintisPub
    ("BI_Roadmap_Universitas.pdf", "https://saintispub.com/index.php/jits/article/download/149/134/"),
    # 10. Jurnal IKRA-ITH Informatika
    ("BI_IKRAITH.pdf", "https://journals.upi-yai.ac.id/index.php/ikraith-informatika/article/download/123/94/"),
    # 11. Bircu Journal
    ("BI_Bircu_Journal.pdf", "https://www.bircu-journal.com/index.php/birci/article/download/1815/1574")
]

output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

for name, url in urls:
    filepath = output_dir / name
    if filepath.exists():
        print(f"Already downloaded: {name}")
        continue
        
    print(f"Downloading {name} from {url}")
    try:
        # Use verify=False to bypass SSL errors (like expired certs common in local journals)
        resp = requests.get(url, headers=headers, timeout=30, verify=False, allow_redirects=True)
        if resp.status_code == 200:
            if b'%PDF' in resp.content[:10]:
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                print(f" -> Success!")
            else:
                # Often it's an OJS landing page, we might need to parse it
                # But let's just save if it claims to be a PDF. Sometimes %PDF is not at the very first byte
                if b'%PDF' in resp.content[:1024]:
                   with open(filepath, 'wb') as f:
                        f.write(resp.content)
                   print(f" -> Success! (PDF header found deeper)") 
                else:
                   print(f" -> Failed! Not a PDF document (Content-Type: {resp.headers.get('Content-Type')})")
        else:
            print(f" -> Failed! Status code: {resp.status_code}")
    except Exception as e:
        print(f" -> Error! {e}")
