import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

res = [3.8,3.2,1.6,0.8,0.4]
wc = 0.2

#init plots
fig, ax1 = plt.subplots(2)

for i in res:

    b = [wc*wc*wc*wc*(1+i)]
    a = [1,4*wc,6*wc*wc,4*wc*wc*wc,wc*wc*wc*wc*(1+i)]

    # Analog filter
    w, h = signal.freqs(b, a, worN=np.linspace(0,np.pi,8192))
    ax1[0].plot(w, 20 * np.log10(abs(h)), linestyle='dashed',label=f'{i}')

    # calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles, linestyle='dashed')

    #Plot -3dB lines
    ax1[0].axvline(x = wc, ymin = 0, ymax = 1, color='black', linestyle='dashed')

ax1[0].set_ylim(-24,36)
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].set_xscale('log')
ax1[0].set_xlim(0.01,np.pi)
ax1[0].set_title('Analog filter frequency response')
ax1[1].set_ylabel('Phase (Radians)', color='g')
ax1[1].set_xlabel('Frequency [rad/sample]')
ax1[1].yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax1[1].set_xscale('log')
ax1[1].set_xlim(0.01,np.pi)
ax1[1].grid()
ax1[0].legend()
plt.show()
