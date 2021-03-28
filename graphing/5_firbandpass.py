import numpy as np
from scipy import signal

# Filter function: y[n] = x[n] - x[n-2]
b = [1,0,-1] 

# Sampling frequency = 2*pi
# In reality it's actually just 2 hz
# and I'm manually adding the PI in
# in the graphic...
w, h = signal.freqz(b, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax1.set_title('Digital filter frequency response')
ax1.plot(w, 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Magnitude [dB]', color='b')
ax1.set_xlabel('Normalized Frequency [$\pi$*rad/sample]')

ax2 = ax1.twinx()

# Wrap angles to be from -pi to pi
# If angle is greater than pi it wraps around to
# the negative side
angles = np.unwrap(np.angle(h))

# Convert from radians to degrees:
angles = ( angles * 180 ) / np.pi
ax2.plot(w, angles, 'g')
ax2.set_ylabel('Phase (degrees)', color='g')
ax2.grid()
ax2.axis('tight')

plt.show()
