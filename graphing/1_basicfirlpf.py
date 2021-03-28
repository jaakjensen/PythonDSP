import numpy as np
from scipy import signal

# Filter function: y[n] = x[n] + x[n-1]
b = [1,1] 

# Sampling frequency = 2
w, h = signal.freqz(b, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax1.set_title('Digital filter frequency response')
ax1.plot(w, 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Magnitude [dB]', color='b')
ax1.set_xlabel('Normalized Frequency [$\pi$*rad/sample]')

ax2 = ax1.twinx()
angles = np.unwrap(np.angle(h))

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi

ax2.plot(w, angles, 'g')
ax2.set_ylabel('Phase (degrees)', color='g')
ax2.grid()
ax2.axis('tight')

plt.show()
