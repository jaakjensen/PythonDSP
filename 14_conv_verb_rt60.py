import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

###############################################################################
###############################################################################

def convolutionReverb ():
    return 0

###############################################################################
###############################################################################

#Main program section

###############################################################################
###############################################################################

wav_fname = 'dspfiles/fostex16_441.wav'

fs, data = wav.read(wav_fname)

Ts = 1/fs

timelength = data.shape[0] / fs

samplelength = data.shape[0]

print(f"timelength = {timelength}s")

# Divide audio signal by max int value for signed 16 bit number
data = data/np.iinfo(np.int16).max

#Set up the time axis for the original waveform
time1 = np.linspace(0, timelength, data.shape[0])

#initialize output signal
out = data[:131072]

#Set up the time axis for the new waveform
time2 = np.linspace(0, len(out)/fs, len(out))

#set up the graphs
fig, axes = plt.subplots(nrows=2,ncols=1)


#plot the original waveform
axes[0].plot(time1, 20*np.log10(abs(data)))
axes[0].plot([0,5],[-60,-60],'k-')
axes[0].set_xlabel("Time [s]")
axes[0].set_ylabel("Amplitude")
#axes[0].set_xlim([2,5])

axes[1].plot(time2, 20*np.log10(abs(out)))
axes[1].set_xlabel("Time [s]")
axes[1].set_ylabel("Amplitude")
#axes[1].set_xlim([2,5])

print(samplelength)

#Normalize the audio output level to max output
amplitude = np.iinfo(np.int16).max - 10
out = out*amplitude

#Truncate any non-integer/fractional data
#If we don't do this, the wav file won't be readable
out = np.asarray(out, dtype = np.int16)

#Write the data to an output file
wav.write("dspfiles/outputfiles/fostex16_441_3secs.wav", fs, out)

print("Processing complete")

plt.show()

