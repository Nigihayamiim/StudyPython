import random
# print("现在进行简单运算")
# input_one = input("请输入第一个数：")
# int_input_one = int(input_one)
# input_fu = input("请输入运算符：")
# input_two = input("请输入第三个数")
# int_input_two = int(input_two)
# if input_fu == '*':
#     result = int_input_one * int_input_two
# elif input_fu == '/':
#     result = int_input_one / int_input_two
# elif input_fu == '+':
#     result = int_input_one + int_input_two
# elif input_fu == '-':
#     result = int_input_one - int_input_two
# else :
#     print("错误")
# print("结果是：%d" % result)

# 生成随机数 random
#
# computer = random.randint(0,2)
# print(computer)

# while循环
# i = 1
# sum = 0
# while i<=100 :
#     sum += i
#     i += 1
# print(sum)

# # 函数
def jisuanqi():
    print("现在进行简单运算")
    input_one = input("请输入第一个数：")
    int_input_one = int(input_one)
    input_fu = input("请输入运算符：")
    input_two = input("请输入第三个数")
    int_input_two = int(input_two)
    if input_fu == '*':
        result = int_input_one * int_input_two
    elif input_fu == '/':
        result = int_input_one / int_input_two
    elif input_fu == '+':
        result = int_input_one + int_input_two
    elif input_fu == '-':
        result = int_input_one - int_input_two
    else:
        print("错误")
    print("结果是：%d" % result)

# jisuanqi()

# my_str = 'nihaoya'
# for v in my_str:
#     print(v)

# user_email = 'zzjim@outlook.com'
# index = user_email.find('@')
# print(index)
# print(user_email[::-1])

# # 列表
# my_list = []
# i = 0
# while i < 10:
#     num = random.randint(1, 10)
#     my_list.append(num)
#     i += 1
# # 对列表元素进行排序，默认是升序
# my_list.sort()
# print(my_list)
# my_list.sort(reverse=True)
# print(my_list)
# # 逆序
# my_list.reverse()
# print(my_list)
# # 列表查找 index(元素) pop(位置)
# if 3 in my_list:
#     pos = my_list.index(3)
#     my_list.pop()
#     print(pos)

# # 合并列表
# my_list2 = ['aa', 'bb', 'cc']
# my_list.extend(my_list2)
# print(my_list)
#
teacher = ['杨老师', '徐老师', '朱老师', '陈老师', '胡老师', '李老师', '赵老师', '欧阳老师']
school = [[], [], []]

for v in teacher:
    random_num = random.randint(0, 2)
    school[random_num].append(v)
for s in school:
    print(s)












