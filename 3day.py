import re

mac_table = '166    54a2.74f7.0326    DYNAMIC     Gi1/0/11'

pattern = r'(\d+)\s+([\w\.]+)\s+(\w+)\s+(\S+)'
result = re.match(pattern, mac_table)

if result:
    vlan = result.group(1)
    mac = result.group(2)
    m_type = result.group(3)
    interface = result.group(4)

    print("{:<10}: {}".format("Vlan", vlan))
    print("{:<10}: {}".format("Mac", mac))
    print("{:<10}: {}".format("Type", m_type))
    print("{:<10}: {}".format("Interface", interface))
else:
    print("No match found")
#task2
import re

conn = 'TCP server  172.16.1.101:443 localserver  172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

pattern = fr'(\w+)\s+server\s+([\d\.]+):(\d+)\s+localserver\s+([\d\.]+):(\d+)'

result = re.search(pattern, conn)

if result:
    protocol = result.group(1)
    server_ip = result.group(2)
    server_port = result.group(3)
    local_ip = result.group(4)
    local_port = result.group(5)
    
    print("{:<10}: {}".format("Protocol", protocol))
    print("{:<10}: {}".format("Server IP", server_ip))
    print("{:<10}: {}".format("Server Port", server_port))
    print("{:<10}: {}".format("Local IP", local_ip))
    print("{:<10}: {}".format("Local Port", local_port))
else:
    print("No match found")



    