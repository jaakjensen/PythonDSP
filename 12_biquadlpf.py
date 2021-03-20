
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

######################################################################
######################################################################
######################################################################

#Transposed Direct Form II Biquad LPF Implementation

def biquadLPF(inputsig, Fs, cutoff, Q, dBGain):

    #Initial parameters
    N = len(inputsig)
    out = np.zeros(N)

    #Intermediate variables
    w0 = 2*np.pi*cutoff/Fs          # Angular freq. (radians/sample)
    alpha = np.sin(w0)/(2*Q)        #Filter width
    A = np.sqrt(10^(dBGain/20))     #Amplitude
    
    #Filter coefficients
    b0 = (1- np.cos(w0))/2
    b1 = 1- np.cos(w0)
    b2 = (1- np.cos(w0))/2
    a0 = 1 + alpha
    a1 = -2*cos(w0)
    a2 = 1-alpha

    #Transposed direct form II implementation
    d1 = 0
    d2 = 0

    for n in range(0,N-1)
        out[n] = (b0/a0)*inputsig[n] + d1
        d1 = (b1/a0)*inputsig[n] - (a1/a0)*out[n] + d2
        d2 = (b2/a0)*inputsig[n] - (a2/a0)*out[n]

    return out[n]

######################################################################
######################################################################
######################################################################


#Load and initialize the audio
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






#set up the output graph
fig = plt.figure(figsize=(10,4), dpi=100)

ax = fig.add_axes([0.1,0.1,0.8,0.8])

#plot the original waveform
ax.plot(time, data, label="Original Audio Signal")
#plot the synthesized sine waveform
ax.plot(time, data2, label="Filtered Signal")
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
