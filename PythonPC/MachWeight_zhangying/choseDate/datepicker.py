import tkinter as tk

from PythonPC.MachWeight_zhangying.choseDate.Calendar import Calendar


class datepicker:
    def __init__(s, window, axes):  # 窗口对象 坐标
        s.window = window
        s.frame = tk.Frame(s.window, padx=5)
        s.frame.grid(row=axes[0], column=axes[1])
        s.start_date = tk.StringVar()  # 开始日期
        s.end_date = tk.StringVar()  # 结束日期
        s.bt1 = tk.Button(s.frame, text='开始', command=lambda: s.getdate('start'))  # 开始按钮
        s.bt1.grid(row=0, column=0)
        s.ent1 = tk.Entry(s.frame, textvariable=s.start_date)  # 开始输入框
        s.ent1.grid(row=0, column=1)
        s.bt2 = tk.Button(s.frame, text='结束', command=lambda: s.getdate('end'))
        s.bt2.grid(row=0, column=2)
        s.ent2 = tk.Entry(s.frame, textvariable=s.end_date)
        s.ent2.grid(row=0, column=3)

    def getdate(s, type):  # 获取选择的日期
        for date in [Calendar().selection()]:
            if date:
                if (type == 'start'):  # 如果是开始按钮，就赋值给开始日期
                    s.start_date.set(date)
                elif (type == 'end'):
                    s.end_date.set(date)


# 执行
if __name__ == '__main__':
    window = tk.Tk()
    window.wm_attributes('-topmost', True)  # 窗口置顶
    tk.Label(window, text='日期段一:').grid(row=0, column=0)
    obj = datepicker(window, (0, 1))  # 初始化类为对象
    startstamp1 = obj.start_date.get()  # 获取开始时期
    endstamp1 = obj.end_date.get()

    tk.Label(window, text='日期段二:').grid(row=1, column=0)
    obj = datepicker(window, (1, 1))
    startstamp2 = obj.start_date.get()
    endstamp2 = obj.end_date.get()
    window.mainloop()