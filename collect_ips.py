import requests
from bs4 import BeautifulSoup

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "ips.txt"

# 请求网页
resp = requests.get(URL)
resp.encoding = resp.apparent_encoding
soup = BeautifulSoup(resp.text, "html.parser")

# 提取表格数据
lines = soup.get_text().splitlines()
data = []

for line in lines:
    line = line.strip()
    if not line or line.startswith("优选地址") or "毫秒" not in line:
        continue
    parts = line.split()
    if len(parts) < 4:
        continue
    ip = parts[0]
    latency_str = parts[3]  # 电信延迟(节点)
    try:
        # 提取数值
        latency = int(latency_str.replace("毫秒(SIN)", ""))
        data.append((ip, latency))
    except:
        continue

# 按电信延迟升序排序，取前6个
data.sort(key=lambda x: x[1])
top6 = data[:6]

# 写入 ips.txt，备注为 CT
with open(OUTPUT, "w") as f:
    for ip, _ in top6:
        f.write(f"{ip}#CT\n")

print(f"✅ 已写入前6个电信延迟 IP 到 {OUTPUT}")
