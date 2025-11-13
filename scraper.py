import requests
import re
from urllib.parse import urljoin

BASE_URL = "http://redforce.live"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
}

def get_channels():
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"Failed to load page: {response.status_code}")
            return []

        channels = []

        # Step 1: Find all .m3u8 links (these are direct stream URLs)
        m3u8_pattern = r'href=["\']([^"\']*\.m3u8[^"\']*)["\']'
        m3u8_links = re.findall(m3u8_pattern, response.text)

        # Step 2: Extract channel names from <div class="channel-name">
        name_pattern = r'<div[^>]+class=["\'][^"\']*channel-name[^"\']*["\'][^>]*>([^<]+)</div>'
        names = re.findall(name_pattern, response.text)

        # Step 3: Match links with names
        for i, link in enumerate(m3u8_links):
            name = names[i].strip() if i < len(names) else f"Channel {i+1}"
            full_url = link if link.startswith('http') else urljoin(BASE_URL, link)
            channels.append({'name': name, 'url': full_url})

        print(f"Found {len(channels)} channels")
        return channels

    except Exception as e:
        print(f"Error: {e}")
        return []

def generate_m3u(channels):
    m3u = "#EXTM3U\n"
    for ch in channels:
        m3u += f'#EXTINF:-1 tvg-logo="" group-title="RedForce",{ch["name"]}\n'
        m3u += f'{ch["url"]}\n'
    return m3u

if __name__ == "__main__":
    channels = get_channels()
    m3u_content = generate_m3u(channels)
    with open("redforce.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Generated redforce.m3u with {len(channels)} channels")
