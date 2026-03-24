
hostname = "C8Kv1"
ip = "192.168.1.1"
vendor = "Cisco"
model = "C8000v"
os_version = "IOS-XE 17.3.4"


print("========== 设备信息 ==========")
print("设备名称: " + hostname)
print("管理地址: " + ip)
print("厂商:     " + vendor)
print("型号:     " + model)
print("系统版本: " + os_version)
print("==============================")




import random


part1 = random.randint(0, 255)
part2 = random.randint(0, 255)
part3 = random.randint(0, 255)
part4 = random.randint(0, 255)


random_ip = str(part1) + "." + str(part2) + "." + str(part3) + "." + str(part4)

print("随机生成的 IP 地址是: " + random_ip)





d1_name = "CoreSwitch"
d1_ip = "10.1.1.1"
d1_role = "核心交换机"


d2_name = "Firewall"
d2_ip = "10.1.1.2"
d2_role = "防火墙"


d3_name = "WLC"
d3_ip = "10.1.1.3"
d3_role = "无线控制器"


print("========== IP地址规划表 ==========")

print("设备名称\t\t管理地址\t\t角色")
print("-" * 41)  

print(d1_name + "\t" + d1_ip + "\t\t" + d1_role)
print(d2_name + "\t" + d2_ip + "\t\t" + d2_role)
print(d3_name + "\t\t" + d3_ip + "\t\t" + d3_role)

print("=========================================")