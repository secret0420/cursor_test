import paramiko
import re

def ssh_exec_command(host, username, password, command):
        """
        封装 SSH 执行命令函数
        返回: 命令输出的字符串内容
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                hostname=host,
                port=22,
                username=username,
                password=password,
                timeout=5,
                look_for_keys=False,
                allow_agent=False
            )

            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()

            ssh.close()
            return output

        except Exception as e:
            return f"SSH 连接失败: {e}"

if __name__ == '__main__':
        host_ip = '192.168.83.240'
        user = 'root'
        passwd = 'Cisc0123!'
        cmd = 'route -n'

        route_output = ssh_exec_command(host_ip, user, passwd, cmd)
        gateway = "未找到"
        pattern = r'^0\.0\.0\.0\s+([\d\.]+)\s+.*UG'

        for line in route_output.split('\n'):
            match = re.search(pattern, line.strip())
            if match:
                gateway = match.group(1)
                break

        print(f"默认网关: {gateway}")
