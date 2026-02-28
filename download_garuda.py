import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)
existing = len(list(output_dir.glob("*.pdf")))
needed = 10 - existing

if needed <= 0:
    print("Already have enough PDFs")
    exit(0)

print(f"Need {needed} more PDFs")

# We will scrape Garuda Ristekdikti
queries = [
    "Business Intelligence Roadmap",
    "Business Intelligence Pendidikan",
    "Business Intelligence Universitas",
    "Moss Atre Business Intelligence"
]

downloaded = 0
found_links = set()

def try_download(url, filename_prefix):
    try:
        # Some URLs might be external publishers but sometimes Garuda provides direct PDF or we get it via publisher redirect
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if resp.status_code == 200 and b'%PDF' in resp.content[:10]:
            name = f"{filename_prefix}.pdf"
            path = output_dir / name
            if not path.exists():
                with open(path, 'wb') as f:
                    f.write(resp.content)
                print(f"  -> SUCCESS: {name}")
                return True
        else:
            # Let's try to parse HTML for an OJS download link
            if resp.status_code == 200 and b'html' in resp.content[:100].lower():
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Look for typical OJS PDF download links
                for a in soup.find_all('a'):
                    href = a.get('href', '')
                    if 'article/download' in href or 'pdf' in href.lower():
                        if not href.startswith('http'):
                            continue
                        print(f"  -> Found OJS PDF link: {href}")
                        pdf_resp = requests.get(href, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                        if pdf_resp.status_code == 200 and b'%PDF' in pdf_resp.content[:10]:
                            name = f"{filename_prefix}_OJS.pdf"
                            path = output_dir / name
                            if not path.exists():
                                with open(path, 'wb') as f:
                                    f.write(pdf_resp.content)
                                print(f"  -> SUCCESS (OJS): {name}")
                                return True
            print(f"  -> FAILED: Status {resp.status_code} or not PDF")
    except Exception as e:
        print(f"  -> ERROR: {e}")
    return False

for query in queries:
    if downloaded >= needed:
        break
    url = f"https://garuda.kemdikbud.go.id/documents?q={query.replace(' ', '+')}"
    print(f"Searching Garuda: {url}")
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Find article links
        for a in soup.find_all('a', class_='title'):
            if downloaded >= needed:
                break
            article_url = a.get('href')
            if not article_url:
                continue
            if not article_url.startswith('http'):
                article_url = 'https://garuda.kemdikbud.go.id' + article_url
                
            title = a.text.strip()
            print(f"Found Article: {title}")
            
            # Request the article page to find the Original Source button
            art_resp = requests.get(article_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            art_soup = BeautifulSoup(art_resp.text, 'html.parser')
            
            # Find the "Original Source" link
            source_link = None
            for s_a in art_soup.find_all('a'):
                href = s_a.get('href', '')
                if 'Original Source' in s_a.text or 'download' in href:
                    if href.startswith('http'):
                        source_link = href
                        break
            
            if source_link:
                if source_link in found_links:
                    continue
                found_links.add(source_link)
                
                print(f"Trying source link: {source_link}")
                safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                if try_download(source_link, safe_title[:50]):
                    downloaded += 1
            else:
                 print("  -> No source link found in Garuda page.")
            time.sleep(1)
            
    except Exception as e:
        print(f"Error scraping Garuda: {e}")

print(f"Finished. Downloaded {downloaded} new files.")
