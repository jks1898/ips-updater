import requests, re, time, socket, concurrent.futures, os

# ---------- 配置 ----------
WETEST_URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT_FILE = "hk_ips.txt"
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN", "")  # GitHub Secrets 或本地环境
MAX_THREADS = 10       # 并发线程数
PING_TIMEOUT = 1       # TCP 超时（秒）
PING_TRIES = 3         # 每个 IP 测试次数
TOP_N = 10             # 输出前 N 个延迟最低 IP

# ---------- 获取候选 IP ----------
try:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(WETEST_URL, headers=headers, timeout=10)
    ips = list(set(re.findall(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', resp.text)))
    print(f"抓取到候选 IP 数量: {len(ips)}")
except Exception as e:
    print(f"获取候选 IP 失败: {e}")
    ips = []

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

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
    results = list(filter(None, ex.map(process, ips)))

# ---------- 输出前 N 个 ----------
results.sort(key=lambda x: x[4])
top_n = results[:TOP_N]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# 优选香港IP（前{TOP_N}个最低延迟）\n")
    f.write("# ip\tcountry\tregion\tcity\tavg_ms\n")
    for ip, c, r, city, avg in top_n:
        f.write(f"{ip}\t{c}\t{r}\t{city}\t{avg:.2f}\n")

print(f"✅ 已输出 {len(top_n)} 个香港 IP 到 {OUTPUT_FILE}")
