import numpy as np
from scipy import signal

sos = signal.cheby2(10, 100, 0.125, 'low', output='sos')

print(sos)

# Sampling frequency = Fs
w, h = signal.sosfreqz(sos, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(3)
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

#x = signal.unit_impulse(1000)
#y_tf = signal.lfilter(b, a, x)
#ax1[2].plot(y_tf, 'r', label='TF')
#ax1[2].set_ylabel('Amplitude', color='g')
#ax1[2].set_xlabel('Time/samples')

plt.show()
