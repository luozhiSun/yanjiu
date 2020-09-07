
from matplotlib import pyplot as plt  # 用来绘制图形

import numpy as np  # 用来处理数据

from pylab import *
#随机选择模块
from random import choice
from mpl_toolkits.mplot3d import Axes3D  # 用来给出三维坐标系。
import xlwt
import xlrd
#区域大小、目标数量
plt.ion()
Boundary=50
#发现概率阈值
B=0.9
#不确定度衰减因子
a=0.5
#目标数量
TargetNum=5
plt.pause(5)
'''静态目标初始位置设定33'''
TargetArray=np.array([[12,12],[33,16],[20,25],[45,32],[19,39]])
#类定义
class UAV:
    #local代表位置信息
    xloacl=0
    ylocal=0
    #本地目标概率矩阵,初始化为0.5
    LoaclTPM = np.zeros((Boundary+2, Boundary+2), dtype=np.float)
    #不确定度矩阵
    UnCertain=np.ones((Boundary+2,Boundary+2),dtype=np.float)
    #概率图初始化

    for i in range(Boundary+2):
        for j in range(Boundary+2):
            LoaclTPM[i][j] = 0.5
            if i==0:
                LoaclTPM[i][j]=0
            if i ==Boundary+1 :
                LoaclTPM[i][j] = 0
            if j==0:
                LoaclTPM[i][j]=0
            if j ==Boundary+1 :
                LoaclTPM[i][j] = 0

    #不确定度初始化
    for i in range(Boundary+2):
        for j in range(Boundary+2):
            if i==0:
                UnCertain[i][j]=0
            if i ==Boundary+1 :
                UnCertain[i][j] = 0
            if j==0:
                UnCertain[i][j]=0
            if j ==Boundary+1 :
                UnCertain[i][j] = 0


    #本地栅格探测次数矩阵
    LoalcSensorTime=np.zeros((Boundary+2,Boundary+2),dtype=np.int)
    #需要设定传感器的参数
    def __init__(self,pd,pf):
        self.pd=pd
        self.pf=pf
    #更新位置信息
    def SetLocal(self,x,y):
        self.xloacl=x
        self.ylocal=y
    #获取位置信息
    def GetLoacl(self):
        return self.xloacl,self.ylocal
    #更新本地传感器信息,传入目前的概率与目标是否存在的标志
    #返回下一时刻的目标存在概率,计算概率
    def UpdateLocalTPM(self,bt,x,y):
        p=self.LoaclTPM[x][y]
        #观测的栅格中目标存在
        if bt==True:
            pnext = self.pd * p / (p * self.pd + self.pf * (1 - p))
        #观测的栅格中目标不存在
        else:
            pnext = (1 - self.pd) * p / ((1 - self.pd) * p + (1 -self. pf) * (1 - p))
        self.LoaclTPM[x][y]=pnext
    #获取本地的目标概率矩阵
    def GetLoaclTPM(self):
        return self.LoaclTPM
    #获取栅格内的概率值
    def GetSingleP(self,x,y):
        return self.LoaclTPM[x][y]
    #获得传感器探测矩阵
    def GetSensorTime(self):
        return self.LoalcSensorTime
    #更新不确定度
    def UpdateUncertain(self,x,y):
        self.UnCertain[x][y]=a*self.UnCertain[x][y]
    def GetSingleUncertain(self,x,y):
        return self.UnCertain[x][y]


#传感器探测次数更新矩阵
def UpdateSensorTime(UAV,x,y):
    UAV.LoalcSensorTime[x][y]=UAV.LoalcSensorTime[x][y]+1
#判断UAV所在位置是否为目标位置
def ISTargetLocal(TargetArray,x,y):
    for i in range(TargetNum):
        if TargetArray[i][0]==x and TargetArray[i][1]==y:
            return True
    return False

# 对TPM进行画图
def ShowTPM(TPM):


    # 画出三维坐标系：
    figure = plt.figure()
    axes = Axes3D(figure)

    X = np.arange(0, Boundary, 1.0)

    Y = np.arange(0, Boundary, 1.0)

    # 限定图形的样式是网格线的样式：

    X, Y = np.meshgrid(X, Y)

    # 绘制曲面，采用彩虹色着色：
    surf = axes.plot_surface(X, Y, TPM, cmap='rainbow')

    # 图形可视化：
    plt.colorbar(surf, shrink=0.5, aspect=7)
    plt.show()
#将数据存入表格中
def save(data, path):
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])
    f.save(path)

#取整函数
def Ln(x):
    if (abs(x-0)<0.1):
        x=0
    if(x>0):
        x=round(x)
    if(x<0):
        x=math.floor(x)
    return x

'''得到所有控制输入。输入当前位置坐标，返回控制输入矩阵
   备选路径的计算基础'''
def GetU(x,y):
    U=np.zeros((27,3),dtype=np.int32)
    o = 0
    Set=[-45,0,45]
    for i in Set:
        for j in Set:
            for k in Set:
                U[o][0] = i
                U[o][1] = j
                U[o][2] = k

                o = o + 1



    return U
'''计算路径中的目标收益，输入当前位置坐标，控制输入角度，返回该条路径的目标发现收益'''
def GetTargetFind(x,y,angle,u):

    Jt=0
    for j in u:
        nextx = int(x + Ln(np.cos(math.radians((angle + j)))))
        nexty = int(y + Ln(np.sin(math.radians((angle + j)))))
        #如果到达边界，不计算其中的值
        if (nextx>Boundary):
            break
        if(nexty>Boundary):
            break
        if(nextx<0):
            break
        if(nexty<0):
            break
        #得到下一位置坐标概率
        p=UAV1.GetSingleP(nextx,nexty)
        b=0
        if(p>0.9):
            b=1
        Jt=Jt+(1-b)*p

        x = nextx
        y = nexty
        angle = angle + j
    return Jt

'''计算环境搜索收益、不确定度减少量,设置衰减因子=0.5
    输入当前位置信息，控制角度，返回环境搜索收益
如果对栅格进行访问，不确定度减少量'''
def GetEnviroment(x,y,angle,u):
    #传感器探测次数矩阵
    TimeMartix=UAV1.GetSensorTime()

    Je=0
    for j in u:
        nextx = int(x + Ln(np.cos(math.radians((angle + j)))))
        nexty = int(y + Ln(np.sin(math.radians((angle + j)))))
        if (nextx>Boundary):
            break
        if(nexty>Boundary):
            break
        if (nextx < 0):
            break
        if (nexty < 0):
            break
        # 得到下一位置的观测次数
        t=TimeMartix[nextx][nexty]
        #若选择路径后的观测次数
        t1=t+1
        #得到栅格内的不确定度
        Uncert1=UAV1.GetSingleUncertain(nextx,nexty)
        #假设访问后的不确定度
        Uncert2=a*Uncert1
        #计算不确定度减少量

        Je=Je+(Uncert1-Uncert2)

        x = nextx
        y = nexty
        angle = angle + j
    return Je

#计算执行代价,统计转弯次数，输入U
def GetCost(u):
    #计算零数值，0越多说明代价越小，对应的收益越大，防止出现负值
    n=0
    for i in u:
        if(i!=0):
            n=n+1
    C=n
    return C*0.25

#栅格图定义
map_grid = np.full((Boundary+1, Boundary+1), float(10), dtype=np.float)
# 画出定义的栅格地图
plt.figure(figsize=(8,8))
my_x_ticks = np.arange(0, Boundary+5, 5)
my_y_ticks = np.arange(0, Boundary+5, 5)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.xlim(0,Boundary)
plt.ylim(0,Boundary)
#显示目标位置信息
for i in range(TargetNum):
    plt.scatter(TargetArray[i][0], TargetArray[i][1], marker='^', c='red', s=30)
plt.grid(True)


#创建UAV1

UAV1=UAV(0.8,0.2)
#先验信息

for i in TargetArray:
    for j in range(1,Boundary+1):
        for k in range(1,Boundary+1):
            UAV1.LoaclTPM[j][k]=UAV1.LoaclTPM[j][k]+0.5*0.5*np.exp(-((j-i[0])*(j-i[0])+(k-i[1])*(k-i[1]))/5*5)


'''设定初始运动位置为（0，0），运动为右上角'''
#初始位置开始运动
move=[1,1]
Dist=[0,0,0]
#对三个运动方向随机选择
tx=move[0]
ty=move[1]
angle=45

#用来计算迭代次数
t=0
#用来统计发现目标数
k=0
#将目标概率矩阵存储到表格中
TPM=UAV1.GetLoaclTPM()
save(TPM,'test.xls')
while(True):
    #更新传感器探测次数矩阵
    UpdateSensorTime(UAV1,move[0],move[1])
    #更新位置对应的不确定度
    UAV1.UpdateUncertain(move[0],move[1])
    #判断所在位置是否为目标位置
    b=ISTargetLocal(TargetArray,move[0],move[1])
    #对概率进行更新
    UAV1.UpdateLocalTPM(b,move[0],move[1])
    #获取访问后的位置概率
    p=UAV1.GetSingleP(move[0],move[1])
    #目标全部被发现，停止循环
    if(p>B):
        k=k+1
        if(k==TargetNum):
            break
    #角度备选集合
    Set=[-45,0,45]
    #获得当前节点的备选路径
    Path=GetU(move[0],move[1])

    MaxJ=0
    s=[0,0,0]
    print(move)
    #得到最大的性能的
    for u in Path:

        J=0.6*GetTargetFind(move[0],move[1],angle,u)+0.2*GetEnviroment(move[0],move[1],angle,u)-0.3*GetCost(u)
        #J = GetTargetFind(move[0], move[1], u)- 0.3 * GetCost(u)

        print(J)
        if J>MaxJ:
            MaxJ=J
            s=u
    print("最大效益：",MaxJ)


    nextangle=s[0]
    nextx=int(move[0]+Ln(np.cos(math.radians((angle+nextangle)))))
    nexty=int(move[1]+Ln(np.sin(math.radians((angle+nextangle)))))
    plt.plot([move[0],nextx],[move[1],nexty],'c.-',linewidth=0.6)
    j=0
    move[0]=nextx
    move[1]=nexty
    angle=angle+nextangle
    plt.pause(0.5)
    t=t+1
    #如果到达边界#粗糙边界处理
    if move[0]>=Boundary-1:
        move[0]=move[0]-1
        angle=angle+90
        nextx = int(move[0] + Ln(np.cos(math.radians((angle )))))
        nexty = int(move[1] + Ln(np.sin(math.radians((angle)))))
        plt.plot([move[0], nextx], [move[1], nexty], 'c.-', linewidth=0.6)
        move[0] = nextx
        move[1] = nexty

    if move[0]<=0:
        move[0]=move[0]+1
        angle = angle + 90
        nextx = int(move[0] + Ln(np.cos(math.radians((angle)))))
        nexty = int(move[1] + Ln(np.sin(math.radians((angle)))))
        plt.plot([move[0], nextx], [move[1], nexty], 'c.-', linewidth=0.6)
        move[0] = nextx
        move[1] = nexty
    if move[1] >= Boundary-1:
        move[1] = move[1] - 1
        angle = angle + 90
        nextx = int(move[0] + Ln(np.cos(math.radians((angle)))))
        nexty = int(move[1] + Ln(np.sin(math.radians((angle)))))
        plt.plot([move[0], nextx], [move[1], nexty], 'c.-', linewidth=0.6)
        move[0] = nextx
        move[1] = nexty
    if move[1] <= 0:
        move[1] = move[1] + 1
        angle = angle + 90
        nextx = int(move[0] + Ln(np.cos(math.radians((angle)))))
        nexty = int(move[1] + Ln(np.sin(math.radians((angle)))))
        plt.plot([move[0], nextx], [move[1], nexty], 'c.-', linewidth=0.6)
        move[0] = nextx
        move[1] = nexty
print("迭代次数：",t)

plt.pause(10)
plt.show()
TPM=UAV1.GetLoaclTPM()
save(TPM,'test.xls')

def save(data, path):
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])
    f.save(path)


