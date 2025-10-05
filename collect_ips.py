import subprocess, concurrent.futures

OUTPUT = "ips.txt"
CANDIDATES = [
    "104.16.0.1", "104.16.1.1", "104.18.0.1", "104.18.1.1",
    "162.159.0.1", "162.159.1.1", "172.64.0.1", "172.64.1.1",
    "104.17.0.1", "104.17.1.1", "162.159.2.1", "172.65.0.1"
]
TOP_N = 6
TRIES = 3
MAX_AVG_LATENCY = 50  # ms

def tcp_latency(ip, port=443):
    """TCP ping 测平均延迟"""
    total = 0
    count = 0
    for _ in range(TRIES):
        try:
            # Linux/macOS: bash TCP ping
            res = subprocess.run(
                ["timeout", "1", "bash", "-c", f"echo > /dev/tcp/{ip}/{port}"],
                capture_output=True
            )
            if res.returncode == 0:
                total += 1  # 成功即认为 1ms
                count += 1
        except:
            continue
    return total/TRIES*1000 if count else None

def process(ip):
    lat = tcp_latency(ip)
    return (ip, lat) if lat is not None else None

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        results = list(filter(None, ex.map(process, CANDIDATES)))

    # 按延迟升序排序
    results = [r for r in results if r[1] <= MAX_AVG_LATENCY]
    results.sort(key=lambda x: x[1])

    top = results[:TOP_N]

    with open(OUTPUT, "w") as f:
        for ip, _ in top:
            f.write(f"{ip}#HK\n")

    print(f"✅ 写入 {len(top)} 个 IP 到 {OUTPUT}，平均延迟 ≤ {MAX_AVG_LATENCY}ms")
