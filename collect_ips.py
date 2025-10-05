import requests
from bs4 import BeautifulSoup

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "ips.txt"

# 请求网页
resp = requests.get(URL)
resp.encoding = resp.apparent_encoding
soup = BeautifulSoup(resp.text, "html.parser")

# 找到统计优选列表的表格
lines = soup.get_text().splitlines()
data = []

for line in lines:
    if "毫秒(SIN)" in line:  # 电信延迟节点标识
        parts = line.split()
        ip = parts[0]
        # 电信延迟一般在第三列
        try:
            latency_str = [p for p in parts if "毫秒(SIN)" in p][0]
            latency = int(latency_str.replace("毫秒(SIN)", ""))
            data.append((ip, latency))
        except:
            continue

# 按电信延迟升序排序，取前5个
data.sort(key=lambda x: x[1])
top5 = data[:5]

# 写入 ips.txt
with open(OUTPUT, "w") as f:
    for ip, _ in top5:
        f.write(f"{ip}#CT\n")

print(f"✅ 已写入前5个电信延迟 IP 到 {OUTPUT}")
