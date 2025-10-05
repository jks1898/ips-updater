import requests, re, os, time, concurrent.futures

OUTPUT_FILE = "ips.txt"
TOP_N = 10              # 输出前 N 个 IP
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN", "")  # GitHub Secrets 或本地环境
MAX_THREADS = 10        # 并发线程

# 候选 IP 列表，可以从 Cloudflare IP 段或 wetest 页面抓取
CANDIDATE_IPS = [
    "104.16.0.0", "104.16.1.0", "104.18.0.0", "104.18.1.0",
    "162.159.0.0", "162.159.1.0", "172.64.0.0", "172.64.1.0",
    "104.17.0.0", "104.17.1.0", "162.159.2.0", "172.65.0.0"
]

def is_hk(ip):
    """通过 ipinfo.io 判断是否为香港 IP"""
    url = f"https://ipinfo.io/{ip}/lite"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        resp = requests.get(url, timeout=3).text
        return '"country":"HK"' in resp
    except:
        return False

def process(ip):
    if is_hk(ip):
        print(f"{ip} 是香港 IP")
        return ip
    return None

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
    results = list(filter(None, ex.map(process, CANDIDATE_IPS)))

top_n = results[:TOP_N]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip in top_n:
        f.write(f"{ip}#HK\n")

print(f"✅ 已生成 {OUTPUT_FILE}，共 {len(top_n)} 个香港 IP")
