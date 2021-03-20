
import matplotlib.pyplot as plt 
import numpy as np


fig, axes = plt.subplots(nrows=2,ncols=1)

m = 3
b = 1
x = np.array([0,1,2,3])
y = np.array([(m*0+b),(m*1+b),(m*2+b),(m*3+b)])


axes[0].plot(x, y, color='b',ls='-',lw=4)


t = np.linspace(0, 2*np.pi,25)
a = np.sin(t)

axes[1].plot(t, a, color='r',ls='--',lw=2)

plt.show()


