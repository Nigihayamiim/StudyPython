def worker_add(work):
    while True:
        input_bh = input('请输入员工编号:')
        if input_bh not in work.keys():
            input_name = input('请输入员工姓名:')
            input_gz = input('请输入员工工资:')
            input_sex = input('请输入员工性别:')
            worker = {'姓名': input_name, '工资': input_gz, '性别': input_sex}
            work.setdefault(input_bh, worker)
            input('员工%s添加成功' % input_bh)
            break
        elif input_bh == 'quit':
            break
        else:
            input('错误!已存在员工编号' + input_bh)

def worker_del(work):
    while True:
        input_bh = input('请输入需要删除的员工编号:')
        worker_id = list(work.keys())
        if input_bh in worker_id:
            del work[input_bh]
            input('员工删除成功')
            break
        elif input_bh == 'quit':
            break
        else:
            input('输入员工编号有误!')

def worker_serch(work):
    work_item = list(work.items())
    for it in work_item:
        it_items = it[1].items()
        print('编号:' + it[0], end='\t')
        for i in it_items:
            print(i[0] + ':' + i[1], end='\t')
        print()
    input('')

def worker_change(work):
    while True:
        input_bh = input('请输入需要修改的员工编号:')
        if input_bh in work.keys():
            new_name = input("姓名是%s\t请输入新的姓名:" % work[input_bh]['姓名'])
            new_sala = input("工资是%s\t请输入新的姓名:" % work[input_bh]['工资'])
            new_sex = input("性别是%s\t请输入新的姓名:" % work[input_bh]['性别'])
            if new_name == '':
                new_name = work[input_bh]['姓名']
            elif new_sala == '':
                new_sala = work[input_bh]['工资']
            elif new_sex == '':
                new_sex = work[input_bh]['性别']
            work[input_bh]['姓名'] = new_name
            work[input_bh]['工资'] = new_sala
            work[input_bh]['性别'] = new_sex
            input('员工%s的信息修改成功!' % input_bh)
            break
        elif input_bh == 'quit':
            break
        else:
            input('您输入的编号不存在!请重新输入.')



