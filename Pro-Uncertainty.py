'''绘制不确定度中参数以及不确定度与概率之间的关系'''
import numpy as np
import math
import matplotlib.pyplot as plt
#保证中文不乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

#确定x的范围
x = np.linspace(0.0001, 1.0, 100,dtype=float)
print(x)

for k in range(5):
    # 不确定度计算公式
    k=k+1
    s="k="+str(k)

    uncertain = np.exp(-k * abs(np.log(1 / x - 1)))
    plt.plot(x,uncertain,label=s)
    plt.legend(frameon=True,loc='upper right')

plt.title("不确定度与概率关系")
plt.show()