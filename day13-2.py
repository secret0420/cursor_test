import sys
import os

# 1. 导入第十二天的 SSH 函数 (确保路径正确)
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
            f"接口名称    : {self.name}",
            f"所属设备    : {device_ip}",
            f"IP 地址     : {self.ip_address} {self.mask}",
            f"描述        : {self.description}",
            f"状态        : {status_str}",
        ]
        return '\n'.join(lines)

class NetworkDevice:
    """网络设备类，保存设备登录信息及关联的接口"""
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.interfaces = []

    def add_interface(self, interface):
        """将接口加入本设备，并建立双向关联"""
        interface.device = self        # 补全：把 interface 的 device 属性指向自己
        self.interfaces.append(interface) # 补全：把 interface 追加到列表

    def apply(self):
        """将所有关联接口的配置一次性下发到设备"""
        if not self.interfaces:
            print(f"[*] {self.ip} 没有待下发的接口配置")
            return

        cmds = ['config ter']
        for iface in self.interfaces:
            # 补全命令拼接逻辑
            cmds.append(f'interface {iface.name}')
            cmds.append(f'ip address {iface.ip_address} {iface.mask}')
            
            # 如果有描述内容则下发
            if iface.description:
                cmds.append(f'description {iface.description}')
            
            # 根据 status 决定下发 no shutdown 还是 shutdown
            cmds.append('no shutdown' if iface.status else 'shutdown')
            
        cmds.append('end')

        iface_names = ', '.join(iface.name for iface in self.interfaces)
        print(f"[*] 正在 {self.ip} 上批量应用接口配置: {iface_names}")
        
        # 调用第 12 天的函数进行 SSH 下发
        qytang_multicmd(self.ip, self.username, self.password, cmds, verbose=False)
        print(f"[*] {self.ip} 所有接口配置应用完成！")

    def __str__(self):
        """打印设备信息及下属接口列表"""
        lines = [
            f"设备 IP      : {self.ip}",
            f"用户名       : {self.username}",
            "接口列表     :",
        ]
        if not self.interfaces:
            lines.append("  （无）")
        else:
            for iface in self.interfaces:
                status_str = 'no shutdown' if iface.status else 'shutdown'
                lines.append(f"  - {iface.name}: {iface.ip_address} {iface.mask}, {status_str}")
        return '\n'.join(lines)

# --- 集成测试 ---
if __name__ == '__main__':
    # 1. 初始化设备
    r1 = NetworkDevice('10.10.1.1', 'admin', 'Cisc0123')

    # 2. 初始化接口 1
    gi1 = Interface('GigabitEthernet1')
    gi1.ip_address = '192.168.1.1'
    gi1.mask = '255.255.255.0'
    gi1.description = 'Connect_to_LAN'
    gi1.status = True

    # 3. 初始化接口 2
    gi2 = Interface('GigabitEthernet2')
    gi2.ip_address = '10.1.1.1'
    gi2.mask = '255.255.255.252'
    gi2.status = False  # 明确关闭

    # 4. 组合：将接口加入设备
    r1.add_interface(gi1)
    r1.add_interface(gi2)

    # 5. 查看打印结果
    print("--- 当前设备规划信息 ---")
    print(r1)
    print("-" * 30)

    # 6. 下发配置 (请确保 10.10.1.1 可达)
    # r1.apply()