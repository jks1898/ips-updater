import requests
import re

URL_164746 = "https://ip.164746.xyz/"
OUTPUT = "164746_test.txt"

resp = requests.get(URL_164746, timeout=10, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
resp.encoding = resp.apparent_encoding
text = resp.text

# 匹配格式：★ 【序号†IP†域名】 ... 平均延迟(ms)
pattern = re.compile(r"★\s*【\d+†(\d{1,3}(?:\.\d{1,3}){3})†.*?】.*?\s\d+\.\d+", re.S)
pattern_latency = re.compile(r"★\s*【\d+†\d{1,3}(?:\.\d{1,3}){3}†.*?】.*?\s\d+\s\d+\s[\d\.]+%\s([\d\.]+)", re.S)

ips = pattern.findall(text)
latencies = pattern_latency.findall(text)

# 转为列表并按延迟排序
data = [(ip, float(latency)) for ip, latency in zip(ips, latencies)]
top4 = sorted(data, key=lambda x: x[1])[:4]

# 输出结果测试
for ip, latency in top4:
    print(ip, latency)
