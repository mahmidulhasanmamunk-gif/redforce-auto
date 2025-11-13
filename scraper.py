import requests
from bs4 import BeautifulSoup
import datetime
import os

# ---------- CONFIG ----------
BASE_URL = "http://redforce.live"
CATEGORIES = ["Bangla", "English", "Hindi", "Islamic", "Kids", "Sports"]
OUTPUT_FILE = "redforce.m3u"
# ----------------------------

def fetch_links(category):
    url = f"{BASE_URL}/{category.lower()}"
    print(f"[+] Scanning: {url}")
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            print(f"[!] {category}: Status {r.status_code}")
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if ".m3u8" in href:
                link = href if href.startswith("http") else BASE_URL + href
                links.append(link)
        print(f"[+] {category}: {len(links)} links")
        return links
    except Exception as e:
        print(f"[x] Error in {category}: {e}")
        return []

def build_playlist():
    all_links = []
    for cat in CATEGORIES:
        for link in fetch_links(cat):
            name = link.split("/")[-1].replace(".m3u8", "").replace("-", " ").title()
            all_links.append((cat, name, link))

    if not all_links:
        print("[!] No channels found. Using fallback.")
        return "#EXTM3U\n# No live channels - redforce.live may be down\n"

    playlist = "#EXTM3U\n"
    playlist += f"# Auto Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    for cat, name, link in all_links:
        playlist += f'#EXTINF:-1 tvg-logo="" group-title="{cat}",{name}\n{link}\n'
    return playlist

if __name__ == "__main__":
    print("Building RedForce M3U Playlist...")
    content = build_playlist()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OUTPUT_FILE} created with {content.count('#EXTINF')}+ channels")
