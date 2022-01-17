# Normalized band pass filter
# 2R*Hbpf(z) -> multiply normal
# BPF by 2R, aka 2*resonance control
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#for this particular example, ignore div/0 
#in the np.log10 expression
np.seterr(divide = 'ignore') 

res = [1,0.8,0.4,0.2,0.1]
wc = 0.2*np.pi #FYI sample rate = 2*pi
g = np.tan(wc/2)

#init plots
fig, ax1 = plt.subplots(2)

for i in res:

    # Digital Filter
    a = 1 / (1+2*i*g+g**2)
    b = 2*i+g
    c = g
    d = g

    Bd = [2*i*a*c,0,2*i*-1*a*c]
    Ad = [1,2*(a*b*c+a*c*d-1),(2*a*c*d-2*a*b*c+1)]

    # Sampling frequency = 2*pi
    w, h = signal.freqz(Bd, Ad, worN=4096, fs=2*np.pi)
    ax1[0].plot(w, 20 * np.log10(abs(h)))

    # calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles)

    # Analog filter
    b = [2*i*wc,0]
    a = [1,2*i*wc,wc*wc]

    w, h = signal.freqs(b, a, worN=np.linspace(0,np.pi,4096))
    ax1[0].plot(w, 20 * np.log10(abs(h)), linestyle='dashed')

    # calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles, linestyle='dashed')

    #Plot -3dB lines
    ax1[0].axvline(x = wc, ymin = 0, ymax = 1, color='black', linestyle='dashed')

ax1[0].set_ylim(-40,16)
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].set_xscale('log')
ax1[0].set_xlim(0.01,np.pi)
ax1[0].set_title('Digital Filter frequency response')
ax1[1].set_ylabel('Phase (radians)', color='g')
ax1[1].set_xlabel('Frequency [rad/sample]')
ax1[1].yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax1[1].set_xscale('log')
ax1[1].set_xlim(0.01,np.pi)
ax1[1].grid()
plt.show()

