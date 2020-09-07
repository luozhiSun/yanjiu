'''UAV八个方向的运动，栅格图
2020年7月1日：实现向静态目标靠近，距离区域开始位置后的运动未完成
'''

import numpy as np
from pylab import *
#随机选择模块
from random import choice

import seaborn as sns

cmap = sns.cubehelix_palette(start = 1.5, rot = 3, gamma=0.8, as_cmap = True)


# 定义一个含有障碍物的30×30的栅格地图

#定义边界
Boundary=100
map_grid = np.full((Boundary, Boundary), float(10), dtype=np.float)

# 画出定义的栅格地图
plt.figure(figsize=(10,10))
my_x_ticks = np.arange(0, Boundary+10, 10)
my_y_ticks = np.arange(0, Boundary+10, 10)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.xlim(0,Boundary)
plt.ylim(0,Boundary)
'''静态目标初始位置设定33'''
plt.scatter(12.5,12.5,marker='^',c='red',s=100)


plt.grid(True)

'''二维情况下设置UAV的8个运动方向'''
#定义一个数组存储运动方向，x和y的位置变化
#设置7X2数组存储xy方向运动的距离
#第一行定义为方向，2，3行定义为对应的位置变化
MoveType=np.zeros((8,3),dtype=np.float)
j=1
for i in range(8):
    MoveType[i][0]=j
    j=j+1
'''用数学公式表示无人机之间的运动'''
'''手动赋值,无人机运动矩阵'''

MoveType[0][1]=1
MoveType[0][2]=0
MoveType[1][1]=1
MoveType[1][2]=1
MoveType[2][1]=0
MoveType[2][2]=1
MoveType[3][1]=-1
MoveType[3][2]=1
MoveType[4][1]=-1
MoveType[4][2]=0
MoveType[5][1]=-1
MoveType[5][2]=-1
MoveType[6][1]=0
MoveType[6][2]=-1
MoveType[7][1]=1
MoveType[7][2]=-1

'''设定初始运动位置为（0，0），运动为右上角'''
#初始位置开始运动
move=[1,1]
Dist=[0,0,0]
#对三个运动方向随机选择
tx=move[0]
ty=move[1]
angle=0
Set=[0,0,0]
#对无人机的八个方向的随机运动，并且设定了边界限制
while(True):
    Set[0]=(angle-1)%8
    Set[1]=angle
    Set[2]=(angle+1)%8

    nextangle=choice(Set)
    nextx=move[0]+MoveType[nextangle][1]
    nexty=move[1]+MoveType[nextangle][2]
    plt.plot([move[0],nextx],[move[1],nexty],'m.-',c='black')
    j=0
    move[0]=nextx
    move[1]=nexty
    angle=nextangle
    plt.pause(0.5)
    #如果到达边界
    #if move[0]>Boundary or move[0]<0 or move[1]>Boundary or move[1]<0:
     #   break
    if move[0]>Boundary:
        move[0]=move[0]-1
    if move[0]<=0:
        move[0]=move[0]+1
    if move[1] > Boundary:
        move[1] = move[1] - 1
    if move[1] <= 0:
        move[1] = move[1] + 1

    print(move[0],move[1])

plt.show()