import pandas as pd


def finddata():
    demo_df = pd.read_excel(r'2020-11-10 超重.xls')  ##文件路径
    print(len(demo_df.loc[0].values))
    print(demo_df.columns.values[2])
    print(demo_df.iloc[0, 0])
    list = demo_df.columns.values
    for i in range(len(list)):
        if (list[i] == '状态'):
            print('行数：', 1, '列数：', i + 1)
            print(demo_df.loc[0].values[i])
finddata()
