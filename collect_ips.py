import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "ips.txt"

# 请求网页
resp = requests.get(URL, timeout=10)
resp.encoding = resp.apparent_encoding
soup = BeautifulSoup(resp.text, "html.parser")
text = soup.get_text()

# 1️⃣ 提取所有 IP
ip_pattern = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
all_ips = ip_pattern.findall(text)

# 2️⃣ 提取电信延迟(节点)列：IP + 延迟毫秒
latency_pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
matches = latency_pattern.findall(text)

# 生成 (IP, 延迟) 对，只保留在 all_ips 中的 IP
data = [(ip, int(latency)) for ip, latency in matches if ip in all_ips]

# 按延迟升序排序，取前 6 个
top6 = sorted(data, key=lambda x: x[1])[:6]

# 写入 ips.txt，备注 CT
with open(OUTPUT, "w") as f:
    for ip, _ in top6:
        f.write(f"{ip}#CT\n")

print(f"✅ 已写入前6个电信延迟 IP 到 {OUTPUT}")
