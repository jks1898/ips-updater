import requests

API_URL = "https://cfcdn.api.urlce.com/total_v4.json"
OUTPUT_FILE = "ips.txt"

# 发送 GET 请求获取 JSON 数据
response = requests.get(API_URL)
response.raise_for_status()  # 如果请求失败，抛出异常

# 解析 JSON 数据
data = response.json()

# 筛选电信延迟数据并排序
filtered_data = [
    (item["ip"], item["latency"])
    for item in data
    if item["isp"] == "电信" and item["latency"] is not None
]
sorted_data = sorted(filtered_data, key=lambda x: x[1])

# 获取前 6 个 IP
top_6_ips = sorted_data[:6]

# 写入文件
with open(OUTPUT_FILE, "w") as file:
    for ip, _ in top_6_ips:
        file.write(f"{ip}#CT\n")

print(f"✅ 已成功获取并写入前 6 个电信延迟 IP 到 {OUTPUT_FILE}")
