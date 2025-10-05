# collect_ips.py
OUTPUT_FILE = "ips.txt"

# 固定香港 IP 列表
IP_LIST = [
    "104.16.0.0", "104.16.1.0", "104.18.0.0", "104.18.1.0",
    "162.159.0.0", "162.159.1.0", "172.64.0.0", "172.64.1.0",
    "104.17.0.0", "104.17.1.0", "162.159.2.0", "172.65.0.0"
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for ip in IP_LIST:
        f.write(f"{ip}\tHK\n")

print(f"✅ 已生成 {OUTPUT_FILE}，共 {len(IP_LIST)} 个 IP")
