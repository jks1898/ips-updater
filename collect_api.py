import requests
import re

URL = "https://www.wetest.vip/page/cloudflare/total_v4.html"
OUTPUT = "api.txt"

# 前三固定优选
fixed_top3 = [
    "47.239.8.172#官方优选",
    "101.32.12.79#官方优选",
    "8.218.189.27#官方优选"
]

# cf.090227.xyz 放第10
special_ip = "cf.090227.xyz#官方优选"

# 请求网页
resp = requests.get(URL, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
resp.encoding = resp.apparent_encoding
text = resp.text

# 匹配 IP + 电信延迟
pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}).*?电信.*?(\d+)\s*毫秒", re.S)
matches = pattern.findall(text)

# 转为整数并排序取前6
data = [(ip, int(latency)) for ip, latency in matches]
top6 = sorted(data, key=lambda x: x[1])[:6]

# 过滤掉前三固定优选中的 IP
top6_filtered = [f"{ip}#官方优选" for ip, _ in top6 if ip not in [f.split('#')[0] for f in fixed_top3]]

# 构建最终列表
final_list = fixed_top3.copy()                  # 第1~3位固定优选
final_list += top6_filtered[:6]                # 第4~9位延迟优选
final_list.append(special_ip)                 # 第10位特殊固定 IP

# 写入文件
with open(OUTPUT, "w") as f:
    for line in final_list:
        f.write(line + "\n")
