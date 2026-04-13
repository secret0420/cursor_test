import re

# 1. 原始 ASA 连接字符串 (使用 \n 分隔多行)
asa_conn = "TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO\nTCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"

conn_dict = {}

# 2. 按行遍历并使用正则提取
# 正则解释：匹配 协议、源IP、源端口、目的IP、目的端口、字节数、标志位
pattern = r'(\w+)\s+\w+\s+([\d\.]+):(\d+)\s+\w+\s+([\d\.]+):(\d+),.*bytes\s+(\d+),\s+flags\s+(\w+)'

for line in asa_conn.split('\n'):
    match = re.search(pattern, line)
    if match:
        # 提取各个字段
        protocol, src_ip, src_port, dst_ip, dst_port, byte_count, flags = match.groups()
        
        # 按照作业要求构建字典：键为元组 (src, src_p, dst, dst_p)，值为元组 (bytes, flags)
        key = (src_ip, src_port, dst_ip, dst_port)
        value = (byte_count, flags)
        conn_dict[key] = value

# 3. 打印分析后的字典结果
print(conn_dict)
print("\n" + "="*84)

# 4. 格式化打印输出
for (sip, sport, dip, dport), (byt, flg) in conn_dict.items():
    # 使用 format 进行对齐
    row1 = "src       : {:<15} | src_port  : {:<6} | dst       : {:<14} | dst_port  : {:<6}".format(sip, sport, dip, dport)
    row2 = "bytes     : {:<15} | flags     : {:<6}".format(byt, flg)
    print(row1)
    print(row2)
    print("=" * 84)




    import re

port_list = ['eth 1/101/1/42','eth 1/101/1/26','eth 1/101/1/23','eth 1/101/1/7','eth 1/101/2/46','eth 1/101/1/34','eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32','eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

# 一句话排序方案：
# 逻辑：将接口名按 '/' 和 ' ' 分割，跳过第一个 'eth'，将剩下的编号转为整数进行比较
port_list.sort(key=lambda x: [int(i) for i in re.split(r'[/ ]', x)[1:]])

print(port_list)