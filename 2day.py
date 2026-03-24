
date = "2026-03-03"
hostname = "SW-Core-01"
level = "CRITICAL"
message = "%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"

print(f"{date} {hostname} {level} {message}")



interface = "GigabitEthernet0/0/1"

if_type = interface[0:15]

if_number = interface[15:]

print(f"接口类型: {if_type}")
print(f"接口编号: {if_number}")



version_raw = "  Cisco IOS XE Software, Version 17.03.04  "

version_stripped = version_raw.strip()

version_upper = version_stripped.upper()

version_replaced = version_stripped.replace("17.03.04", "17.06.01")

print(f"去掉空格: {version_stripped}")
print(f"转大写:   {version_upper}")
print(f"替换版本: {version_replaced}")




intf1, status1, speed1 = "Gi0/0", "up", "1G"
intf2, status2, speed2 = "Gi0/1", "down", "1G"
intf3, status3, speed3 = "Gi0/2", "up", "10G"

template = "{:<10} {:<8} {:<5}"

print(template.format("接口", "状态", "速率"))
print("-" * 30)

print(template.format(intf1, status1, speed1))
print(template.format(intf2, status2, speed2))
print(template.format(intf3, status3, speed3))