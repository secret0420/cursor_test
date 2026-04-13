import os
import shutil


files = {
    'R1_config.txt': 'hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R2_config.txt': 'hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R3_config.txt': 'hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'SW1_config.txt': 'hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
}


dir_name = 'backup'

os.makedirs(dir_name, exist_ok=True)

for filename, content in files.items():
    file_path = os.path.join(dir_name, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("发现包含 shutdown 接口的设备配置文件:")


for filename in os.listdir(dir_name):
    file_path = os.path.join(dir_name, filename)
    
    with open(file_path, 'r', encoding='utf-8') as f:
      
        lines = f.readlines()
        
       
        for line in lines:
            
            if 'shutdown' in line and 'no shutdown' not in line:
                print(filename)
                break

shutil.rmtree(dir_name)
print(f"{dir_name}/ 目录已清理")