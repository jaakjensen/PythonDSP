import numpy as np
from scipy import signal

# 5 sample delay: y[n] = x[n] + y[n-5]
b =  [1]
a =  [1,0,0,0,0,1]              #5 sample delay
a1 = [1,0,0,0,0,0,0,1]          #7 sample delay
a2 = [1,0,0,0,0,0,0,0,0,1]        #9 sample delay
a3 = [1,0,0,0,0,0,0,0,0,0,0,1]      #11 sample delay
a4 = [1,0,0,0,0,0,0,0,0,0,0,0,0,1]    #13 sample delay

# Sampling frequency = 2
w,  h  = signal.freqz(b, a, fs=2)
w1, h1 = signal.freqz(b, a1, fs=2)
w2, h2 = signal.freqz(b, a2, fs=2)
w3, h3 = signal.freqz(b, a3, fs=2)
w4, h4 = signal.freqz(b, a4, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_title('Digital filter frequency response')
ax1[0].plot(w, 20 * np.log10(abs(h)), 'black', label = r"delay = 5")
ax1[0].plot(w, 20 * np.log10(abs(h1)), 'g', label = r"delay = 7")
ax1[0].plot(w, 20 * np.log10(abs(h2)), 'orange', label = r"delay = 9")
ax1[0].plot(w, 20 * np.log10(abs(h3)), 'blue', label = r"delay = 11")
ax1[0].plot(w, 20 * np.log10(abs(h4)), 'red', label = r"delay = 13")
ax1[0].set_ylabel('Magnitude [dB]', color='black')
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

ax1[1].plot(w, angles, 'black', label = r"delay = 5")
ax1[1].plot(w, angles1, 'g', label = r"delay = 7")
ax1[1].plot(w, angles2, 'orange', label = r"delay = 9")
ax1[1].plot(w, angles3, 'blue', label = r"delay = 11")
ax1[1].plot(w, angles4, 'red', label = r"delay = 13")

ax1[1].set_ylabel('Phase (degrees)', color='black')
ax1[1].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].grid()
ax1[1].axis('tight')
#ax1[1].legend(prop = {'size': 6})

plt.show()
