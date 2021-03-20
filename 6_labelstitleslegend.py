
import matplotlib.pyplot as plt 
import numpy as np


fig, axes = plt.subplots(nrows=1,ncols=1)

t = np.linspace(0, 2*np.pi,25)
a = np.sin(t)

axes.plot(t,a, color='red', marker = 'o', label = 'sin(t)')
axes.plot(t,3*a, color='blue', marker = 'o', label = '3*sin(t)')

axes.set_title('my plot')
axes.set_xlabel('time')
axes.set_ylabel('amplitude')

axes.set_xlim([-5,10])
axes.set_ylim([-5,5])

axes.legend(loc = 0)
plt.show()


