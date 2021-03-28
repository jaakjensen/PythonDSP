import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

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

#set up the graphs
fig, axes = plt.subplots()

#only grab the first 20-40 msecs
out = data[int(fs*0.0222):int(fs*0.035)]
temp = time1[int(fs*0.0222):int(fs*0.035)]

#plot the original waveform
axes.plot(temp, out)
axes.set_xlabel("Time [s]")
axes.set_ylabel("Amplitude")

print(samplelength)

print("Processing complete")

plt.show()

