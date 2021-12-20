from scipy.fft import fft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import hann

# Number of sample points
N = 1024
# sample spacing
Fs = 48000
T = 1.0 / Fs
#X axis
x = np.linspace(0.0, N*T, N, endpoint=False)
#Signal
y = np.cos(2.0*np.pi*x*5000)
#Window
w = hann(N)
#FFT of signal without window
yf = fft(y)
#FFT of signal with window
ywf = fft(y*w)

# Used to calculate bins
# We only grab the first half of the bins
# because we don't need the negative frequencies
xf = np.arange(0,Fs/2,Fs/N)

plt.semilogy(xf[0:int(N/2)], 2.0/N * np.abs(yf[0:int(N/2)]), '-b')
plt.semilogy(xf[0:int(N/2)], 2.0/N * np.abs(ywf[0:int(N/2)]), '-r')
plt.legend(['FFT without Window', 'FFT with Window'])
plt.grid()
plt.show()
