from 员工管理系统.主页面 import show_menu
from 员工管理系统.增删查改 import worker_add
from 员工管理系统.增删查改 import worker_del
from 员工管理系统.增删查改 import worker_change
from 员工管理系统.增删查改 import worker_serch

def yggl():
    work = {}
    while True:
        show_menu()
        input_num = int(input('请输入您的操作:'))
        print('*' * 20)
        if input_num == 1:
            worker_add(work)
        elif input_num == 2:
            worker_del(work)
        elif input_num == 3:
            worker_change(work)
        elif input_num == 4:
            worker_serch(work)
        elif input_num == 5:
            print('感谢使用本系统,再见')
            break
        else:
            print('输入有误请重新输入')