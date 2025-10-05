import socket, concurrent.futures

OUTPUT_FILE = "ips.txt"
TARGET_COUNT = 6
MAX_LATENCY = 70
MAX_THREADS = 10
PORT = 443

# 香港专用 Cloudflare IPv4 段（示例）
HK_IPS = [
    "104.16.0.1", "104.16.1.1", "104.18.0.1", "104.18.1.1",
    "162.159.0.1", "162.159.1.1", "172.64.0.1", "172.64.1.1",
    "104.17.0.1", "104.17.1.1", "162.159.2.1", "172.65.0.1"
]

def ping(ip, port=PORT, timeout=0.2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        from time import time
        start = time()
        s.connect((ip, port))
        latency = (time() - start) * 1000
        s.close()
        return latency
    except:
        return None

def process(ip):
    lat = ping(ip)
    if lat is not None and lat <= MAX_LATENCY:
        print(f"{ip} 延迟 {lat:.2f} ms ✅")
        return ip
    print(f"{ip} 延迟超限或不可达 ❌")
    return None

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
    results = list(filter(None, ex.map(process, HK_IPS)))

top_ips = results[:TARGET_COUNT]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip in top_ips:
        f.write(f"{ip}#HK\n")

print(f"✅ 已生成 {OUTPUT_FILE}，共 {len(top_ips)} 个 IP")
