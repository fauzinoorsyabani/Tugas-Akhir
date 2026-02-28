import requests
import json
import urllib.parse
from pathlib import Path
import os
import time

# Create output dir
output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)

# Count existing PDFs
existing_count = len(list(output_dir.glob("*.pdf")))
target_count = 10
to_download = target_count - existing_count
print(f"Already have {existing_count} PDFs. Need {to_download} more.")

if to_download <= 0:
    print("Sufficient PDFs downloaded.")
    exit(0)

# We search broad queries
queries = [
    '"Business Intelligence Roadmap"',
    '"Business Intelligence Roadmap" AND (pendidikan OR universitas OR kampus OR "perguruan tinggi" OR akademik)',
    '("Business Intelligence Roadmap" OR "Larissa T. Moss") AND "perguruan tinggi"',
    '"Business Intelligence" AND "Tableau" AND "Universitas"'
]

headers = {'User-Agent': 'mailto:test234@example.com'}

downloaded = 0
seen_titles = set()

for query in queries:
    if downloaded >= to_download:
        break
        
    print(f"==== Searching OpenAlex for: {query} ====")
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&has_oa_hosted_pdf=true&per-page=50"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            continue
            
        data = resp.json()
         
        for work in data.get('results', []):
            if downloaded >= to_download:
                break
                
            title = work.get('title')
            if not title or title.lower() in seen_titles:
                continue
            seen_titles.add(title.lower())
            
            pdf_url = None
            if work.get('best_oa_location'):
                pdf_url = work['best_oa_location'].get('pdf_url')
            if not pdf_url:
                for loc in work.get('locations', []):
                    if loc.get('pdf_url'):
                        pdf_url = loc['pdf_url']
                        break
                        
            if pdf_url and '.pdf' in pdf_url.lower():
                print(f"Trying to download: {title}\n  URL: {pdf_url}")
                try:
                    pdf_resp = requests.get(pdf_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                    if pdf_resp.status_code == 200 and b'%PDF' in pdf_resp.content[:10]:
                        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                        filepath = output_dir / f"{safe_title[:50]}.pdf"
                        if not filepath.exists():
                            with open(filepath, 'wb') as f:
                                f.write(pdf_resp.content)
                            print(f"  -> SUCCESS: Saved to {filepath.name}")
                            downloaded += 1
                        else:
                            print(f"  -> ALREADY EXISTS")
                    else:
                        print(f"  -> FAILED: Invalid PDF or status {pdf_resp.status_code}")
                except Exception as e:
                    print(f"  -> ERROR downloading: {e}")
            time.sleep(1) # be polite to OpenAlex and hosts
            
    except Exception as e:
        print(f"Error querying: {e}")

print(f"\nDone! Downloaded {downloaded} new PDFs.")
