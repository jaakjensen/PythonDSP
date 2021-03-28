import numpy as np
from scipy import signal

# gain must be less than 1
# to maintain stability
g = 0.2

# Difference equation: 
# y[n] = g*x[n] + x[n-1] 
b = [g,1]
a = [1]

# y[n] = x[n] - g*y[n-1]
b1 = [1]
a1 = [1,g]

# y[n] = g*x[n] + x[n-1] - g*y[n-1]
b2 = [g,1]
a2 = [1,g]

# Sampling frequency = 2
# FIR LPF
w, h = signal.freqz(b, a, fs=2)
# IIR HPF
w1, h1 = signal.freqz(b1, a1, fs=2)
# Combined APF
w2, h2 = signal.freqz(b2, a2, fs=2)

import matplotlib.pyplot as plt


# FIR LPF magnitud
fig, ax1 = plt.subplots(4,figsize=(6.4, 8))
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'blue', label = 'Feedforward')
ax1[0].set_ylabel('Magnitude [dB]', color='blue')

# IIR HPF magnitude
ax1[0].plot(w, 20 * np.log10(abs(h1)), 'green', label = 'Feedback')

# FIR LPF phase
angles = np.angle(h)
# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi

ax1[1].plot(w, angles, 'blue', label = 'Feedforward')
ax1[1].set_ylabel('Phase (degrees)', color='blue')

# IIR HPF phase
angles = np.angle(h1)
# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi

ax1[1].plot(w1, angles, 'green', label = 'Feedback')
ax1[1].set_ylabel('Phase (degrees)', color='green')

# APF magnitude and phase
ax1[2].plot(w2, 20 * np.log10(abs(h2)), 'blue', label = 'APF magnitude')
ax1[2].set_ylabel('Magnitude [dB]', color='blue')
ax1[2].set_ylim([-20,20])


angles = np.angle(h2)
# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi

ax1[3].plot(w2, angles, 'green', label = 'APF Phase')
ax1[3].set_ylabel('Phase (degrees)', color='green')
ax1[3].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
#ax1[1].legend(prop = {'size': 6})

ax1[0].grid()
ax1[1].grid()
ax1[2].grid()
ax1[3].grid()

ax1[0].legend()
ax1[1].legend()
ax1[2].legend()
ax1[3].legend()

plt.show()
