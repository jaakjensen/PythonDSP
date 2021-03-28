import numpy as np
from scipy import signal

# 1 sample delay: u[n] = x[n] + x[n-1]
# 1 sample delay: y[n] = u[n] + u[n-1]
# Final equation: y[n] = x[n] + x[n-1] + x[n-1] + x[n-2]
#                 y[n] = x[n] + 2*x[n-1] + x[n-2]

# Two series LPFs with the system gain normalized
b = [0.25,0.5,0.25]

# Single LPF difference equation
b1 = [0.5,0.5]

# Sampling frequency = 2
w, h = signal.freqz(b, fs=2)
w1, h1 = signal.freqz(b1, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'black', label = "Series LPFs")
ax1[0].plot(w, 20 * np.log10(abs(h1)), 'g', label = "Single LPF") 
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].legend(prop = {'size': 8})
ax1[0].axis('tight')

# calculate the phase
angles = np.angle(h)
angles1 = np.angle(h1)

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi
angles1 = ( angles1 * 180 ) / np.pi

ax1[1].plot(w, angles, 'black', label = "Series LPFs")
ax1[1].plot(w, angles1, 'g', label = "Single LPF")

ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
#ax1[1].legend(prop = {'size': 6})

plt.show()
