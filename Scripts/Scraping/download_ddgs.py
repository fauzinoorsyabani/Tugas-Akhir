from duckduckgo_search import DDGS
import requests
import time
from pathlib import Path
import os

output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)
existing_count = len(list(output_dir.glob("*.pdf")))
target_count = 10
needed = target_count - existing_count

if needed <= 0:
    print("Already have enough PDFs")
    exit(0)

print(f"Need {needed} more PDFs")
queries = [
    '"Business Intelligence Roadmap" Moss Atre pdf',
    '"Business Intelligence Roadmap" pendidikan pdf',
    '"Business Intelligence Roadmap" perguruan tinggi jurnal pdf'
]

downloaded = 0
found_links = set()

def test_and_download(url, pdf_idx):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200 and b'%PDF' in resp.content[:10]:
            name = url.split('/')[-1]
            if not name.endswith('.pdf'):
                name = f"document_{pdf_idx}.pdf"
            
            # keep it valid windows string
            name = "".join([c for c in name if c.isalnum() or c in ' ._-'])
            
            path = output_dir / name
            with open(path, 'wb') as f:
                f.write(resp.content)
            print(f"  -> SUCCESS: {name}")
            return True
        else:
            print(f"  -> Failed: Status {resp.status_code} or not PDF")
    except Exception as e:
        print(f"  -> Error: {e}")
    return False

with DDGS() as ddgs:
    for q in queries:
        if downloaded >= needed:
            break
        print(f"Searching: {q}")
        results = ddgs.text(q, max_results=30)
         
        for r in results:
            if downloaded >= needed:
                break
            url = r.get('href')
            if '.pdf' in url.lower() or 'download' in url.lower():
                if url in found_links:
                    continue
                found_links.add(url)
                print(f"Trying: {url}")
                if test_and_download(url, downloaded + existing_count + 1):
                    downloaded += 1
                time.sleep(1)

print(f"Finished. Downloaded {downloaded} new files.")
