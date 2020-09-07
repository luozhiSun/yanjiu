'''测试概率与不确定度之间的关系'''
'''通过子图的形式显示'''
import numpy as np
import math
import matplotlib.pyplot as plt
#保证中文不乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
#初始概率为0.5
pd=0.6
pf=0.4
p=0.5
iterate=10
k=2

for i in range(iterate):
    pnext=pd*p/(p*pd+pf*(1-p))
    #绘制概率变化曲线
    plt.subplot(221)
    plt.xlim(0,10)
    plt.title("概率图")
    plt.plot([i,i+1],[p,pnext],c='#20B2AA')
    #绘制不确定度变化曲线
    #计算不确定度,初始设定k=2
    uncer0=np.exp(-k*abs(math.log(1/p-1)))

    uncer1=np.exp(-k*abs(math.log(1/pnext-1)))
    plt.subplot(222)
    plt.plot([i,i+1],[uncer0,uncer1],c='#20B2AA')
    plt.xlim(0, 10)
    plt.title("不确定图")
    p=pnext


p=0.5
for i in range(iterate):
    pnext=(1-pd)*p/((1-pd)*p+(1-pf)*(1-p))
    #绘制概率变化曲线
    plt.subplot(223)
    plt.plot([i,i+1],[p,pnext],c='#FF4500')
    plt.xlim(0, 10)

    uncer0 = np.exp(-k * abs(math.log(1 / p - 1)))

    uncer1 = np.exp(-k * abs(math.log(1 / pnext - 1)))
    plt.subplot(224)
    plt.plot([i, i + 1], [uncer0, uncer1],c='#FF4500')
    plt.xlim(0, 10)

    p=pnext
plt.show()
