from scipy.fft import fft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import hann

# Number of sample points
N1 = 1024
N2 = 1024
N3 = 1024
# sample spacing
Fs = 48000
T = 1.0 / Fs
#X axis
x1 = np.linspace(0.0, N1*T, N1, endpoint=False)
x2 = np.linspace(0.0, N2*T, N2, endpoint=False)
x3 = np.linspace(0.0, N3*T, N3, endpoint=False)
#Signals -> two on bin edge, other in center
y1 = np.cos(2.0*np.pi*x1*4687.5)
y2 = np.cos(2.0*np.pi*x2*4710.9375)
y3 = np.cos(2.0*np.pi*x3*4734.375)
#Window
w1 = hann(N1)
w2 = hann(N2)
w3 = hann(N3)
#FFT of signal with window
ywf1 = fft(y1*w1)
ywf2 = fft(y2*w2)
ywf3 = fft(y3*w3)
# Used to calculate bins
# We only grab the first half of the bins
# because we don't need the negative frequencies
xf1 = np.arange(0,Fs/2,Fs/N1)
xf2 = np.arange(0,Fs/2,Fs/N2)
xf3 = np.arange(0,Fs/2,Fs/N3)

plt.semilogy(xf1[0:int(N1/2)], 2.0/N1 * np.abs(ywf1[0:int(N1/2)]), '-r',marker="o")
plt.semilogy(xf2[0:int(N2/2)], 2.0/N2 * np.abs(ywf2[0:int(N2/2)]), '-g',marker="o")
plt.semilogy(xf3[0:int(N3/2)], 2.0/N3 * np.abs(ywf3[0:int(N3/2)]), '-b',marker="o")

plt.legend([f'Frequency 1 = 4.688kHz', f'Frequency 2 = 4.711kHz',
            f'Frequency 3 = 4.734kHz'])
plt.grid()
plt.show()
