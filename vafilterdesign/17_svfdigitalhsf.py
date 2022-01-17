# Digital High Shelf Filter
# 1+K*Hhpf(z) where
# K is the boost/cut factor.
# NOTE: Set K using dBGain.
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#for this particular example, ignore div/0 
#in the np.log10 expression
np.seterr(divide = 'ignore') 

dBGain = 6
K = (10**(dBGain / 20)-1)
res = [1,0.8,0.4,0.2,0.1]
wc = 0.1*np.pi #FYI sample rate = 2*pi
g = np.tan(wc/2)

#init plots
fig, ax1 = plt.subplots(2)

for i in res:

    # Digital Filter
    a = 1 / (1+2*i*g+g**2)
    b = 2*i+g
    c = g
    d = g

    Bd = [K*a+1,K*-2*a+2*(a*b*c+a*c*d-1),K*a+(2*a*c*d-2*a*b*c+1)]
    Ad = [1,2*(a*b*c+a*c*d-1),(2*a*c*d-2*a*b*c+1)]

    # Sampling frequency = 2*pi
    w, h = signal.freqz(Bd, Ad, worN=4096, fs=2*np.pi)
    ax1[0].plot(w, 20 * np.log10(abs(h)))

    # Calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles)

    # Analog filter
    b = [K+1,2*i*wc,wc*wc]
    a = [1,2*i*wc,wc*wc]

    w, h = signal.freqs(b, a, worN=np.linspace(0,np.pi,4096))
    ax1[0].plot(w, 20 * np.log10(abs(h)), linestyle='dashed')

    # calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles, linestyle='dashed')

    #Plot -3dB lines
    ax1[0].axvline(x = wc, ymin = 0, ymax = 1, color='black', linestyle='dashed')

ax1[0].set_ylim(-20,16)
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
