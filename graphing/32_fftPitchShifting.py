# Use this code to pitch shift an audio signal
# using the STFT.
from scipy.fft import fft, ifft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import hann
from scipy.signal import sawtooth
import sys
#suppress the sometimes-annoying sci-notation
np.set_printoptions(suppress=True,threshold=np.inf)
# Number of sample points
N = 1024
# How much to pitch shift? (2 = 2x, aka an octave)
pitchShiftRatio = 2
# HopSize
hopSize = int(N/8)
# How many overlaps should we calculate?
frames = 15
# sample spacing
Fs = 48000
T = 1.0 / Fs
#X axis - start, stop, # sample points
#don't grab the end point
x1 = np.linspace(0.0, (N+frames*hopSize)*T, N+frames*hopSize, endpoint=False)
#Signal
oscFrequency = 1968.75
#Window
w1 = hann(N)
# Used to calculate bins (non-angular frequency)
# We only grab the first half of the bins (Fs/2)
# because we don't need the negative frequencies
fftBins = np.arange(0,Fs/2,Fs/N)

#Grab X Vals (aka real bins)
xvals = fftBins[0:int(N/2)]

#function used for calculating FFT
def FFTPitchShift():
    #signals - cos
    y1 = np.cos(2.0*np.pi*x1*oscFrequency)

    # For merging all frames at the end
    outSignalsMerged = np.zeros(frames*hopSize+N,dtype=complex)

    #For holding input and output phases between frames
    lastInputPhase = np.zeros(int(N/2))
    lastOutputPhase = np.zeros(int(N/2))

    for hop in range(0,frames):
        #FFT of signal with window
        ywf = fft(y1[hop*hopSize:hop*hopSize+N]*w1)
        
        #grab Y values for FFTs
        y_vals = np.abs(ywf[0:int(N/2)])
        
        #grab phase values from both FFTs
        currentPhase = np.arctan2(ywf[0:int(N/2)].imag, ywf[0:int(N/2)].real)

        #take the difference -> phase[n] - phase[n-1]
        phaseDifference = currentPhase - lastInputPhase
        
        #save current phase for next frame
        lastInputPhase = currentPhase

        #calculate phase remainder by subtracting the phase shift
        #we'd expect from the center frequency
        aPhaseRemainder = phaseDifference - 2*np.pi*fftBins*hopSize/Fs

        #re-wrap the phase to -pi to pi
        #NOTE: this is not a great method for re-wrapping the phase, but it works
        # It may be ok with LUT based approach for sin and cos
        aPhaseRemainder = np.arctan2(np.sin(aPhaseRemainder), np.cos(aPhaseRemainder))

        # Calculate fractional bin number -> fftBins*N/Fs is the bin
        aFractionalBin = ((aPhaseRemainder*N)/(2*np.pi*hopSize)) + (fftBins*N/Fs)

        #Calculate new bins
        newBins = np.floor(pitchShiftRatio*fftBins*N/Fs + 0.5)

        synthesisAmp = np.zeros(int(N/2))
        synthesisFreqs = np.zeros(int(N/2))

        for i in range(0,int(N/2)):
            if(newBins[i] < N/2):
                synthesisAmp[int(newBins[i])] += y_vals[int(i)]
                synthesisFreqs[int(newBins[i])] = (aFractionalBin[int(i)] * pitchShiftRatio)

        outFFT = np.zeros(N,dtype=complex)
   
        for i in range(0,int(N/2)):
            amplitude = synthesisAmp[i]
            binDeviation = synthesisFreqs[i] - i
            phaseDiff = binDeviation * 2.0 * np.pi * hopSize / N
            phaseDiff += 2.0 * np.pi * i * hopSize / N

            #Wrap phases
            outPhase = np.arctan2(np.sin(phaseDiff+lastOutputPhase[i]), np.cos(phaseDiff+lastOutputPhase[i]))

            lastOutputPhase[i] = outPhase

            outFFT[i] = amplitude*(np.cos(outPhase) + 1j*np.sin(outPhase))

            if(i>0 and i<(N/2)):
                outFFT[N-i] = amplitude*(np.cos(outPhase) - 1j*np.sin(outPhase))

        #Take inverse FFT
        outSignal = ifft(outFFT)

        #Apply Output Window
        outSignal = outSignal*w1

        #plot data of FFT
        ax[0].plot(xvals, np.abs(ywf[0:int(N/2)]), marker="o")
        ax[0].plot(xvals, np.abs(outFFT[0:int(N/2)]), marker="o")

        #plot time domain signals
        #resynthesised output
        ax[1].plot(range(hop*hopSize,hop*hopSize+N), outSignal[0:N].real, marker="o",linewidth=2)

        #original signal
        ax[2].plot(range(hop*hopSize,hop*hopSize+N), y1[hop*hopSize:hop*hopSize+N], marker="o",linewidth=2)

        for g in range(hop*hopSize,hop*hopSize+N):
            outSignalsMerged[g] += 0.5*outSignal[g-hop*hopSize]

    #At the very end, plot time domain signal
    #resynthesised output
    ax[1].plot(range(0,frames*hopSize+N), outSignalsMerged[0:frames*hopSize+N].real, marker="o",linewidth=2)

#init plots
fig, ax = plt.subplots(3)
FFTPitchShift();
plt.tight_layout()
plt.show()
