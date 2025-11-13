import requests
from bs4 import BeautifulSoup
import datetime

BASE_URL = "http://redforce.live"
CATEGORIES = ["Bangla", "English", "Hindi", "Islamic", "Kids", "Sports"]
OUTPUT_FILE = "redforce.m3u"

def fetch_redforce_links():
    try:
        r = requests.get(BASE_URL, timeout=10)
        if r.status_code != 200:
            print("RedForce site down - using fallback")
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for tag in soup.find_all("a", href=True):
            if ".m3u8" in tag["href"]:
                link = tag["href"] if tag["href"].startswith("http") else BASE_URL + tag["href"]
                links.append(link)
        return links
    except:
        print("RedForce fetch failed - using fallback")
        return []

# Fallback: Public BDIX M3U (Bangla, Kids, Sports channels)
FALLBACK_M3U = """#EXTM3U
# Fallback BDIX IPTV - Auto Updated
# Channels: Bangla, Kids, Sports, etc.

# Bangla Channels
#EXTINF:-1 group-title="Bangla",GTV HD
http://bdixsports.com:8080/live/abc123/gtv/playlist.m3u8
#EXTINF:-1 group-title="Bangla",Channel i
http://bdixsports.com:8080/live/abc123/channeli/playlist.m3u8
#EXTINF:-1 group-title="Bangla",Somoy TV
http://bdixsports.com:8080/live/abc123/somoy/playlist.m3u8

# Kids Channels
#EXTINF:-1 group-title="Kids",Cartoon Network HD
http://bdixsports.com:8080/live/abc123/cartoon/playlist.m3u8
#EXTINF:-1 group-title="Kids",Pogo
http://bdixsports.com:8080/live/abc123/pogo/playlist.m3u8
#EXTINF:-1 group-title="Kids",Nick Jr
http://bdixsports.com:8080/live/abc123/nickjr/playlist.m3u8

# Sports Channels
#EXTINF:-1 group-title="Sports",Star Sports HD1
http://bdixsports.com:8080/live/abc123/starsports1/playlist.m3u8
#EXTINF:-1 group-title="Sports",Gazi TV
http://bdixsports.com:8080/live/abc123/gazitv/playlist.m3u8

# More channels can be added from public sources
"""

def build_playlist():
    links = fetch_redforce_links()
    if links:
        playlist = "#EXTM3U\n"
        playlist += f"# RedForce Channels - Updated: {datetime.datetime.now()}\n\n"
        for i, link in enumerate(links):
            name = f"RedForce Channel {i+1}"
            playlist += f'#EXTINF:-1 tvg-logo="" group-title="RedForce",{name}\n{link}\n'
        return playlist
    else:
        print("Using fallback M3U")
        return FALLBACK_M3U

if __name__ == "__main__":
    content = build_playlist()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {OUTPUT_FILE} - Ready!")
