import requests, re, os

site = "https://taraftarsporamp31.pages.dev/"
output_path = "/storage/emulated/0/Download/taraftarium24_auto.m3u"

print("[+] Connecting to main site:", site)
try:
    html = requests.get(site, timeout=10).text
except:
    print("[-] Unable to reach the site!")
    exit()

links = re.findall(r'https:\/\/[a-zA-Z0-9\.\-\/]+player-[a-zA-Z0-9]+', html)
links = list(dict.fromkeys(links))

if not links:
    print("[-] No player links found.")
    exit()

print(f"[+] Found {len(links)} channels.")

channels = []
for link in links:
    referrer = re.match(r'(https:\/\/[^\/]+)', link).group(1)
    short = re.search(r'player\-([a-zA-Z0-9]+)', link).group(1).lower()

    name = short.upper()
    if re.match(r'bsn(\d+)', short):
        num = re.findall(r'\d+', short)[0]
        name = f"Bein {num}"
    elif re.match(r'mx(\d+)', short):
        num = re.findall(r'\d+', short)[0]
        name = f"Bein Max {num}"
    elif re.match(r's(\d+)', short):
        num = re.findall(r'\d+', short)[0]
        name = f"S-Sport {num}"
    elif re.match(r'tvb(\d+)', short):
        num = re.findall(r'\d+', short)[0]
        name = f"Tivibu {num}"

    print(f"[*] Scanning: {name}")

    try:
        headers = {"Referer": referrer, "User-Agent": "Mozilla/5.0"}
        page = requests.get(link, headers=headers, timeout=10).text
    except:
        print(f"[-] Failed to fetch page for {name}")
        continue

    m3u8 = re.findall(r'https?:\/\/[^\s\'"]+\.m3u8[^\s\'"]*', page)
    if not m3u8:
        print(f"[-] Stream not found for {name}")
        continue

    stream = m3u8[0]
    channels.append((name, stream))
    print(f"[+] Stream found: {name}")

if channels:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch_name, ch_url in channels:
            f.write(f'#EXTINF:-1 group-title="taraftarium",{ch_name}\n{ch_url}\n')
    print(f"\n✅ M3U file saved to: {output_path}")
else:
    print("[-] No streams available.")
