# 获得要拷贝的文件的名称

data = input("请输入需要拷贝文件的文件名:")
# 获取要拷贝的文件的文件类型
data.rfind('.')
# 读取要拷贝的文件内容,并存储
f = open(data, 'rb')
line = f.readlines()
f.close()

# 输入新文件的名称
copy_data = input('请输入新文件的名称:')
# 创建新文件并写入拷贝的文件内容
f = open('copy_a', 'wb')
f.writelines(line)
f.close()
