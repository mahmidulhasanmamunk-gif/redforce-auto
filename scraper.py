import requests
import re
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://redforce.live"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
}

def get_channels():
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"Failed to load: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract active users and categories
        active_users = re.search(r'Active Users: (\d+)', response.text)
        print(f"Active Users: {active_users.group(1) if active_users else 'Unknown'}")

        # Find channel data from JS or HTML
        channels = []
        
        # Look for JS array with channel data (common in IPTV sites)
        js_match = re.search(r'channels\s*=\s*(\[.*?\]);', response.text, re.DOTALL | re.IGNORECASE)
        if js_match:
            try:
                data = json.loads(js_match.group(1))
                for ch in data:
                    name = ch.get('name', 'Unknown')
                    stream = ch.get('stream') or ch.get('url')
                    if stream and '.m3u8' in stream:
                        url = stream if stream.startswith('http') else urljoin(BASE_URL, stream)
                        channels.append({'name': name, 'url': url})
            except:
                pass

        # Fallback: Extract from HTML links (channel logos)
        if not channels:
            channel_links = soup.find_all('a', href=True)
            for link in channel_links:
                href = link.get('href', '')
                if '.m3u8' in href:
                    name = link.get('title') or link.text.strip() or 'Channel'
                    url = href if href.startswith('http') else urljoin(BASE_URL, href)
                    channels.append({'name': name, 'url': url})

        # Add categories as groups
        categories = ['Bangla', 'English', 'Hindi', 'Islamic', 'Kids', 'Sports']
        for i, ch in enumerate(channels):
            ch['group'] = categories[i % len(categories)]

        print(f"Found {len(channels)} channels")
        return channels

    except Exception as e:
        print(f"Error: {e}")
        return []

def generate_m3u(channels):
    m3u = "#EXTM3U\n"
    m3u += f"# RedForce IPTV - Auto Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    m3u += "# Source: http://redforce.live\n\n"
    
    for ch in channels:
        m3u += f'#EXTINF:-1 tvg-logo="" group-title="{ch["group"]}",{ch["name"]}\n'
        m3u += f'{ch["url"]}\n'
    
    return m3u

if __name__ == "__main__":
    channels = get_channels()
    content = generate_m3u(channels)
    with open("redforce.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated redforce.m3u with {len(channels)} channels")
