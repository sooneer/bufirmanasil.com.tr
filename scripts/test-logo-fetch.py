import requests
from bs4 import BeautifulSoup

url = "https://airadio.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/121.0'
}

try:
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find og:image
    og_image = soup.find('meta', property='og:image')
    if og_image:
        print(f"og:image: {og_image.get('content')}")

    # Find logo images
    logo_imgs = soup.select('img[class*="logo"], img[id*="logo"]')
    print(f"\nFound {len(logo_imgs)} logo images:")
    for img in logo_imgs[:5]:
        print(f"  - src: {img.get('src')}, alt: {img.get('alt')}")

    # Find favicon
    favicon = soup.find('link', rel='icon')
    if favicon:
        print(f"\nfavicon: {favicon.get('href')}")

except Exception as e:
    print(f"Error: {e}")
