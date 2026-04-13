import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 创建数据库引擎 (使用本地 SQLite 文件)
engine = create_engine('sqlite:///device_inventory.db?check_same_thread=False', echo=False)

Base = declarative_base()

# 2. 定义 Device 数据库模型类
class Device(Base):
    __tablename__ = 'devices'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(64), nullable=False, index=True)
    type        = Column(String(64), nullable=False)
    version     = Column(String(64))
    location    = Column(String(128))
    # 使用 datetime.datetime.now 不要加括号，表示入库时才调用
    create_time = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f"{self.__class__.__name__}(设备名称: {self.name} | 类型: {self.type} | "
                f"版本: {self.version} | 位置: {self.location} | 入库时间: {self.create_time})")

# 3. 初始化数据库连接会话
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    # A. 创建数据库表
    Base.metadata.create_all(engine, checkfirst=True)

    # B. 只有表为空时才插入初始数据 (Seed Data)
    if session.query(Device).count() == 0:
        device_list = [
            {'name': 'R1', 'type': 'router', 'version': 'IOS XE 17.14', 'location': 'Beijing-IDC-A'},
            {'name': 'R2', 'type': 'router', 'version': 'IOS XE 17.14', 'location': 'Shanghai-IDC-B'},
            {'name': 'SW1', 'type': 'switch', 'version': 'IOS 15.2', 'location': 'Beijing-IDC-A'},
            {'name': 'SW2', 'type': 'switch', 'version': 'IOS 15.2', 'location': 'Shanghai-IDC-B'},
            {'name': 'FW1', 'type': 'firewall', 'version': 'ASA 9.16', 'location': 'Beijing-IDC-A'},
            {'name': 'FW2', 'type': 'firewall', 'version': 'FTD 7.2', 'location': 'Shenzhen-IDC-C'},
        ]
        for dev_data in device_list:
            session.add(Device(**dev_data))
        session.commit()
        print("[+] 初始设备数据已写入数据库")

    # C. 交互式查询菜单
    while True:
        print("\n请输入查询选项:")
        print("输入 1：查询所有设备")
        print("输入 2：根据设备名称查询")
        print("输入 3：根据设备类型查询")
        print("输入 4：根据机房位置查询")
        print("输入 0：退出")

        choice = input("\n请输入查询选项：").strip()
        
        if choice not in ('0', '1', '2', '3', '4'):
            print("无效的选项，请重新输入（0-4）")
            continue

        if choice == '1':
            # 查询全部设备
            results = session.query(Device).all()
            for dev in results:
                print(dev)

        elif choice == '2':
            name_input = input("请输入设备名称：").strip()
            # 精确查询
            results = session.query(Device).filter(Device.name == name_input).all()
            if not results:
                print("未找到该名称的设备")
            for dev in results:
                print(dev)

        elif choice == '3':
            type_input = input("请输入设备类型（router/switch/firewall）：").strip()
            # 过滤查询
            results = session.query(Device).filter(Device.type == type_input).all()
            for dev in results:
                print(dev)

        elif choice == '4':
            keyword = input("请输入机房位置关键词：").strip()
            # 模糊查询，使用 contains
            results = session.query(Device).filter(Device.location.contains(keyword)).all()
            for dev in results:
                print(dev)

        elif choice == '0':
            print("退出系统...")
            break