import numpy as np
from scipy import signal

# 3 sample delay: y[n] = x[n] + x[n-3]
b = [1,0,0,1]

# 4 sample delay: y[n] = x[n] + x[n-4]
b1 = [1,0,0,0,1] 

# 5 sample delay: y[n] = x[n] + x[n-5]
b2 = [1,0,0,0,0,1] 

# Sampling frequency = 2
w, h = signal.freqz(b, fs=2)
w1, h1 = signal.freqz(b1, fs=2)
w2, h2 = signal.freqz(b2, fs=2)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax1.set_title('Digital filter frequency response')
ax1.plot(w, 20 * np.log10(abs(h)), 'black', label = "3-sample delay")
ax1.plot(w, 20 * np.log10(abs(h1)), 'g', label = "4-sample delay")
ax1.plot(w, 20 * np.log10(abs(h2)), 'orange', label = "5-sample delay")
ax1.set_ylabel('Magnitude [dB]', color='b')
ax1.set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1.legend()

plt.show()
