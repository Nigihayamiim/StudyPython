import datetime

import xlwt

def set_style(name, height, bold = False):
    style = xlwt.XFStyle()   #初始化样式

    font = xlwt.Font()       #为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 1
    font.height = height

    style.font = font
    return style

def write_excel(datas,filename,date):
    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')

    # 创建sheet
    data_sheet = workbook.add_sheet('demo')

    # 设置格式----------------------------------------------

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy-MM-dd '

    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = '等线'
    font.bold = False
    font.color_index = 1
    font.height = 220

    al = xlwt.Alignment()  # 设置单元格对齐方式
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中

    style.font = font
    style.alignment = al
    date_format.font = font
    date_format.alignment = al

    data_sheet.col(0).width = 3000
    data_sheet.col(1).width = 8000
    data_sheet.col(2).width = 3800
    data_sheet.col(3).width = 3000
    data_sheet.col(4).width = 3500
    data_sheet.col(5).width = 6000

    # ----------------------------------------------------

    row0 = ['商店编号', '商店名称', '联系方式', '商店地区', '收录日期', '商品编号']
    for i in range(len(row0)):
        data_sheet.write(0, i, row0[i], style)
    nrows = len(datas)

    for i in range(nrows):
        for j in range(len(row0)):
            if j == 4:
                data_sheet.write(i + 1, j, datas[i][j], date_format)
            else:
                data_sheet.write(i+1, j, datas[i][j], style)


    # 工作簿保存到磁盘
    workbook.save("C:\\Users\\WaitingForTheName\\Desktop\\" + filename)