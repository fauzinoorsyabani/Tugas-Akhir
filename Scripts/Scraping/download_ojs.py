import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls = [
    # 1. Business Intelligence Framework for Performance Measurement in Higher Education Study Programs
    ("BI_Framework_IAPS40_Untar.pdf", "https://journal.untar.ac.id/index.php/jmistki/article/view/8877"),
    ("BI_Untar_12612.pdf", "https://journal.untar.ac.id/index.php/jmistki/article/view/12612"),
    ("Roadmap_Implementing_BI_HEI_MDPI.pdf", "https://www.mdpi.com/2071-1050/13/2/747/pdf"),
    ("Pemanfaatan_BI_PT_MaChung.pdf", "https://machung.ac.id/wp-content/uploads/2021/04/Pemanfaatan-Business-Intelligence-di-Perguruan-Tinggi.pdf"),
    ("BI_Alumni_Data_Unud.pdf", "https://ojs.unud.ac.id/index.php/merpati/article/view/74889"),
    ("BI_Prediksi_Kelulusan_UMRI.pdf", "https://jurnal.umri.ac.id/index.php/generics/article/view/2836"),
    ("Penerapan_BI_UPA_TIK_Unima.pdf", "https://jti.teknikinformatika.org/index.php/jti/article/view/434"),
    ("BI_STMIK_Royal.pdf", "https://jurnal.stmikroyal.ac.id/index.php/jurteksi/article/view/2143"),
    ("BI_Roadmap_Universitas_SaintisPub.pdf", "https://saintispub.com/index.php/jits/article/view/149"),
    ("BI_IKRAITH.pdf", "https://journals.upi-yai.ac.id/index.php/ikraith-informatika/article/view/123"),
    ("BI_Bircu_Journal.pdf", "https://www.bircu-journal.com/index.php/birci/article/view/1815")
]

output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def download_file(url, out_path):
    resp = requests.get(url, headers=headers, timeout=30, verify=False, allow_redirects=True)
    if resp.status_code == 200 and b'%PDF' in resp.content[:1024]:
        with open(out_path, 'wb') as f:
            f.write(resp.content)
        return True
    return False

for name, url in urls:
    filepath = output_dir / name
    if filepath.exists():
        continue
    print(f"\nProcessing {name} from {url}")
    
    # if it's already a direct pdf
    if url.endswith('.pdf'):
        if download_file(url, filepath):
            print(" -> Direct PDF Success!")
        else:
            print(" -> Failed direct PDF download")
        continue

    # Get the HTML page
    try:
        resp = requests.get(url, headers=headers, timeout=30, verify=False)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Look for typical OJS PDF download links
            found = False
            for a in soup.find_all('a'):
                href = a.get('href', '')
                if 'article/download' in href or 'pdf' in href.lower() or 'download' in a.text.lower():
                    if 'http' not in href:
                         continue # or we could resolve it, but OJS usually has absolute URLs here
                    
                    print(f" -> Found potential PDF link: {href}")
                    if download_file(href, filepath):
                        print(" -> Success downloading OJS PDF!")
                        found = True
                        break
            if not found:
                print(" -> Could not find a working PDF link on the page.")
        else:
            print(f" -> Failed to load page. Status: {resp.status_code}")
    except Exception as e:
         print(f" -> Error: {e}")
