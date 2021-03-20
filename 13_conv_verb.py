
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal

#wet or dry mix from 0 to 1
wet_dry = 1

#Setup for impulse response:
wav_fname1 = 'dspfiles/Flashy808.wav'
fs1, data1 = wav.read(wav_fname1)
Ts1 = 1/fs1
timelength1 = data1.shape[0] / fs1
samplelength1 = data1.shape[0]
print(f"Reverb File Time = {timelength1}s")
# Divide audio signal by max int value for signed 16 bit number
data1 = data1/np.iinfo(np.int16).max
#Set up the time axis for the original waveform
time1 = np.linspace(0, timelength1, data1.shape[0])


#Setup for audio file:
wav_fname2 = 'dspfiles/tapestester.wav'
fs2, data2 = wav.read(wav_fname2)
Ts2 = 1/fs2
timelength2 = data2.shape[0] / fs2
samplelength2 = data2.shape[0]
print(f"Audio File Time = {timelength2}s")
# Divide audio signal by max int value for signed 16 bit number
data2 = data2/np.iinfo(np.int16).max
#Set up the time axis for the original waveform
time2 = np.linspace(0, timelength2, data2.shape[0])


#initialize output signal
out = signal.fftconvolve(data2[:,0]*0.5, data1[:,0]*0.5, mode='full')
#Set up the time axis for the new waveform
time3 = np.linspace(0, len(out)/fs2, len(out))


#set up the graphs
fig, axes = plt.subplots(nrows=3,ncols=1)

#plot the original waveform
axes[0].plot(time1, data1)
axes[0].set_xlabel("Time [s]")
axes[0].set_ylabel("Amplitude")
#axes[0].set_xlim([2,5])


axes[1].plot(time2, data2)
axes[1].set_xlabel("Time [s]")
axes[1].set_ylabel("Amplitude")
#axes[1].set_xlim([2,5])

axes[2].plot(time3, out, label = "Convolved Output")
axes[2].set_xlabel("Time [s]")
axes[2].set_ylabel("Amplitude")
axes[2].legend(loc= 7)
#axes[1].set_xlim([2,5])

#Normalize the audio output level to max output
amplitude = np.iinfo(np.int16).max
out = out*amplitude

#Truncate any non-integer/fractional data
#If we don't do this, the wav file won't be readable
out = np.asarray(out, dtype = np.int16)

#Write the data to an output file
wav.write("dspfiles/outputfiles/fostex_fftconv.wav", fs2, out)

print("Processing complete")

plt.show()

