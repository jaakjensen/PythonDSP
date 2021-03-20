
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav


########################################################################################
########################################################################################


def fbcfNoMod(inputsignal, audioBuffer, fs, n, delay, fbGain):
    
    #Determine indexes for circular buffer
    bufferLength = len(audioBuffer)
    indexC = ( n % bufferLength )               #Current index
    indexD = ( ( n - delay) % bufferLength )    #Delay index

    out = audioBuffer[int(indexD)]

    audioBuffer[int(indexC)] = inputsignal + fbGain*audioBuffer[int(indexD)]

    return out, audioBuffer


def fbcf(inputsignal, audioBuffer, fs, n, delay, fbGain, amp, rate):
    
    #Calculate current time in seconds for the current sample
    t = n/fs
    fracDelay = amp * np.sin(2*np.pi*rate*t);
    intDelay = np.floor(fracDelay);
    frac = fracDelay - intDelay

    #Determine indexes for circular buffer
    bufferLength = len(audioBuffer)
    indexC = ( n % bufferLength )                               #Current index
    indexD = ( ( n - delay + intDelay) % bufferLength )         #Delay index
    indexF = ( ( n - delay + intDelay + 1 ) % bufferLength )    #Fractional index

    out = (1 - frac) * audioBuffer[int(indexD)] + (frac) *  audioBuffer[int(indexF)]

    audioBuffer[int(indexC)] = inputsignal + fbGain*out

    return out, audioBuffer

########################################################################################
########################################################################################

#NOTE: MUST BE 16-bit wav file. 48khz is OK.
wav_fname = 'dspfiles/AfroCuban.wav'

fs, inputsignal = wav.read(wav_fname)

Ts = 1/fs

timelength = inputsignal.shape[0] / fs
samplelength = inputsignal.shape[0]

print(f"timelength = {timelength}s")

# Divide audio signal by max int value for signed 16 bit number
inputsignal = inputsignal/np.iinfo(np.int16).max

#Set up the time axis for the waveform
time = np.linspace(0, timelength, inputsignal.shape[0])

#Initialize the delay buffer
maxDelay = np.ceil(0.07*fs) #maximum delay of 50msecs

#Create a buffer filled with zeros 
audioBuffer1 = np.zeros(int(maxDelay))
audioBuffer2 = np.zeros(int(maxDelay))

#40msecs of delay
d1 = np.fix(0.042*fs)
d2 = np.fix(0.053*fs)

#Feedback gain value
g1 = 0.5
g2 = -0.5

#LFO rate in Hz
rate1 = 0.6
rate2 = 0.5

#Range of +/- 6 samples for modulation delay
amp1 = 6
amp2 = 8

#initialize output signal
out = np.zeros(samplelength)
w = np.zeros(samplelength)

#Run the function through all the samples
for n in range(0,samplelength):

    #Use FBCF with modulation
    w, audioBuffer1 = fbcf(inputsignal[n,0], audioBuffer1, fs, n, d1, g1, amp1, rate1)

    #Use FBCF with modulation
    out[n], audioBuffer2 = fbcf(w, audioBuffer2, fs, n, d2, g2, amp2, rate2)

print("DSP complete")

#set up the graphs
#fig, axes = plt.subplots(nrows=2,ncols=1)

#plot the original waveform
#axes[0].plot(time, inputsignal, label="Original Audio Signal")
#axes[0].set_xlabel("Time [s]")
#axes[0].set_ylabel("Amplitude")
#axes[0].legend(loc= 7)
#axes[0].set_xlim([0,1])

#plot the original waveform
#axes[1].plot(time, out, label="Processed Audio Signal")
#axes[1].set_xlabel("Time [s]")
#axes[1].set_ylabel("Amplitude")
#axes[1].legend(loc= 7)
#axes[1].set_xlim([0,1])

#Normalize the audio output level to max output
amplitude = np.iinfo(np.int16).max - 10
out = out*amplitude

#Truncate any non-integer/fractional data
#If we don't do this, the wav file won't be readable
out = np.asarray(out, dtype = np.int16)

#Write the data to an output file
wav.write("dspfiles/outputfiles/fbcf_series_example.wav", 48000, out)

print("Wav file written")

#plt.show()

