#matplotlib是一个Python库，用于绘制各种类型的图形和图表。它提供了类似于MATLAB的绘图接口
import matplotlib.pyplot as plt
import numpy as np

def parabola(x, a, h, k):
    return a * (x - h)**2 + k

# 定义抛物线参数
a = 1  # 抛物线开口方向和形状参数
h = 0  # 顶点横坐标
k = 0  # 顶点纵坐标

# 生成x值范围
x_values = np.linspace(-10, 10, 400)
# 计算对应的y值
y_values = parabola(x_values, a, h, k)

# 绘制抛物线图像
plt.plot(x_values, y_values, label='Parabola')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Parabola')
plt.legend()
plt.grid(True)
plt.show()
