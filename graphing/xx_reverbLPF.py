import numpy as np
from scipy import signal

# 1 sample delay: y[n] = x[n] + y[n-1]
b = [0.25]
a = [1, 0.75]

# Sampling frequency = 2
w, h = signal.freqz(b, a, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'blue')
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].axis('tight')

# calculate the phase
angles = np.angle(h)

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi

ax1[1].plot(w, angles, 'green')

ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
#ax1[1].legend(prop = {'size': 6})

plt.show()
