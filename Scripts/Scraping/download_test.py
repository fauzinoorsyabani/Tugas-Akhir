import requests
url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE2OXxkBEzNuXjrdpCZsN8Yr1ZCJ-TPfS9Ess7yDJkv9w8guv5hdSt4mr-DfTwMZWPx3TeV5ZPcFdaGpUu3lCD1DxFsLu3uTSQhphJ75LoyIHaElfFIc2GXu5tTKQP6TtN169mTUe_bFaDT4q0YWTys4yKliOq9C4VSgVysbC0RBzQ="
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers, allow_redirects=True)
print(f"Status Code: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('Content-Type')}")
with open('test_download.pdf', 'wb') as f:
    f.write(resp.content)
