import requests
import time
from pathlib import Path
import os
import urllib.parse

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
    'business intelligence higher education roadmap',
    '"business intelligence roadmap" university',
    'business intelligence implementation higher education',
    'business intelligence dashboard university',
    'Data warehouse business intelligence roadmap education'
]

downloaded = 0
found_links = set()

for query in queries:
    if downloaded >= needed:
        break
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&fields=title,openAccessPdf&limit=100"
    print(f"Searching: {query}")
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get('data', [])
            for item in data:
                if downloaded >= needed:
                    break
                
                pdf_info = item.get('openAccessPdf')
                if pdf_info and pdf_info.get('url'):
                    pdf_url = pdf_info['url']
                    if pdf_url in found_links:
                        continue
                    found_links.add(pdf_url)
                    
                    if not pdf_url.lower().endswith('.pdf'):
                        continue
                    
                    print(f"Trying: {pdf_url}")
                    try:
                        pdf_resp = requests.get(pdf_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                        if pdf_resp.status_code == 200 and b'%PDF' in pdf_resp.content[:10]:
                            title = item.get('title', 'Document')
                            safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                            name = f"{safe_title[:60]}.pdf"
                            path = output_dir / name
                            if not path.exists():
                                with open(path, 'wb') as f:
                                    f.write(pdf_resp.content)
                                print(f"  -> SUCCESS: {name}")
                                downloaded += 1
                        else:
                            print(f"  -> Failed: Status {pdf_resp.status_code} or not PDF")
                    except Exception as e:
                        print(f"  -> Error: {e}")
                    time.sleep(1)
            time.sleep(1)
    except Exception as e:
        print(f"Search API Error: {e}")

print(f"Finished. Downloaded {downloaded} new files.")
