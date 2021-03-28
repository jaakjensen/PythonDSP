import numpy as np
from scipy import signal

# 5 sample delay: y[n] = x[n] + y[n-5]
b = [1]
a = [1,0,0,0,0,1]

# Sampling frequency = 2
w, h = signal.freqz(b, a, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'blue')
ax1[0].set_ylabel('Magnitude [dB]', color='blue')

angles = np.angle(h)

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi

ax1[1].plot(w, angles, 'green')
ax1[1].set_ylabel('Phase (degrees)', color='green')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
#ax1[1].legend(prop = {'size': 6})

plt.show()
