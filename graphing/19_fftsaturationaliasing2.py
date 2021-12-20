from scipy.fft import fft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import blackman
from scipy.signal import hann

#Chebyshev Filter Coefficients
sos = signal.cheby2(10, 100, 0.25, 'low', output='sos')

#print(sos)
#print(np.shape(sos))


for n in sos:
    #print(n)
    for j in n:
        #print(j)
        print(j, end='f, ')
    print()


#Oversampling amount
overSample = 4

#Saturation function
def saturateAsym(x):

    if x < 0:
        return x
    elif x > 3:
        return 1
    else :
        return x * (27 + x * x) / (27 + 9 * x * x)

def saturate(x):

    if x < -3:
        return -1
    elif x > 3:
        return 1
    else :
        return x * (27 + x * x) / (27 + 9 * x * x)

# Number of sample points
N = 4096

# sample spacing
Fs = 48000
T = 1.0 / Fs

#X axis
x = np.linspace(0.0, N*T, N, endpoint=False)

y = np.sin(5000.0 * 2.0*np.pi*x)
z = np.sin(5000.0 * 2.0*np.pi*x)

for n in range(0,N):
    y[n] = saturate(y[n]*10)
    #y[n] = saturateAsym(y[n]*10)
    

w = blackman(N)

yf = fft(z*w)

ywf = fft(y*w)

xf = fftfreq(N, T)[:N//2]



#Upsample
out = np.zeros((len(z))*overSample)

j=0

for n in range(0,len(out)):
    if (n % overSample) == 0:
        out[n] = z[j]
        j+=1

#Chebyshev Filter
out = signal.sosfilt(sos, out)

#Distortion
for n in range(0,len(out)):
    out[n] = saturate(out[n]*15)
    #out[n] = saturateAsym(out[n]*20)


#Chebyshev Filter
out = signal.sosfilt(sos, out)

j=0

#Decimate
for n in range(0,len(out)):
    if (n % overSample) == 0:
        z[j] = out[n]
        j+=1







#FFT for bandlimited signal
zwf = fft(z*w)

plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')

plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')

plt.semilogy(xf[1:N//2], 2.0/N * np.abs(zwf[1:N//2]), '-g')

plt.legend(['Original', 'Distortion with Aliasing', 'Upsampling, Filtering, Distorting, Filtering, Decimating'])

plt.grid()

plt.show()
