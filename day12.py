import paramiko
import time

def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    """
    交互式 SSH 执行多条命令函数
    """
    try:
        # 1. 建立 SSH 连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ip, 
            port=22, 
            username=username, 
            password=password,
            timeout=10, 
            look_for_keys=False, 
            allow_agent=False
        )

        # 2. 开启交互式 Shell
        chan = ssh.invoke_shell()
        time.sleep(1)
        # 接收并忽略登录时的初始信息
        chan.recv(4096)

        # 3. 处理 Enable 模式 (如果提供了密码)
        if enable:
            chan.send(b'enable\n')
            time.sleep(1)
            chan.send(enable.encode() + b'\n')
            time.sleep(1)
            chan.recv(4096) # 清空缓冲区

        # 4. 循环执行命令列表
        full_output = ""
        for cmd in cmd_list:
            # 发送命令 (记得加换行符并转码为 bytes)
            chan.send(cmd.encode() + b'\n')
            
            # 等待设备响应
            time.sleep(wait_time)
            
            # 接收返回内容 (指定一个足够大的缓冲区)
            resp = chan.recv(9999).decode(encoding='utf-8', errors='ignore')
            
            # 如果开启了打印模式
            if verbose:
                print(f"--- {cmd} ---")
                print(resp.strip())
                print()
            
            full_output += resp

        # 5. 关闭连接
        ssh.close()
        return full_output

    except Exception as e:
        print(f"连接失败: {e}")
        return None

if __name__ == '__main__':
    # --- 测试配置 ---
    target_ip = '10.10.1.1'
    user = 'admin'
    pwd = 'Cisc0123'
    
    # 待执行命令列表
    cmds = [
        'terminal length 0',
        'show version',
        'config ter',
        'router ospf 1',
        'network 10.0.0.0 0.0.0.255 area 0',
        'end',
        'show ip protocols'
    ]
    
    # 执行函数
    qytang_multicmd(target_ip, user, pwd, cmds, wait_time=2)