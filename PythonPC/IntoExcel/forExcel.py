import datetime

import xlwt

def set_style(name, height, bold = False):
    style = xlwt.XFStyle()   #初始化样式

    font = xlwt.Font()       #为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    return style

def write_excel(datas,filename,date):
    #创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    #创建sheet
    data_sheet = workbook.add_sheet('demo')
    row0 = [u'单号', u'下单重量', '实际重量', '检查时间']
    for i in range(len(row0)):
        data_sheet.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    nrows=len(datas)
    for i in range(nrows):
        for j in range(len(row0)):
            if j == 3:
                data_sheet.write(i + 1, 3, date)
            else:
                data_sheet.write(i+1,j,datas[i][j])

    # 工作簿保存到磁盘
    workbook.save("C:\\Users\\WaitingForTheName\\Desktop\\" + filename)