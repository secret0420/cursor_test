import os
import re
result = os.popen("ifconfig ens192").read()

print(result)

# --- 正则表达式提取 ---
# 提取 IP: inet 后面跟着的数字点分组合
ip = re.search(r'inet\s+([\d\.]+)', result).group(1)
# 提取 Netmask: netmask 后面跟着的数字点分组合
netmask = re.search(r'netmask\s+([\d\.]+)', result).group(1)
# 提取 Broadcast: broadcast 后面跟着的数字点分组合
broadcast = re.search(r'broadcast\s+([\d\.]+)', result).group(1)
# 提取 MAC: ether 后面跟着的 17 位十六进制字符组合
mac = re.search(r'ether\s+([0-9a-f:]{17})', result).group(1)

# --- 打印提取结果 ---
print("{:<12}: {}".format("IP", ip))
print("{:<12}: {}".format("Netmask", netmask))
print("{:<12}: {}".format("Broadcast", broadcast))
print("{:<12}: {}".format("MAC", mac))
print("-" * 35)

# 第二步：生成网关地址并进行 Ping 测试
# 1. 将 IP 字符串按 '.' 分割成列表，取前三段，最后拼接 '.1'
ip_parts = ip.split('.')
gateway_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"

print(f"假设网关为: {gateway_ip}")
print(f"Ping {gateway_ip} ...", end=" ", flush=True)

# 2. 执行 Linux 的 ping 命令 (-c 1 表示发送 1 个包，-W 2 表示超时时间 2 秒)
# 为了演示，我们使用实际生成的网关执行
ping_cmd = os.popen(f"ping -c 1 -W 2 {gateway_ip}").read()

# 3. 判断 Ping 结果
if "1 received" in ping_cmd:
    print("reachable")
else:
    print("unreachable (Timeout or No route)")