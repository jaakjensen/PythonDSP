import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# y[n] = (b0/a0)*x[n] + (b1/a0)*x[n-1] + (b2/a0)*x[n-2] - ...
#           (a1/a0)*y[n-1] - (a2/a0)*y[n-2]


Fs = 48000
cutoff = 2000
Q = 40
dBGain = 6

#Intermediate variables
w0 = 2*np.pi*cutoff/Fs          # Angular freq. (radians/sample)
bw = cutoff/Q                   #Filter width
A = np.sqrt(10**(dBGain/20))

#Filter coefficients
b2 = np.exp(-2*np.pi*bw/Fs)
b1 = -1*(4*b2/(1+b2))*np.cos(w0)

a0 = 1-np.sqrt(b2)
a2 = -1*a0

print(b1)
print(b2)
print(a0)
print(a2)

b = [a0, 0, a2]
a = [1, b1, b2]

# Sampling frequency = Fs
w, h = signal.freqz(b, a, fs=48000)

fig, ax1 = plt.subplots(2)
ax1[0].set_xscale('log')
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
