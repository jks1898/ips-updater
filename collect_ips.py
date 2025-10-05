import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "ips.txt"

# 请求网页
resp = requests.get(URL, timeout=10)
resp.encoding = resp.apparent_encoding
soup = BeautifulSoup(resp.text, "html.parser")

# 正则匹配电信延迟
# 匹配形式：IP ... 电信 ... 数字毫秒
pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+).*?电信.*?(\d+)毫秒")
data = [(m.group(1), int(m.group(2))) for m in pattern.finditer(soup.get_text())]

# 按电信延迟升序排序，取前6个
top6 = sorted(data, key=lambda x: x[1])[:6]

# 写入 ips.txt，备注 CT
with open(OUTPUT, "w") as f:
    for ip, _ in top6:
        f.write(f"{ip}#CT\n")

print(f"✅ 已写入前6个电信延迟 IP 到 {OUTPUT}")
