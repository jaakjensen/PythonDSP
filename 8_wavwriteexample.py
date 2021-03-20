
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

wav_fname = 'textbookcode/Ch_03/sw440hz.wav'

fs, data = wav.read(wav_fname)

length = data.shape[0] / fs

print(f"length = {length}s")

# Divide audio signal by max int value for signed 16 bit number
data = data/np.iinfo(np.int16).max

#Set up the time axis for the waveform
time = np.linspace(0, length, data.shape[0])

#Create a synthesized sine wave of twice the frequency
data2 = np.sin(2*np.pi*44100*880*time)

#AM modulate the original waveform by new wave form
data3 = data2*data

#set up the graphs
fig, axes = plt.subplots(nrows=3,ncols=1)

#plot the original waveform
axes[0].plot(time, data, label="Original Audio Signal")
axes[0].set_xlabel("Time [s]")
axes[0].set_ylabel("Amplitude")
axes[0].legend(loc= 7)
axes[0].set_xlim([0,0.05])

#plot the synthesized sine waveform
axes[1].plot(time, data2, label="Modulation Signal")
axes[1].set_xlabel("Time [s]")
axes[1].set_ylabel("Amplitude")
axes[1].legend(loc= 7)
axes[1].set_xlim([0,0.05])

#plot the original waveform being modulated by new wave form
axes[2].plot(time, data3, label="Modulated Audio Signal")
axes[2].set_xlabel("Time [s]")
axes[2].set_ylabel("Amplitude")
axes[2].legend(loc= 7)
axes[2].set_xlim([0,0.05])

#Normalize the audio output level to max output
amplitude = np.iinfo(np.int16).max
data3 = data3*amplitude

#Truncate any non-integer/fractional data
#If we don't do this, the wav file won't be readable
data3 = np.asarray(data3, dtype = np.int16)

#Write the data to an output file
wav.write("textbookcode/Ch_03/sw440hz_modulated.wav", 44100, data3)

plt.show()


