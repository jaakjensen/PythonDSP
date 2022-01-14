import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_xscale('log')
ax1[1].set_xscale('log')

for i in range(1,101):
    f = 0.01 * i
    xmp2 = (1.0* (f**3) - 1*(f**2) +  0*f)
    xmp1 = (-1 * (f**3) + 1*(f**2) +  1*f)
    xm   = (1.0* (f**3) - 2*(f**2) +  0*f + 1)
    xmm1 = (-1 * (f**3) + 2*(f**2) + -1*f)

    b = [xmp2,xmp1,xm,xmm1] 

    # Sampling frequency = 2
    w, h = signal.freqz(b, fs=48000)

    #ax1[0].plot(w, 20 * np.log10(abs(h)), label=f'Coef = {i*coef:.2f}')
    ax1[0].plot(w, 20 * np.log10(abs(h)))
    
    angles = np.unwrap(np.angle(h))

    # Convert from radians to degrees:
    angles = ( angles * 180 ) / np.pi

    #ax1[1].plot(w, angles, label=f'Coef = {i*coef:.2f}')
    ax1[1].plot(w, angles)

ax1[0].set_title('Digital filter frequency response')
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].grid()
ax1[0].legend()
ax1[1].legend()
plt.show()
