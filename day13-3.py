import sys
import os

# 1. 导入第十二天的 SSH 函数
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from day12 import qytang_multicmd

class Interface:
    """接口配置类，只保存接口数据"""
    def __init__(self, name):
        self.name = name
        self.device = None
        self.ip_address = ''
        self.mask = ''
        self.description = ''
        self.status = False

    def __str__(self):
        status_str = 'no shutdown' if self.status else 'shutdown'
        device_ip = self.device.ip if self.device else '未绑定设备'
        lines = [
            f"  - {self.name}: {self.ip_address} {self.mask}, {status_str}"
        ]
        return lines[0]

class NetworkDevice:
    """网络设备类"""
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.interfaces = []

    def add_interface(self, interface):
        """双向绑定接口"""
        interface.device = self
        self.interfaces.append(interface)

    def apply(self):
        """批量下发配置"""
        if not self.interfaces:
            print(f"[*] {self.ip} 没有待下发的接口配置")
            return

        # 拼接 Cisco 配置指令
        cmds = ['config ter']
        for iface in self.interfaces:
            cmds.append(f'interface {iface.name}')
            if iface.ip_address:
                cmds.append(f'ip address {iface.ip_address} {iface.mask}')
            if iface.description:
                cmds.append(f'description {iface.description}')
            cmds.append('no shutdown' if iface.status else 'shutdown')
        cmds.append('end')

        iface_names = ', '.join(iface.name for iface in self.interfaces)
        print(f"[*] 正在 {self.ip} 上批量应用接口配置: {iface_names}")
        
        # 调用 SSH 函数执行命令
        qytang_multicmd(self.ip, self.username, self.password, cmds, verbose=False)
        print(f"[*] {self.ip} 所有接口配置应用完成！")

    def __str__(self):
        lines = [
            f"设备 IP      : {self.ip}",
            f"用户名       : {self.username}",
            "接口列表     :",
        ]
        if not self.interfaces:
            lines.append("  （无）")
        else:
            for iface in self.interfaces:
                lines.append(str(iface))
        return '\n'.join(lines)

# --- 主程序测试区域 ---
if __name__ == '__main__':
    # 1. 实例化设备对象 (请确保 IP、账号、密码与你的路由器一致)
    r1 = NetworkDevice('10.10.1.1', 'admin', 'Cisc0123')

    # 2. 创建第一个接口 (Loopback13)
    loop13 = Interface('Loopback13')
    loop13.ip_address = '13.13.13.13'
    loop13.mask = '255.255.255.255'
    loop13.description = 'Created_by_Python'
    loop13.status = True
    r1.add_interface(loop13)

    # 3. 创建第二个接口 (GigabitEthernet2)
    gi2 = Interface('GigabitEthernet2')
    gi2.ip_address = '172.16.1.12'
    gi2.mask = '255.255.255.0'
    gi2.description = 'Created_by_Python'
    gi2.status = True
    r1.add_interface(gi2)

    # 4. 打印预览当前设备规划信息
    print("=" * 40)
    print(r1)
    print("=" * 40)

    # 5. 执行 SSH 连接并一次性下发所有配置
    r1.apply()