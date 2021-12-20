from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

#Chebyshev Filter Coefficients
b = [ 0.00757702, -0.02666634,  0.06433529, -0.09739344,  0.11965053, -0.10339635,
  0.07472005, -0.0214037,  -0.0214037,   0.07472005, -0.10339635,  0.11965053,
 -0.09739344,  0.06433529, -0.02666634,  0.00757702]


a = [ 1.00000000e+00, -6.35728196e+00,  2.04575618e+01, -4.29494964e+01,
  6.51181196e+01, -7.49392883e+01,  6.73105585e+01, -4.78581686e+01,
  2.70870646e+01, -1.21715215e+01,  4.30082438e+00, -1.17046262e+00,
  2.37624459e-01, -3.36085164e-02,  2.99150600e-03, -7.07731789e-05]

def saturate(x):

    if x < -3:
        return -1
    elif x > 3:
        return 1
    else :
        return x * (27 + x * x) / (27 + 9 * x * x)

# Number of sample points
N = 4096
Fs = 48000
T = 1 / Fs

x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(5000 * 2.0*np.pi*x)
z = np.sin(5000 * 2.0*np.pi*x)

for n in range(0,N):
    y[n] = saturate(y[n]*20)

fig, ax1 = plt.subplots(2)

ax1[0].plot(x[0:128], y[0:128])
ax1[0].plot(x[0:128], z[0:128])


yf = fft(y)
xf = fftfreq(N, T)[:N//2]
ax1[1].plot(xf, 2.0/N * np.abs(yf[0:N//2]))

yf = fft(z)
xf = fftfreq(N, T)[:N//2]
ax1[1].plot(xf, 2.0/N * np.abs(yf[0:N//2]))

#Upsample
xUpSample = np.linspace(0.0, N*T, N, endpoint=False)

#Chebyshev Filter

#Distort

#Down Sample

#FFT


plt.grid()
#plt.xscale('log')
plt.show()
