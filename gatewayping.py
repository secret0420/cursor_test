from pythonping import ping

def ping_check(host):
    """
    封装 Ping 检查函数
    参数: host (IP地址字符串)
    返回: (布尔值-是否可达, 浮点数-平均RTT)
    """
    try:
        result = ping(host, count=1, timeout=2)
        return result.success(), result.rtt_avg_ms
    except Exception:
        return False, 0

if __name__ == '__main__':
    gateways = ['192.168.83.1', '10.0.0.1', '172.16.1.1']
    
    print("-" * 40)
    for gw in gateways:
        is_up, rtt = ping_check(gw)

        if is_up:
            status = "可达"
            print("{:<12} : {:<6} | RTT: {:.2f} ms".format(gw, status, rtt))
        else:
            status = "不可达"
            print("{:<12} : {:<6}".format(gw, status))
    print("-" * 40)