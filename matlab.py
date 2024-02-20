#matplotlib是一个Python库，用于绘制各种类型的图形和图表。它提供了类似于MATLAB的绘图接口
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
