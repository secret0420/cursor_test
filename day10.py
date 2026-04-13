import sys
import os

# 1. 将当前目录加入系统路径，确保能找到 day8 和 day9
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 2. 从之前的作业中导入函数
from day8 import ping_check
from day9 import ssh_exec_command as ssh_run # 将函数重命名为 ssh_run 方便使用

def network_audit(ip_list, user, passwd):
    """
    自动化巡检函数：先探测后采集
    """
    show_command = "show ip interface brief"
    
    for ip in ip_list:
        # 第一步：调用 day8 的函数探测可达性
        # ping_check 返回 (is_up, rtt)
        is_up, rtt = ping_check(ip)
        
        if is_up:
            print(f"[*] {ip} 可达 (RTT: {rtt:.2f} ms)，正在采集...")
            
            # 第二步：调用 day9 的函数执行 SSH 命令
            try:
                output = ssh_run(ip, user, passwd, show_command)
                print(f"---------- {ip} 接口信息 ----------")
                print(output)
                print("-" * 40)
            except Exception as e:
                print(f"[!] {ip} SSH 连接失败: {e}")
        else:
            print(f"[x] {ip} 不可达，跳过，不采集。")

if __name__ == '__main__':
    # --- 待测试设备列表 ---
    devices = ['10.10.1.1', '10.10.1.2', '10.10.1.3']
    
    # --- 登录凭据 ---
    username = 'admin'
    password = 'Cisc0123'
    
    network_audit(devices, username, password)