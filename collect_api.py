import requests
from bs4 import BeautifulSoup
import re

URL_164746 = "https://ip.164746.xyz/"
URL_WETEST = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "api.txt"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
session = requests.Session()
session.headers.update(headers)

# -----------------------------
# 抓取 ip.164746.xyz（最多取3个）
# -----------------------------
resp_164746 = session.get(URL_164746, timeout=10)
resp_164746.encoding = resp_164746.apparent_encoding
soup = BeautifulSoup(resp_164746.text, "html.parser")

data_164746 = []
for row in soup.select("table tr")[1:]:
    cols = row.find_all("td")
    if len(cols) < 5:
        continue
    ip = cols[0].text.strip().lstrip("★").strip()
    if not ip:
        continue
    try:
        latency = float(cols[4].text.strip())
        data_164746.append((ip, latency))
    except:
        continue

top_164746 = [ip for ip, _ in sorted(data_164746, key=lambda x: x[1])[:3]]

# -----------------------------
# 抓取 wetest.vip（最多取3个）
# -----------------------------
resp_wetest = session.get(URL_WETEST, timeout=10)
resp_wetest.encoding = resp_wetest.apparent_encoding

pattern_wetest = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
data_wetest = [(ip, int(lat)) for ip, lat in pattern_wetest.findall(resp_wetest.text)]
top_wetest_sorted = [ip for ip, _ in sorted(data_wetest, key=lambda x: x[1])]

# -----------------------------
# 合并逻辑，总数6
# -----------------------------
final_ips = top_164746.copy()

needed = 6 - len(final_ips)
for ip in top_wetest_sorted:
    if ip not in final_ips and needed > 0:
        final_ips.append(ip)
        needed -= 1

# -----------------------------
# 写入文件
# -----------------------------
with open(OUTPUT, "w", encoding="utf-8") as f:
    for ip in final_ips:
        f.write(f"{ip}#官方优选\n")

print("成功生成 IP 列表：")
for i, ip in enumerate(final_ips, start=1):
    print(f"{i}. {ip}#官方优选")
