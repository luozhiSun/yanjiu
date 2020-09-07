'''2020年7月1日
   三维显示目标概率图
'''
Boundary=100
from matplotlib import pyplot as plt  # 用来绘制图形

import numpy as np  # 用来处理数据

from mpl_toolkits.mplot3d import Axes3D  # 用来给出三维坐标系。

figure = plt.figure()

# 画出三维坐标系：

axes = Axes3D(figure)

X = np.arange(0, Boundary, 1.0)
print(X)
Y = np.arange(0, Boundary, 1.0)

# 限定图形的样式是网格线的样式：

X, Y = np.meshgrid(X, Y)


print(X.shape)
#初始化均赋值为0.5
'''
Z = 3 * (X) ** 2 + 2 * (Y) ** 2 + 5
print(Z.shape)'''
Z = np.zeros((Boundary, Boundary), dtype=np.float)
#重新进行赋值
for i in range(Boundary):
    for j in range(Boundary):
        Z[i][j]=0.5

#对先验信息进行初始化
for i in range(10,15):
    for j in range(10,15):
        Z[i][j]=Z[i][j]+1/(5*5)

# 绘制曲面，采用彩虹色着色：
surf=axes.plot_surface(X, Y, Z, cmap='rainbow')

# 图形可视化：
plt.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

