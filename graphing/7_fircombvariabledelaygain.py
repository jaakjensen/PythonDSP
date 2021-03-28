import numpy as np
from scipy import signal

# 3 sample delay: y[n] = x[n] + B * x[n-3]
b = [1,0,0,0]
b1 = [1,0,0,0.25]
b2 = [1,0,0,0.5]
b3 = [1,0,0,0.75]
b4 = [1,0,0,1]

# Sampling frequency = 2
w, h = signal.freqz(b, fs=2)
w1, h1 = signal.freqz(b1, fs=2)
w2, h2 = signal.freqz(b2, fs=2)
w3, h3 = signal.freqz(b3, fs=2)
w4, h4 = signal.freqz(b4, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'black', label = r"$\beta$ = 0")
ax1[0].plot(w, 20 * np.log10(abs(h1)), 'g', label = r"$\beta$ = 0.25")
ax1[0].plot(w, 20 * np.log10(abs(h2)), 'orange', label = r"$\beta$ = 0.5")
ax1[0].plot(w, 20 * np.log10(abs(h3)), 'blue', label = r"$\beta$ = 0.75")
ax1[0].plot(w, 20 * np.log10(abs(h4)), 'red', label = r"$\beta$ = 1")
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].legend(prop = {'size': 8})


# Wrap angles to be from -pi to pi
# If angle is greater than pi it wraps around to
# the negative side
angles = np.unwrap(np.angle(h))
angles1 = np.unwrap(np.angle(h1))
angles2 = np.unwrap(np.angle(h2))
angles3 = np.unwrap(np.angle(h3))
angles4 = np.unwrap(np.angle(h4))

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi
angles1 = ( angles1 * 180 ) / np.pi
angles2 = ( angles2 * 180 ) / np.pi
angles3 = ( angles3 * 180 ) / np.pi
angles4 = ( angles4 * 180 ) / np.pi

ax1[1].plot(w, angles, 'black', label = r"$\beta$ = 0")
ax1[1].plot(w, angles1, 'g', label = r"$\beta$ = 0.25")
ax1[1].plot(w, angles2, 'orange', label = r"$\beta$ = 0.5")
ax1[1].plot(w, angles3, 'blue', label = r"$\beta$ = 0.75")
ax1[1].plot(w, angles4, 'red', label = r"$\beta$ = 1")

ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
#ax1[1].legend(prop = {'size': 6})

plt.show()
