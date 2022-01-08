# Use this animation to calculate the exact
# frequency of a signal in a bin.
# Press 'k' and 'l' keys to raise and lower
# the frequency of the cosine wave.
from scipy.fft import fft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import hann
from scipy.signal import sawtooth
import sys

# Number of sample points
N = 1024
# Amount of overlap
overlap = int(N/2)
# sample spacing
Fs = 48000
T = 1.0 / Fs
#X axis - start, stop, # sample points
#don't grab the end point
x1 = np.linspace(0.0, (N+overlap)*T, N+overlap, endpoint=False)
#Signal
oscFrequency = 2000
#Window
w1 = hann(N)
# Used to calculate bins
# We only grab the first half of the bins (Fs/2)
# because we don't need the negative frequencies
xf1 = np.arange(0,Fs/2,Fs/N)

#function used for replotting if frequency is changed
def on_press(event):
    sys.stdout.flush()
    keyPressed = event.key
    global oscFrequency
    if keyPressed == 'l':
        oscFrequency = oscFrequency + 0.25
    if keyPressed == 'k':
        oscFrequency = oscFrequency - 0.25
    calculateFreqWithFFT();

#function used for calculating FFT
def calculateFreqWithFFT():
    #signals - cos
    y1 = np.cos(2.0*np.pi*x1*oscFrequency)
    #y1 = sawtooth(2.0*np.pi*x1*oscFrequency)
    #FFT of signals with window
    ywf1 = fft(y1[0:N]*w1)
    ywf2 = fft(y1[overlap:overlap+N]*w1)
    # COSINE SIGNAL #
    #grab X and Y values for first FFT
    x_vals1 = xf1[0:int(N/2)]
    y_vals1 = 2.0/N * np.abs(ywf1[0:int(N/2)])
    #Grab bin with largest peak (not the greatest approach):
    maxValue = np.max(y_vals1)
    binNum = 0
    for i in y_vals1:
        if(i == maxValue):
            break
        else:
            binNum+=1
    #grab x and y values for second FFT
    x_vals2 = xf1[0:int(N/2)]
    y_vals2 = 2.0/N * np.abs(ywf2[0:int(N/2)])
    #grab phase values from both FFTs
    phase1 = np.arctan2(ywf1[0:int(N/2)].imag, ywf1[0:int(N/2)].real)
    phase2 = np.arctan2(ywf2[0:int(N/2)].imag, ywf2[0:int(N/2)].real)
    # unwrap the phase -> I don't think you have to do this step
    #phase1 = np.unwrap(phase1)
    #phase2 = np.unwrap(phase2)
    #take the difference
    phaseDifference = phase2 - phase1
    #calculate phase remainder
    phaseRemainder = phaseDifference - 2*np.pi*xf1*overlap/Fs
    #re-wrap the phase to -pi to pi
    phaseRemainder = np.arctan2(np.sin(phaseRemainder), np.cos(phaseRemainder))
    angFreq = (phaseRemainder/overlap) + 2*np.pi*xf1/Fs
    measuredFreq = angFreq*Fs/(2*np.pi)
    #clear plot (aka clear axis)
    ax[0].cla()
    ax[1].cla()
    #plot data
    ax[0].plot(x_vals1[binNum-5:binNum+5], y_vals1[binNum-5:binNum+5], '-b',marker="o")
    ax[0].plot(x_vals2[binNum-5:binNum+5], y_vals2[binNum-5:binNum+5], '-r',marker="o")
    #ax[0].plot(x_vals1[0:int(N/2)], y_vals1[0:int(N/2)], '-b',marker="o")
    #ax[0].plot(x_vals2[0:int(N/2)], y_vals2[0:int(N/2)], '-r',marker="o")

    ax[0].set_ylabel('Amplitude')
    ax[0].set_xlabel('Frequency (Hz)')
    #plot signals
    ax[1].plot(x1[0:N], y1[0:N], '-b',marker="o",linewidth=3)
    ax[1].plot(x1[overlap:overlap+N], y1[overlap:overlap+N], '-r',marker="o")
    ax[1].set_ylabel('Amplitude')
    ax[1].set_xlabel('Time (sec)')
    #add legend and plot
    ax[0].legend([f'Bin {binNum}, Expected: {oscFrequency}, Measured: {round(measuredFreq[binNum],5)}, Error:{round(oscFrequency-measuredFreq[binNum],5)}'])

fig, ax = plt.subplots(2)
fig.canvas.mpl_connect('key_press_event', on_press)
calculateFreqWithFFT();

plt.tight_layout()
plt.show()
