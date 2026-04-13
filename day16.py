import sys
import os
import hashlib
import time
import datetime
import re

# ---- 1. 复用第 12 天的 qytang_multicmd ----
# 确保能够找到同级目录下的 day12.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from day12 import qytang_multicmd  # 请确保你的 day12.py 中函数名一致

# ---- 2. SQLAlchemy ORM 配置 ----
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///router_config.db',
                       connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

class RouterConfig(Base):
    """路由器配置备份模型"""
    __tablename__ = 'router_config'
    id            = Column(Integer, primary_key=True)
    router_ip     = Column(String(64),    nullable=False, index=True)
    router_config = Column(String(99999), nullable=False)
    config_hash   = Column(String(500),   nullable=False)
    record_time   = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"路由器IP地址: {self.router_ip} | "
                f"配置Hash: {self.config_hash[:10]}... | "
                f"记录时间: {self.record_time})")

# 创建数据库表
Base.metadata.create_all(engine, checkfirst=True)

# ---- 3. 工具函数 ----
def get_show_run(host, username, password):
    """获取配置并计算 hash"""
    # 1. 采集原始配置
    raw = qytang_multicmd(host, username, password,
                          ['terminal length 0', 'show running-config'],
                          verbose=False)
    
    # 2. 正则提取有效配置段 (排除掉时间戳等会导致干扰的信息)
    match = re.search(r'(hostname[\s\S]+end)', raw)
    if not match:
        return None, None
    
    config = match.group(1).strip()  # 补全：取出配置文本
    
    # 3. 计算 SHA256 哈希值
    # 补全：对配置文本进行编码并计算 SHA256
    config_hash = hashlib.sha256(config.encode('utf-8')).hexdigest()
    
    return config, config_hash

def save_config(host, config, config_hash):
    """写入数据库"""
    with Session() as session:
        # 补全：创建记录对象
        record = RouterConfig(
            router_ip=host, 
            router_config=config, 
            config_hash=config_hash
        )
        session.add(record)
        session.commit()

def get_latest_two_hashes(host):
    """查询最近两条记录"""
    with Session() as session:
        # 补全：按 IP 过滤，按 ID 倒序排列取前两条
        results = (session.query(RouterConfig)
                   .filter(RouterConfig.router_ip == host)
                   .order_by(RouterConfig.id.desc())
                   .limit(2)
                   .all())
        return results

# ---- 4. 主循环 ----
if __name__ == '__main__':
    # 请填入你自己的设备信息
    DEVICE_IP = '10.10.1.1'
    USER = 'admin'
    PWD = 'Cisc0123'

    print(f"[*] 开始监控 {DEVICE_IP} 的配置变化，每 5 秒采集一次...\n")
    
    try:
        while True:
            # 采集并计算
            config_text, current_hash = get_show_run(DEVICE_IP, USER, PWD)
            
            if config_text:
                # 存入数据库
                save_config(DEVICE_IP, config_text, current_hash)
                
                # 获取最近两条记录进行对比
                records = get_latest_two_hashes(DEVICE_IP)

                if len(records) < 2:
                    # 第一次运行
                    print(f"本次采集的HASH:{current_hash}")
                elif records[0].config_hash == records[1].config_hash:
                    # 补全：无变化逻辑
                    print(f"本次采集的HASH:{current_hash}")
                else:
                    # 补全：发生变化逻辑
                    print("==========配置发生变化==========")
                    print(f"  THE MOST RECENT HASH  {records[0].config_hash}")
                    print(f"  THE LAST HASH         {records[1].config_hash}")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[*] 监控已停止。")