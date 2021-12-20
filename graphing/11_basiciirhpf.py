import numpy as np
from scipy import signal

# 1 sample delay: y[n] = beta * x[n] - alpha * y[n-1]
beta = 0.1
alpha = 1-beta
b = [beta]
a = [1, alpha]
beta = 0.5
alpha = 1-beta
b1 = [beta]
a1 = [1, alpha]
beta = 0.9
alpha = 1-beta
b2 = [beta]
a2 = [1, alpha]

# Sampling frequency = 2
w,  h  = signal.freqz(b, a, fs=2)
w1, h1 = signal.freqz(b1, a1, fs=2)
w2, h2 = signal.freqz(b2, a2, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_xscale('log')
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'black', label = f"beta = {b}")
ax1[0].plot(w, 20 * np.log10(abs(h1)), 'g', label = f"beta = {b1}")
ax1[0].plot(w, 20 * np.log10(abs(h2)), 'orange', label = f"beta = {b2}")
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].axis('tight')
ax1[0].legend(prop = {'size': 6})

# calculate the phase
angles = np.unwrap(np.angle(h))
angles1 = np.unwrap(np.angle(h1))
angles2 = np.unwrap(np.angle(h2))

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi
angles1 = ( angles1 * 180 ) / np.pi
angles2 = ( angles2 * 180 ) / np.pi

ax1[1].plot(w, angles, 'black', label = f"beta = {b}")
ax1[1].plot(w, angles1, 'g', label = f"beta = {b1}")
ax1[1].plot(w, angles2, 'orange', label = f"beta = {b2}")

ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
ax1[1].legend(prop = {'size': 6})

plt.show()
