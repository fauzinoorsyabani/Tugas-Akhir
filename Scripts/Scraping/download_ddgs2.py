import requests
import time
from pathlib import Path
from duckduckgo_search import DDGS
import os

output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)
existing = len(list(output_dir.glob("*.pdf")))
needed = 10 - existing

if needed <= 0:
    print("Already have enough PDFs")
    exit(0)

print(f"Need {needed} more PDFs")

queries = [
    '"Business Intelligence Roadmap" filetype:pdf site:ac.id',
    '"Business Intelligence Roadmap" jurnal Moss Atre filetype:pdf site:ac.id',
    '"Business Intelligence" roadmap tableau perguruan tinggi filetype:pdf',
    '"roadmap business intelligence" "pendidikan" filetype:pdf',
    '"roadmap business intelligence" "universitas" filetype:pdf site:ac.id',
    'metode "Business Intelligence Roadmap" ext:pdf',
    '"business intelligence roadmap" "dashboard" ext:pdf site:ac.id'
]

downloaded = 0
found_links = set()

def try_download(url, fallback_name):
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if resp.status_code == 200 and b'%PDF' in resp.content[:10]:
            name = url.split('/')[-1]
            if not name.endswith('.pdf'):
                name = fallback_name
            name = "".join([c for c in name if c.isalnum() or c in ' ._-'])
            if len(name) > 60:
                name = name[-60:]
            path = output_dir / name
            if not path.exists():
                with open(path, 'wb') as f:
                    f.write(resp.content)
                print(f"  -> SUCCESS: {name}")
                return True
            else:
                print(f"  -> ALREADY EXISTS: {name}")
                return False
        else:
            print(f"  -> FAILED: Status {resp.status_code} or not PDF")
    except Exception as e:
        print(f"  -> ERROR: {e}")
    return False

with DDGS() as ddgs:
    for q in queries:
        if downloaded >= needed:
            break
        print(f"\nSearching: {q}")
        try:
            results = ddgs.text(q, max_results=30)
            for r in results:
                if downloaded >= needed:
                    break
                url = r.get('href')
                if url in found_links:
                    continue
                found_links.add(url)
                
                print(f"Trying: {url}")
                if try_download(url, f"Jurnal_BI_Pendidikan_{downloaded+existing+1}.pdf"):
                    downloaded += 1
                time.sleep(1)
        except Exception as e:
            print(f"Search API Error: {e}")

print(f"Finished. Downloaded {downloaded} new files.")
