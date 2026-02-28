import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import time

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    links = []
    for a in soup.find_all('a', class_='result__url'):
        href = a.get('href')
        if href:
            if href.startswith('//duckduckgo.com/l/?'):
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if 'uddg' in parsed:
                    link = parsed['uddg'][0]
                    if link.lower().endswith('.pdf'):
                        links.append(link)
            elif href.lower().endswith('.pdf'):
                links.append(href)
    return links

queries = [
    '"Business Intelligence Roadmap" "pendidikan" ext:pdf',
    '"Business Intelligence Roadmap" "perguruan tinggi" ext:pdf',
    '"Business Intelligence Roadmap" "universitas" ext:pdf',
    '"Business Intelligence Roadmap" "kampus" ext:pdf',
    '"Larissa T. Moss" "Business Intelligence Roadmap" "pendidikan" ext:pdf'
]

all_links = set()
for q in queries:
    print(f"Searching: {q}")
    links = search_ddg(q)
    print(f"Found {len(links)} links")
    for link in links:
        all_links.add(link)
    time.sleep(2)

print(f"\nTotal unique PDF links: {len(all_links)}")
for link in all_links:
    print(link)
