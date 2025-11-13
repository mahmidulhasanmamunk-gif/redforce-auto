import requests
import re
from urllib.parse import urljoin
import datetime

# Your website URL – only this line is changed
BASE_URL = "http://redforce.live"
OUTPUT_FILE = "redforce.m3u"

def get_channels():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(BASE_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print("Site down")
            return fallback_channels()

        channels = []
        # Extract .m3u8 links from page source
        links = re.findall(r'["\'](https?://[^"\']*\.m3u8[^"\']*)["\']', response.text)
        names = re.findall(r'channel[^>]*>([^<]+)', response.text, re.I) or \
                re.findall(r'title=["\']([^"\']+)["\']', response.text)

        for i, url in enumerate(links[:100]):
            name = names[i].strip() if i < len(names) else f"Channel {i+1}"
            channels.append({"name": name, "url": url, "group": "RedForce"})

        if not channels:
            return fallback_channels()

        print(f"Found {len(channels)} channels")
        return channels

    except Exception as e:
        print(f"Error: {e}")
        return fallback_channels()

def fallback_channels():
    print("Using fallback channels")
    return [
        {"name": "GTV HD", "url": "http://bdixsports.com:8080/live/gtv/playlist.m3u8", "group": "Bangla"},
        {"name": "Cartoon Network", "url": "http://bdixsports.com:8080/live/cartoon/playlist.m3u8", "group": "Kids"},
        {"name": "Star Sports 1", "url": "http://bdixsports.com:8080/live/starsports1/playlist.m3u8", "group": "Sports"}
    ]

def generate_m3u(channels):
    m3u = "#EXTM3U\n"
    m3u += f"# Auto Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    m3u += f"# Source: {BASE_URL}\n\n"
    for ch in channels:
        m3u += f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}\n'
        m3u += f'{ch["url"]}\n'
    return m3u

if __name__ == "__main__":
    channels = get_channels()
    content = generate_m3u(channels)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OUTPUT_FILE} created with {len(channels)} channels")
