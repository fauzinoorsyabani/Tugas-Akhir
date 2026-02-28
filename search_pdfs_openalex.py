import requests
import json
import urllib.parse
from pathlib import Path

def search_openalex():
    # OpenAlex search:
    query = '"Business Intelligence Roadmap" (pendidikan OR universitas OR kampus OR "perguruan tinggi")'
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&has_oa_hosted_pdf=true&per-page=25"
    
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        
        results = []
        for work in data.get('results', []):
            pdf_url = None
            if work.get('best_oa_location'):
                pdf_url = work['best_oa_location'].get('pdf_url')
            if not pdf_url:
                for loc in work.get('locations', []):
                    if loc.get('pdf_url'):
                        pdf_url = loc['pdf_url']
                        break
            
            if pdf_url:
                title = work.get('title', 'Unknown Title')
                results.append((title, pdf_url))
        
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

pdf_links = search_openalex()
print(f"Found {len(pdf_links)} works with PDFs")

for idx, (title, pdf_url) in enumerate(pdf_links, 1):
    print(f"{idx}. {title}\n   {pdf_url}")
