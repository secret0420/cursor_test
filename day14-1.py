import os
import time
from datetime import datetime, timedelta

def main():
    # 1. 确定备份目录
    # os.path.abspath(__file__) 获取当前脚本的绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(base_dir, 'backup')
    
    # 如果目录不存在则创建
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    print(f"开始模拟备份，目录: {backup_dir}")
    print("按 Ctrl+C 停止并清理...")
    
    try:
        while True:
            # 2. 获取当前时间并生成备份文件
            now = datetime.now()
            now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"backup_{now_str}.txt"
            filepath = os.path.join(backup_dir, filename)
            
            # 使用 with open 写入文件（模拟备份过程）
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Device configuration backup at {now_str}")
            
            print(f"\n[+] 创建备份: {filename}")
            
            # 3. 计算 15 秒前的时间基准
            expire_time = now - timedelta(seconds=15)
            
            # 4. 遍历备份目录，找出过期文件并删除
            current_files = []
            for file in os.listdir(backup_dir):
                if file.startswith('backup_') and file.endswith('.txt'):
                    # 从文件名提取时间字符串
                    time_str = file.replace('backup_', '').replace('.txt', '')
                    # 将字符串转换回 datetime 对象进行比较
                    try:
                        file_time = datetime.strptime(time_str, '%Y-%m-%d_%H-%M-%S')
                        
                        # 比较时间，如果过期则删除
                        if file_time < expire_time:
                            os.remove(os.path.join(backup_dir, file))
                            print(f"[-] 删除过期: {file}")
                        else:
                            current_files.append(file)
                    except ValueError:
                        # 忽略格式不正确的文件
                        continue
            
            # 5. 打印当前保留的所有备份文件
            print(f"[*] 当前保留的备份 ({len(current_files)}个):")
            # 排序打印，让输出更整齐
            for f in sorted(current_files):
                print(f"    - {f}")
                
            # 6. 休眠 3 秒
            time.sleep(3)
            
    except KeyboardInterrupt:
        # 7. 捕获 Ctrl+C，进行收尾工作
        print("\n\n收到停止信号，正在清理所有备份文件...")
        
        # 再次遍历目录清理剩余文件
        if os.path.exists(backup_dir):
            for file in os.listdir(backup_dir):
                file_path = os.path.join(backup_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"[-] 已清理: {file}")
            
            # 最后删除目录本身
            os.rmdir(backup_dir)
            print("[-] 已删除 backup 目录")
            
        print("清理完成，程序退出。")

if __name__ == '__main__':
    main()