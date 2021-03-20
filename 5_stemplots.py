
import matplotlib.pyplot as plt 
import numpy as np


fig, axes = plt.subplots(nrows=2,ncols=1)

t = np.linspace(0, 2*np.pi,25)
a = np.sin(t)

axes[0].stem(t,a, use_line_collection = True, label = 'My function')
axes.set_title('My Stem Plot')
axes.set_xlabel('Time')
axes.set_ylabel('Amplitude')

ax.legend(loc = 0)
plt.show()


