import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

res = [3.9,3.2,1.6,0.8,0.4]
wc = 0.1

#init plots
fig, ax1 = plt.subplots(2)

for k in res:

    #Digital filter
    g = np.tan(wc/2)
    G = g/(1+g)

    a = (g**3) / ((1+g)**4)
    b = (g**2) / ((1+g)**3)
    c = (g   ) / ((1+g)**2)
    d = (1   ) / ((1+g)   )

    a0 = 1 /(1+k*G**4)
    coef1 = (1+k)*a0*G**4
    coef2 = (16*a*a0*G**4*k - 24*a*a0*G**3*k + 12*a*a0*G**2*k - 2*a*a0*G*k    + 8*a0*b*G**4*k - 8*a0*b*G**3*k + 2*a0*b*G**2*k + 4*a0*c*G**4*k - 2*a0*c*G**3*k + 2*a0*d*G**4*k + 16*G**4 - 32*G**3 + 24*G**2 - 8*G + 1)
    coef3 = (24*a*a0*G**3*k - 24*a*a0*G**2*k + 6*a*a0*G*k     + 8*a0*b*G**4*k - 2*a0*b*G**2*k + 8*a0*c*G**4*k - 2*a0*c*G**3*k + 6*a0*d*G**4*k + 32*G**3 - 48*G**2 + 24*G - 4)
    coef4 = (12*a*a0*G**2*k - 6*a*a0*G*k     + 8*a0*b*G**3*k  - 2*a0*b*G**2*k + 4*a0*c*G**4*k + 2*a0*c*G**3*k + 6*a0*d*G**4*k + 24*G**2 - 24*G + 6)
    coef5 = (2*a*a0*G*k     + 2*a0*b*G**2*k  + 2*a0*c*G**3*k  + 2*a0*d*G**4*k + 8*G - 4 )

    Bd = [coef1,4*coef1,6*coef1,4*coef1,coef1]
    Ad = [1,coef5,coef4,coef3,coef2]

    # Sampling frequency = 2*pi
    w, h = signal.freqz(Bd, Ad, worN=8192, fs=2*np.pi)
    ax1[0].plot(w, 20 * np.log10(abs(h)))

    # calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles)

    # Analog filter
    b = [wc*wc*wc*wc*(1+k)]
    a = [1,4*wc,6*wc*wc,4*wc*wc*wc,wc*wc*wc*wc*(1+k)]

    w, h = signal.freqs(b, a, worN=np.linspace(0,np.pi,8192))
    ax1[0].plot(w, 20 * np.log10(abs(h)), linestyle='dashed',label=f'{k}')

    # calculate the phase
    angles = np.angle(h)
    ax1[1].plot(w, angles, linestyle='dashed')

    #Plot -3dB lines
    ax1[0].axvline(x = wc, ymin = 0, ymax = 1, color='black', linestyle='dashed')

ax1[0].set_ylim(-40,38)
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
