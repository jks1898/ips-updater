import requests, concurrent.futures, time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OUTPUT_FILE = "ips.txt"
TARGET_COUNT = 6
MAX_AVG_LATENCY = 50   # 平均延迟阈值 ms
MAX_THREADS = 10
REQUEST_TRIES = 3      # 每个 IP 请求次数

# 香港专用 Cloudflare IPv4 段（可扩展更多 IP）
HK_IPS = [
    "104.16.0.1", "104.16.1.1", "104.18.0.1", "104.18.1.1",
    "162.159.0.1", "162.159.1.1", "172.64.0.1", "172.64.1.1",
    "104.17.0.1", "104.17.1.1", "162.159.2.1", "172.65.0.1"
]

def http_latency(ip, tries=REQUEST_TRIES):
    url = f"https://{ip}/"  # 请求根路径
    latencies = []
    for _ in range(tries):
        try:
            start = time.time()
            requests.get(url, timeout=0.5, verify=False)
            latencies.append((time.time() - start) * 1000)
        except:
            pass
    if latencies:
        return sum(latencies)/len(latencies)
    return None

def process(ip):
    avg_lat = http_latency(ip)
    if avg_lat is not None and avg_lat <= MAX_AVG_LATENCY:
        print(f"{ip} 平均延迟 {avg_lat:.2f} ms ✅")
        return (ip, avg_lat)
    print(f"{ip} 延迟过高或不可达 ❌")
    return None

# ---------- 并发测速 ----------
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
    results = list(filter(None, ex.map(process, HK_IPS)))

# 按平均延迟排序
results.sort(key=lambda x: x[1])

# 取前 TARGET_COUNT 个
top_ips = results[:TARGET_COUNT]

# ---------- 输出到文件 ----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip, _ in top_ips:
        f.write(f"{ip}#HK\n")

print(f"✅ 已生成 {OUTPUT_FILE}，共 {len(top_ips)} 个 IP，平均延迟 ≤ {MAX_AVG_LATENCY}ms")
