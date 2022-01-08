# Use this code to pitch shift an audio signal
# using the STFT.
from scipy.fft import fft, ifft, fftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.signal import hann
from scipy.signal import sawtooth
import sys
import scipy.io.wavfile as wav
from tqdm import tqdm

#suppress the sometimes-annoying sci-notation
np.set_printoptions(suppress=True,threshold=np.inf)

# Number of sample points in FFT
N = 1024

# How much to pitch shift? (2 = 2x, aka an octave)
semitones = 12
pitchShiftRatio = 2**(semitones/12)

# HopSize
hopSize = int(N/8)

# Read input wav file
#NOTE: MUST BE 16-bit wav file. 48khz is OK.
#wav_fname = 'dspfiles/BibioGuitar.wav'
#wav_fname = 'dspfiles/GrandPiano.wav'
#wav_fname = 'dspfiles/FenderRhodes.wav'
wav_fname = 'dspfiles/Voice.wav'


Fs, inputsignal = wav.read(wav_fname)
Ts = 1/Fs

# Number of samples in audio file
# Drops some of the samples at the end if it isn't divisible by FFT size
numSamples = int(inputsignal.shape[0]-inputsignal.shape[0]%N)

# Determine #of FFT frames
frames = int(numSamples / hopSize)
timelength = numSamples / Fs

# Divide audio signal by max int value for signed 16 bit number
# Discard the right channel of audio, only keep the left
y1 = inputsignal[0:numSamples,0]/(np.iinfo(np.int16).max)

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

    global y1

    # For merging all frames at the end
    outSignalsMerged = np.zeros(frames*hopSize+N,dtype=complex)

    #For holding input and output phases between frames
    lastInputPhase = np.zeros(int(N/2))
    lastOutputPhase = np.zeros(int(N/2))

    for hop in tqdm(range(0,frames-10)):
        
        #FFT of signal with window
        try:
            ywf = fft(y1[hop*hopSize:hop*hopSize+N]*w1)
        except:
            print(hop)
            print(hopSize)
            print(N)

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


        for g in range(hop*hopSize,hop*hopSize+N):
            outSignalsMerged[g] += 0.5*outSignal[g-hop*hopSize]


    
    #Normalize the audio output level to max output
    amplitudeOut = np.iinfo(np.int16).max - 3000
    audOut = outSignalsMerged.real * amplitudeOut

    #Truncate any non-integer/fractional data
    #If we don't do this, the wav file won't be readable
    audOut = np.asarray(audOut, dtype = np.int16)

    #Write the data to an output file
    wav.write("dspfiles/outputfiles/fftPitchShiftedSignal.wav", 48000, audOut)

    print("Wav file written")


FFTPitchShift();
