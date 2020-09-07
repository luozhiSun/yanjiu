#2020年8月18日，该文件用来显示目标概率图
#并从表格中读取数据，并进行三维展示

import xlwt
import xlrd
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 用来给出三维坐标系。
Boundary=50
#存入数据到excel表格中
def save(data, path):
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])
    f.save(path)
#显示概率图
def ShowTPM(TPM):


    # 画出三维坐标系：
    figure = plt.figure()
    axes = Axes3D(figure)

    X = np.arange(0, Boundary+2, 1.0)

    Y = np.arange(0, Boundary+2, 1.0)

    # 限定图形的样式是网格线的样式：

    X, Y = np.meshgrid(X, Y)

    # 绘制曲面，采用彩虹色着色：
    surf = axes.plot_surface(X, Y, TPM, color="deepskyblue")

    # 图形可视化：
    #plt.colorbar(surf, shrink=0.5, aspect=7)
    plt.show()

#从excel表格中读取数据

def excel_to_matrix(path):
    table = xlrd.open_workbook(path).sheets()[0]  # 获取第一个sheet表
    row = table.nrows  # 行数
    col = table.ncols  # 列数
    datamatrix = np.zeros((row, col))  # 生成一个nrows行ncols列，且元素均为0的初始矩阵
    for x in range(col):
        cols = np.matrix(table.col_values(x))  # 把list转换为矩阵进行矩阵操作
        datamatrix[:, x] = cols  # 按列把数据存进矩阵中

    return datamatrix

TPM=excel_to_matrix('test.xls')
ShowTPM(TPM)
