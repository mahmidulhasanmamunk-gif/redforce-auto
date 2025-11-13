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
            print("Failed to load page")
            return []

        channels = []

        # Step 1: Extract from JavaScript (var channels = [...])
        js_match = re.search(r'var\s+channels\s*=\s*(\[[\s\S]*?\]);', response.text, re.DOTALL)
        if js_match:
            try:
                import json
                data = json.loads(js_match.group(1))
                for ch in data:
                    stream = ch.get('stream_url') or ch.get('url') or ch.get('stream')
                    if stream and '.m3u8' in str(stream):
                        name = ch.get('name', 'Unknown')
                        url = stream if str(stream).startswith('http') else urljoin(BASE_URL, str(stream))
                        channels.append({'name': name.strip(), 'url': url})
                if channels:
                    print(f"Success: Found {len(channels)} channels from JS")
                    return channels
            except:
                pass

        # Step 2: Fallback - Find all .m3u8 links
        m3u8_links = re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', response.text)
        name_elements = re.findall(r'channel[^>]*name[^>]*>([^<]+)', response.text, re.IGNORECASE)

        for i, link in enumerate(m3u8_links):
            name = name_elements[i].strip() if i < len(name_elements) else f"Channel {i+1}"
            full_url = link if link.startswith('http') else urljoin(BASE_URL, link)
            if full_url not in [c['url'] for c in channels]:
                channels.append({'name': name, 'url': full_url})

        print(f"Success: Found {len(channels)} channels (total)")
        return channels

    except Exception as e:
        print(f"Error: {e}")
        return []

def generate_m3u(channels):
    if not channels:
        return "#EXTM3U\n# No channels found - check connection or site\n"
    
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
    print(f"redforce.m3u created with {len(channels)} channels")
