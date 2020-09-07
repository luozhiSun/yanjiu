import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 用来给出三维坐标系。
Boundary=50
TPM=np.zeros([Boundary+2,Boundary+2],dtype=np.float)
for i in range(Boundary+2):
    for j in range(Boundary+2):
        TPM[i][j] = 0.5
        if(i==0):
            TPM[i][j]=0
        if(j==0):
            TPM[i][j]=0
        if(i==Boundary+1):
            TPM[i][j]=0
        if(j==Boundary+1):
            TPM[i][j]=0
TargetArray=[[10,10],[20,25],[30,15]]
for i in TargetArray:
    for j in range(1,Boundary+1):
        for k in range(1,Boundary+1):
            TPM[j][k]=TPM[j][k]+0.5*0.4*np.exp(-((j-i[0])*(j-i[0])+(k-i[1])*(k-i[1]))/5*5)
#显示TMP
# 对TPM进行画图
def ShowTPM(TPM):


    # 画出三维坐标系：
    figure = plt.figure()
    axes = Axes3D(figure)

    X = np.arange(0, Boundary+2, 1.0)

    Y = np.arange(0, Boundary+2, 1.0)

    # 限定图形的样式是网格线的样式：

    X, Y = np.meshgrid(X, Y)

    # 绘制曲面，采用彩虹色着色：
    surf = axes.plot_surface(X, Y, TPM, cmap='rainbow')

    # 图形可视化：
    plt.colorbar(surf, shrink=0.5, aspect=7)
    plt.show()
ShowTPM(TPM)