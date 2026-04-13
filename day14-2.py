import argparse
import paramiko
import sys

def ssh_run(host, username, password, command):
    """通过 paramiko 执行 SSH 命令并返回结果"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 建立连接
        ssh.connect(
            host, 
            port=22, 
            username=username, 
            password=password, 
            timeout=5,
            look_for_keys=False, 
            allow_agent=False
        )
        
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        error = stderr.read().decode()
        
        ssh.close()
        
        # 如果有错误输出，返回错误信息
        if error:
            return f"命令执行错误:\n{error}"
        return result

    except Exception as e:
        return f"SSH 连接失败: {e}"

def main():
    # 1. 创建解析器对象
    parser = argparse.ArgumentParser(description='网络设备 SSH 命令执行工具')
    
    # 2. 添加命令行参数
    # required=True 表示该参数必须提供
    # help 是当输入 -h 时显示的说明文字
    parser.add_argument('-i', '--ip', required=True, help='设备的 IP 地址')
    parser.add_argument('-u', '--username', required=True, help='登录用户名')
    parser.add_argument('-p', '--password', required=True, help='登录密码')
    parser.add_argument('-c', '--cmd', required=True, help='要执行的命令')
    
    # 3. 解析终端输入的参数
    args = parser.parse_args()
    
    # 4. 调用函数，从 args 对象中获取解析后的值
    print(f"\n[*] 正在尝试连接 {args.ip} ...\n")
    
    output = ssh_run(args.ip, args.username, args.password, args.cmd)
    
    # 5. 打印执行结果
    print(output)

if __name__ == '__main__':
    main()

