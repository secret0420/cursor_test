import os
import time
from pythonping import ping

# --- 1. 定义可以被别人调用的函数 (放在外面) ---
def ping_check(host):
    try:
        # 1. 将 count 增加到 2，给 ARP 解析预留时间
        # 2. 明确使用 verbose=False 减少干扰
        result = ping(host, count=2, timeout=2)
        
        # 打印一下结果，看看具体收到了什么
        # print(f"DEBUG: {host} stats: {result}") 
        
        return result.success(), result.rtt_avg_ms
    except Exception as e:
        # 核心调试：如果报错了，把错误打印出来
        print(f"[!] Ping 内部错误 ({host}): {e}")
        return False, 0
# --- 2. 只有直接运行本文件时才执行的代码 (放在 if 里面) ---
if __name__ == "__main__":
    target_proto = "tcp"
    target_port = ":22 "  # 你这里改成了 22 端口

    print("[*] 开始监测任务...")

    while True:
        ss_result = os.popen('ss -tulnp').read()
        lines = ss_result.split('\n')
        
        is_open = False
        for line in lines:
            if target_proto in line.lower() and target_port in line:
                is_open = True
                break
                
        if is_open:
            # 修正了打印信息，使其与 target_port 匹配
            print(f"[!] 告警: TCP/22 已开放！请检查是否为授权服务。")
            break
        else:
            print("[*] 检测中... TCP/22 未监听")
        
        time.sleep(1)