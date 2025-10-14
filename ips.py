import requests
import re

URL_WETEST = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "api.txt"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
session = requests.Session()
session.headers.update(headers)

all_data = []

# -----------------------------
# 抓取 wetest.vip（电信节点）
# -----------------------------
resp = session.get(URL_WETEST, timeout=10)
resp.encoding = resp.apparent_encoding

# 匹配格式：IP + “电信” + 延迟数字 + “毫秒”
pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
for ip, lat in pattern.findall(resp.text):
    all_data.append((ip, int(lat)))

# -----------------------------
# 按延迟排序，取前8个
# -----------------------------
top_ips = [ip for ip, _ in sorted(all_data, key=lambda x: x[1])[:8]]

# -----------------------------
# 写入文件，备注为 #CT
# -----------------------------
with open(OUTPUT, "w", encoding="utf-8") as f:
    for ip in top_ips:
        f.write(f"{ip}#CT\n")

print("成功生成 IP 列表：")
for i, ip in enumerate(top_ips, start=1):
    print(f"{i}. {ip}#CT")
