import requests
import re

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "ips.txt"

# 请求网页
resp = requests.get(URL, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
resp.encoding = resp.apparent_encoding
text = resp.text

# 正则匹配 IP + 电信延迟(节点)，跨行匹配
pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
matches = pattern.findall(text)

# 转为整数，排序取前6
data = [(ip, int(latency)) for ip, latency in matches]
top6 = sorted(data, key=lambda x: x[1])[:6]

# 写入 ips.txt，备注 CT
with open(OUTPUT, "w") as f:
    for ip, _ in top6:
        f.write(f"{ip}#CT\n")

# 打印前6条供验证
for ip, latency in top6:
    print(f"{ip} - {latency}ms")

print(f"✅ 已写入前6个电信延迟 IP 到 {OUTPUT}")
