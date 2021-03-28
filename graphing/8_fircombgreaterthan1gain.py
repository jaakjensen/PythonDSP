import numpy as np
from scipy import signal

# 3 sample delay: y[n] = x[n] + B * x[n-3]
b = [1,0,0,0.5]
b1 = [1,0,0,2]

# Sampling frequency = 2
w, h = signal.freqz(b, fs=2)
w1, h1 = signal.freqz(b1, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'black', label = r"$\beta$ = 0.5")
ax1[0].plot(w, 20 * np.log10(abs(h1)), 'g', label = r"$\beta$ = 2")
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].legend(prop = {'size': 8})

# calculate the phase
angles = np.angle(h)
angles1 = np.angle(h1)

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi
angles1 = ( angles1 * 180 ) / np.pi

ax1[1].plot(w, angles, 'black', label = r"$\beta$ = 0")
ax1[1].plot(w, angles1, 'g', label = r"$\beta$ = 0.25")

ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
#ax1[1].legend(prop = {'size': 6})

plt.show()
