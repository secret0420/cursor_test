import hashlib
import time
import re
import sys
import os

# 1. 导入第九天的 SSH 函数
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from day9 import ssh_exec_command as ssh_run

def get_config(host, user, passwd):
    """
    函数一：获取设备配置并截取有效部分
    """
    command = "show running-config"
    # 执行命令获取原始输出
    raw_output = ssh_run(host, user, passwd, command)
    
    # 使用正则表达式截取从 hostname 开始到 end 结束的部分
    # [\s\S]+ 表示匹配包括换行符在内的任意字符
    match = re.search(r'(hostname[\s\S]+end)', raw_output)
    
    if match:
        return match.group(1).strip()
    else:
        return ""

def monitor_config(host, user, passwd):
    """
    函数二：监控配置变化
    """
    last_md5 = ""
    print(f"[*] 开始监控设备 {host} 的配置变化...")

    while True:
        # 1. 获取当前配置
        config_str = get_config(host, user, passwd)
        
        if not config_str:
            print("[!] 错误：无法获取配置或未找到有效起始标记")
            time.sleep(5)
            continue

        # 2. 计算 MD5 值
        # 注意：hashlib.md5() 必须接收 bytes 类型数据
        current_md5 = hashlib.md5(config_str.encode()).hexdigest()

        # 3. 逻辑比对
        if last_md5 == "":
            # 第一次运行，记录初始 MD5
            last_md5 = current_md5
            print(f"[*] 初始配置 MD5: {last_md5}")
        elif current_md5 == last_md5:
            # 配置未变
            print(f"[*] 当前配置 MD5: {current_md5}")
        else:
            # 配置发生变化
            print(f"[!] 告警: 配置已改变！新 MD5: {current_md5}")
            # 发现变化后退出程序
            break
        
        # 4. 每 5 秒轮询一次
        time.sleep(5)

if __name__ == '__main__':
    # --- 设备配置信息 ---
    DEVICE_IP = '10.10.1.1'
    USERNAME = 'admin'
    PASSWORD = 'Cisc0123'
    
    try:
        monitor_config(DEVICE_IP, USERNAME, PASSWORD)
    except KeyboardInterrupt:
        print("\n[*] 监控已由用户停止")