import requests, re, time, socket, concurrent.futures

WETEST_URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT_FILE = "hk_ips.txt"
IPINFO_TOKEN = ""

headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(WETEST_URL, headers=headers, timeout=10)
ips = list(set(re.findall(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', resp.text)))

def get_country(ip):
    url = f"https://ipinfo.io/{ip}/json"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        data = requests.get(url, timeout=3).json()
        return data.get("country", ""), data.get("region", ""), data.get("city", "")
    except:
        return "", "", ""

def ping(ip, port=443, timeout=0.5, tries=3):
    latencies = []
    for _ in range(tries):
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
            latencies.append((time.time() - start) * 1000)
        except:
            pass
        s.close()
    return sum(latencies) / len(latencies) if latencies else 9999

def process(ip):
    country, region, city = get_country(ip)
    if country == "HK":
        avg = ping(ip)
        return (ip, country, region, city, avg)

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
    results = list(filter(None, ex.map(process, ips)))

results.sort(key=lambda x: x[4])
top10 = results[:10]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("# 优选香港IP（前10个最低延迟）\n")
    f.write("# ip\tcountry\tregion\tcity\tavg_ms\n")
    for ip, c, r, city, avg in top10:
        f.write(f"{ip}\t{c}\t{r}\t{city}\t{avg:.2f}\n")

print(f"✅ 已输出 {len(top10)} 个香港 IP 到 {OUTPUT_FILE}")
