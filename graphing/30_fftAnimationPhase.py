# Use this animation to show that the
# bin reaches its peak when the input
# signal reaches the bin frequency.
# When you're between bin frequencies,
# the energy spills between adjacent bins
# and the amplitude of the two adjacent
# bins is lower.
from scipy.fft import fft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import hann
import sys

# Number of sample points
N1 = 1024
# sample spacing
Fs = 48000
T = 1.0 / Fs
#X axis
x1 = np.linspace(0.0, N1*T, N1, endpoint=False)
#Signal
oscFrequency = 2000
oscPhase = 0
#Window
w1 = hann(N1)
# Used to calculate bins
# We only grab the first half of the bins
# because we don't need the negative frequencies
xf1 = np.arange(0,Fs/2,Fs/N1)
print(xf1)

def on_press(event):
    sys.stdout.flush()
    keyPressed = event.key
    global oscFrequency
    global oscPhase
    
    if keyPressed == 'l':
        oscPhase = oscPhase + np.pi/16

    if keyPressed == 'k':
        oscPhase = oscPhase - np.pi/16

    #signal
    y1 = np.cos(2.0*np.pi*x1*oscFrequency + oscPhase)
    #FFT of signal with window
    ywf1 = fft(y1*w1)
    #grab X and Y values
    x_vals = xf1[0:int(N1/2)]
    y_vals = 2.0/N1 * np.abs(ywf1[0:int(N1/2)])
    #clear plot (aka clear axis)
    ax.cla()
    #fill plot
    ax.plot(x_vals[30:50], y_vals[30:50], '-r',marker="o")
    ax.legend([f'Phase = {oscPhase}'])

#init plots
fig, ax = plt.subplots()
fig.canvas.mpl_connect('key_press_event', on_press)

#signal - print once
y1 = np.cos(2.0*np.pi*x1*oscFrequency)
#FFT of signal with window
ywf1 = fft(y1*w1)
#grab X and Y values
x_vals = xf1[0:int(N1/2)]
y_vals = 2.0/N1 * np.abs(ywf1[0:int(N1/2)])
#clear plot (aka clear axis)
ax.cla()
#fill plot
ax.plot(x_vals[30:50], y_vals[30:50], '-r',marker="o")
ax.legend([f'Phase = {oscPhase}'])

plt.tight_layout()
plt.show()
