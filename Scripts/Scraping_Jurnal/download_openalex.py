import requests
import json
import urllib.parse
from pathlib import Path
import os
import time

titles = [
    "Business Intelligence Framework for Performance Measurement in Higher Education Study Programs",
    "Business Intelligence Roadmap for Tableau Dashboard Development in Higher Education",
    "Roadmap for Implementing Business Intelligence Systems in Higher Education Institutions: Systematic Literature Review",
    "Analysis of business intelligence system design for student performance monitoring",
    "Application of Business Intelligence in the Analysis and Visualization of Alumni Data Using the Tableau Platform",
    "Implementasi Business Intelligence Menggunakan Tableau untuk Visualisasi Prediksi Kelulusan Mahasiswa",
    "Penerapan Business Intelligence Pada Unit Penunjang Akademik Teknologi Informasi Dan Komunikasi Universitas Negeri Manado",
    "Pemanfaatan Business Intelligence di Perguruan Tinggi"
]

output_dir = Path("d:/Code/Tugas Akhir/Referensi Business Intelligence Roadmap")
output_dir.mkdir(parents=True, exist_ok=True)

headers = {'User-Agent': 'mailto:test@example.com'} # OpenAlex prefers an email

for i, title in enumerate(titles, 1):
    query = f"https://api.openalex.org/works?search={urllib.parse.quote(title)}"
    try:
        resp = requests.get(query, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get('results', [])
            if results:
                work = results[0]
                pdf_url = None
                if work.get('best_oa_location'):
                    pdf_url = work['best_oa_location'].get('pdf_url')
                if not pdf_url:
                    for loc in work.get('locations', []):
                        if loc.get('pdf_url'):
                            pdf_url = loc['pdf_url']
                            break
                
                print(f"{i}. {title}")
                if pdf_url:
                    print(f"   PDF: {pdf_url}")
                    # Try to download it
                    try:
                        pdf_resp = requests.get(pdf_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                        if pdf_resp.status_code == 200 and b'%PDF' in pdf_resp.content[:10]:
                            safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                            filepath = output_dir / f"{safe_title[:50]}.pdf"
                            with open(filepath, 'wb') as f:
                                f.write(pdf_resp.content)
                            print(f"   -> Downloaded to {filepath}")
                        else:
                            print(f"   -> Failed to download or not a PDF (Status: {pdf_resp.status_code})")
                    except Exception as e:
                        print(f"   -> Error downloading: {e}")
                else:
                    print("   No PDF URL found.")
            else:
                print(f"{i}. {title}\n   No results found.")
        else:
             print(f"Error for {title}: {resp.status_code}")
    except Exception as e:
        print(f"Error querying {title}: {e}")
    
    time.sleep(1)
