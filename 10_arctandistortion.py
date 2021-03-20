
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav




def arcTanSaturation(inputsig, gain):

    #Saturate the output signal using ArcTan clipping
    out = (2/np.pi)*np.arctan(gain*inputsig)
    return out

wav_fname = 'textbookcode/Ch_03/sw440hz.wav'

fs, data = wav.read(wav_fname)

length = data.shape[0] / fs
samplelength = data.shape[0]

print(f"length = {length}s")

# Divide audio signal by max int value for signed 16 bit number
data = data/np.iinfo(np.int16).max

#Set up the time axis for the waveform
time = np.linspace(0, length, data.shape[0])

#initialize output signal
data2 = np.zeros(samplelength)

#define the gain parameter (only use a value from 0 to 1)
gain = 5

#Run the data through ArcTan function
for n in range(0,samplelength):
    data2[n] = arcTanSaturation(data[n], gain)

#set up the graph
fig = plt.figure(figsize=(10,4), dpi=100)

ax = fig.add_axes([0.1,0.1,0.8,0.8])

#plot the original waveform
ax.plot(time, data, label="Original Audio Signal")
#plot the synthesized sine waveform
ax.plot(time, data2, label="Saturated Signal")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Amplitude")
ax.legend(loc= 7)
ax.set_xlim([0,0.02])


#Normalize the audio output level to max output
amplitude = np.iinfo(np.int16).max
data2 = data2*amplitude

#Truncate any non-integer/fractional data
#If we don't do this, the wav file won't be readable
data2 = np.asarray(data2, dtype = np.int16)

#Write the data to an output file
wav.write("textbookcode/Ch_03/sw440hz_modulated.wav", 44100, data2)

plt.show()

