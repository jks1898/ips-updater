import socket, concurrent.futures

OUTPUT_FILE = "ips.txt"
TARGET_COUNT = 6       # 目标 IP 数量
MAX_LATENCY = 70       # 延迟阈值 (ms)
MAX_THREADS = 10       # 并发线程
PORT = 443             # TCP 测速端口

# Cloudflare 香港专用 IPv4 段（示例）
HK_IPS = [
    "104.16.0.1", "104.16.1.1", "104.18.0.1", "104.18.1.1",
    "162.159.0.1", "162.159.1.1", "172.64.0.1", "172.64.1.1",
    "104.17.0.1", "104.17.1.1", "162.159.2.1", "172.65.0.1"
]

def ping(ip, port=PORT, timeout=0.2):
    """TCP 测延迟，返回毫秒"""
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

# ---------- 并发测速 ----------
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
    results = list(filter(None, ex.map(process, HK_IPS)))

# 取前 TARGET_COUNT 个
top_ips = results[:TARGET_COUNT]

# ---------- 写入文件 ----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip in top_ips:
        f.write(f"{ip}#HK\n")

print(f"✅ 已生成 {OUTPUT_FILE}，共 {len(top_ips)} 个 IP")
