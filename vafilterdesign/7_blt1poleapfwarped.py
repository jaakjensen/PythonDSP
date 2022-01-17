import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#for this particular example, ignore div/0 
#in the np.log10 expression
np.seterr(divide = 'ignore') 

plotpoints = [0.02,0.1,1,2.5]

#init plots
fig, ax1 = plt.subplots(2)

# 1 sample delay: y[n] = beta * x[n] + alpha * y[n-1]
for i in plotpoints:
    bA = i
    aA = 1-bA

    g = np.tan(i/2)
    alpha = g/(1+g)

    bd = [(2*alpha-1),1]        #--->Compute BLT coefficients
    ad = [1, (2*alpha - 1)]     #--->Compute BLT coefficients

    # Sampling frequency = 2*pi
    w, h = signal.freqz(bd, ad, worN=4096, fs=2*np.pi)
    ax1[0].plot(w, 20 * np.log10(abs(h)))

    # calculate the phase
    angles = np.angle(h)
    # Convert from radians to degrees:
    angles = ( angles * 180 ) / np.pi
    ax1[1].plot(w, angles)


ax1[0].set_ylim(-24,6)
ax1[0].set_ylabel('Magnitude [dB]', color='b')
ax1[0].set_xscale('log')
ax1[0].set_xlim(0.001,np.pi)
ax1[0].set_title('Digital filter frequency response')
ax1[1].set_ylabel('Phase (degrees)', color='g')
ax1[1].set_xlabel('Frequency [rad/sample]')
ax1[1].set_xscale('log')
ax1[1].set_xlim(0.001,np.pi)
ax1[1].grid()
plt.show()
