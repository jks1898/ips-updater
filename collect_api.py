import requests
from bs4 import BeautifulSoup
import re

URL_164746 = "https://ip.164746.xyz/"
URL_WETEST = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "api.txt"

special_ip = "cf.090227.xyz#官方优选"

# -----------------------------
# 1. 获取 ip.164746.xyz 的 IP 并按平均延迟排序
# -----------------------------
resp_164746 = requests.get(URL_164746, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
resp_164746.encoding = resp_164746.apparent_encoding
soup = BeautifulSoup(resp_164746.text, "html.parser")

data_164746 = []
for row in soup.select("table tr")[1:]:  # 跳过表头
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

top4_164746 = sorted(data_164746, key=lambda x: x[1])[:4]
top4_list = [f"{ip}#官方优选" for ip, _ in top4_164746]

# -----------------------------
# 2. 获取 wetest.vip 的 IP 并按电信延迟排序
# -----------------------------
resp_wetest = requests.get(URL_WETEST, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
resp_wetest.encoding = resp_wetest.apparent_encoding
pattern_wetest = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
matches_wetest = pattern_wetest.findall(resp_wetest.text)
data_wetest = [(ip, int(latency)) for ip, latency in matches_wetest]

top_wetest_filtered = [f"{ip}#官方优选" for ip, _ in sorted(data_wetest, key=lambda x: x[1])
                       if ip not in [ip for ip, _ in top4_164746]]
top5_wetest = top_wetest_filtered[:5]

# -----------------------------
# 3. 合并前9 + 特殊 IP
# -----------------------------
final_list = top4_list + top5_wetest + [special_ip]

# -----------------------------
# 4. 写入文件
# -----------------------------
with open(OUTPUT, "w") as f:
    for line in final_list:
        f.write(line + "\n")

print("成功生成 IP 列表：")
for line in final_list:
    print(line)
