import requests
import re

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "api.txt"

# 固定优选（调整顺序，删除 cf.877774.xyz）
fixed_ips = [
    "101.32.12.79#官方优选",
    "8.218.189.27#官方优选",
    "cf.090227.xyz#官方优选"
]

# 请求网页
resp = requests.get(URL, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
resp.encoding = resp.apparent_encoding
text = resp.text

# 正则匹配 IP + 电信延迟(节点)
pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
matches = pattern.findall(text)

# 转为整数，排序取前6
data = [(ip, int(latency)) for ip, latency in matches]
top6 = sorted(data, key=lambda x: x[1])[:6]

# 构建最终列表：先放 top6，再把固定优选放到最后
final_list = [f"{ip}#官方优选" for ip, _ in top6] + fixed_ips

# 写入文件
with open(OUTPUT, "w") as f:
    for line in final_list:
        f.write(line + "\n")
