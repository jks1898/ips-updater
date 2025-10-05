import requests, socket, concurrent.futures, os, time, random

# ---------- 配置 ----------
OUTPUT_FILE = "hk_ips.txt"
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN", "652658c50a1b7f")  # 从 Secrets 或本地环境
MAX_THREADS = 10       # 并发线程
PING_TIMEOUT = 2       # TCP 超时（秒）
PING_TRIES = 2         # 测试次数
TOP_N = 10             # 输出前 N 个延迟最低 IP

# 固定香港 Cloudflare IP 段（备用源）
HK_IPS = [
    "104.16.0.0", "104.16.1.0", "104.18.0.0", "104.18.1.0",
    "162.159.0.0", "162.159.1.0", "172.64.0.0", "172.64.1.0"
]

# ---------- 获取地理位置 ----------
def get_country(ip):
    url = f"https://ipinfo.io/{ip}/lite"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        data = requests.get(url, timeout=3).text
        country = re.search(r'"country": ?"(\w+)"', data)
        region = re.search(r'"region": ?"([^"]+)"', data)
        city = re.search(r'"city": ?"([^"]+)"', data)
        return (country.group(1) if country else "", 
                region.group(1) if region else "", 
                city.group(1) if city else "")
    except:
        return "", "", ""

# ---------- TCP测速 ----------
def ping(ip, port=443, timeout=PING_TIMEOUT, tries=PING_TRIES):
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
    return sum(latencies)/len(latencies) if latencies else 9999

# ---------- 并发处理 ----------
def process(ip):
    country, region, city = get_country(ip)
    if country == "HK":
        avg = ping(ip)
        print(f"{ip} 延迟: {avg:.2f} ms")
        return (ip, country, region, city, avg)
    return None

# ---------- 主逻辑 ----------
print(f"候选香港 IP 数量: {len(HK_IPS)}")
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
    results = list(filter(None, ex.map(process, HK_IPS)))

# 输出前 N 个
results.sort(key=lambda x: x[4])
top_n = results[:TOP_N]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# 优选香港IP（前{TOP_N}个最低延迟）\n")
    f.write("# ip\tcountry\tregion\tcity\tavg_ms\n")
    for ip, c, r, city, avg in top_n:
        f.write(f"{ip}\t{c}\t{r}\t{city}\t{avg:.2f}\n")

print(f"✅ 已输出 {len(top_n)} 个香港 IP 到 {OUTPUT_FILE}")
