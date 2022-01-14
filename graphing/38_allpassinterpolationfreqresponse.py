import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(2)
ax1[0].set_xscale('log')
ax1[1].set_xscale('log')

for i in range(1,101):
    f = 0.01 * i + 0.5
    b = [f,1]
    a = [1,f]

    # Sampling frequency = 2
    w, h = signal.freqz(b,a, fs=48000)

    #ax1[0].plot(w, 20 * np.log10(abs(h)), label=f'Coef = {i*coef:.2f}')
    ax1[0].plot(w, 20 * np.log10(abs(h)))
    
    angles = np.unwrap(np.angle(h))

    # Convert from radians to degrees:
    angles = ( angles * 180 ) / np.pi

    #ax1[1].plot(w, angles, label=f'Coef = {i*coef:.2f}')
    ax1[1].plot(w, angles)

ax1[0].set_ybound(-20,10)
ax1[0].set_title('Digital filter frequency response')
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].set_xlabel('Normalized Frequency [$\pi$*rad/sample]')
ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].grid()
ax1[0].legend()
ax1[1].legend()
plt.show()
