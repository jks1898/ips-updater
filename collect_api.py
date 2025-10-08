import requests
from bs4 import BeautifulSoup
import re

# -----------------------------
# 固定参数
# -----------------------------
URL_164746 = "https://ip.164746.xyz/"
URL_WETEST = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "api.txt"

fixed_ips = [
    "47.239.8.172#官方优选",
    "103.115.64.38#官方优选",
    "101.32.12.79#官方优选",
    "8.218.189.27#官方优选",
    "101.32.179.58#官方优选",
]
special_ip = "cf.090227.xyz#官方优选"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
session = requests.Session()
session.headers.update(headers)

# -----------------------------
# 抓取 wetest.vip (第6~8)
# -----------------------------
resp_wetest = session.get(URL_WETEST, timeout=10)
resp_wetest.encoding = resp_wetest.apparent_encoding
pattern_wetest = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
data_wetest = [(ip, int(lat)) for ip, lat in pattern_wetest.findall(resp_wetest.text)]
top3_wetest = [f"{ip}#官方优选" for ip, _ in sorted(data_wetest, key=lambda x: x[1])[:3]]

# -----------------------------
# 抓取 ip.164746.xyz (第9~10)
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

top2_164746 = sorted(data_164746, key=lambda x: x[1])[:2]
top2_list = [f"{ip}#官方优选" for ip, _ in top2_164746]

# 若只抓到1个，则补上 special_ip
if len(top2_list) == 1:
    top2_list.append(special_ip)
elif len(top2_list) == 0:
    top2_list = [special_ip]

# -----------------------------
# 合并
# -----------------------------
final_list = fixed_ips + top3_wetest + top2_list

# -----------------------------
# 写入文件
# -----------------------------
with open(OUTPUT, "w", encoding="utf-8") as f:
    for line in final_list:
        f.write(line + "\n")

print("成功生成 IP 列表：")
for line in final_list:
    print(line)
