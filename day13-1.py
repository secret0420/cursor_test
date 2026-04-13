class Interface:
    """接口配置类，只保存接口数据"""
    def __init__(self, name):
        self.name = name
        self.device = None           # 所属设备，默认未绑定
        self.ip_address = ''         # IP 地址，默认空字符串
        self.mask = ''               # 子网掩码，默认空字符串
        self.description = ''        # 接口描述，默认空字符串
        self.status = False          # True=no shutdown, False=shutdown，默认关闭 (False)

    def __str__(self):
        """格式化打印接口信息"""
        # 如果 self.status 为 True 则为 'no shutdown'，否则为 'shutdown'
        status_str = 'no shutdown' if self.status else 'shutdown'
        
        # 如果 self.device 存在则取 self.device.ip，否则显示 '未绑定设备'
        # 注意：这里假设 NetworkDevice 类有一个属性叫 ip
        device_ip = self.device.ip if self.device else '未绑定设备'
        
        lines = [
            f"接口名称    : {self.name}",
            f"所属设备    : {device_ip}",
            f"IP 地址     : {self.ip_address} {self.mask}",
            f"描述        : {self.description}",
            f"状态        : {status_str}",
        ]
        return '\n'.join(lines)

# --- 测试代码 ---
if __name__ == '__main__':
    # 1. 创建一个接口对象
    gi1 = Interface("GigabitEthernet1")
    
    # 2. 设置属性
    gi1.ip_address = "192.168.1.1"
    gi1.mask = "255.255.255.0"
    gi1.description = "Connect to Core_Switch"
    gi1.status = True # 开启接口
    
    # 3. 打印接口信息（会自动调用 __str__ 方法）
    print(gi1)