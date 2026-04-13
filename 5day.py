import os
import re

route_n_result = os.popen("route -n").read()

print(route_n_result)



pattern = r'^0\.0\.0\.0\s+([\d\.]+)\s+[\d\.]+\s+UG'

# 3. 在多行文本中进行搜索
result = re.search(pattern, route_n_result, re.MULTILINE)

# 4. 打印输出
if result:
    gateway = result.group(1)
    print(f"网关为: {gateway}")
else:
    print("未找到默认网关信息。")




# 第二部分：列表引用与拷贝对比
l1 = [100, 1000, 10, 400, 25, 40, 0]

# --- 实验：使用拷贝 (copy) ---
# 如果使用 l2 = l1，排序 l2 会导致 l1 也跟着变
# 使用 .copy() 会创建一个全新的列表对象，互不干扰
l2 = l1.copy() 
l2.sort()  # 从小到大排序

# 打印表头
print("{:<8} {:<8}".format("l1", "l2"))

# 使用 zip 函数并排循环打印两个列表
for v1, v2 in zip(l1, l2):
    print("{:<8} {:<8}".format(v1, v2))

print("-" * 30)