
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

#########################################################################
#########################################################################


def modDelay(inputsignal, audioBuffer, fs, n, delay, amp, rate):
    
    #Calculate current time in seconds for the current sample
    t = n/fs
    fracDelay = amp * np.sin(2*np.pi*rate*t)
    intDelay = np.floor(fracDelay)
    frac = fracDelay - intDelay

    #Determine indexes for circular buffer
    bufferLength = len(audioBuffer)
    indexC = ( n % bufferLength )                               #Current index
    indexD = ( ( n - delay + intDelay) % bufferLength )         #Delay index
    indexF = ( ( n - delay + intDelay + 1 ) % bufferLength )    #Fractional index

    out = (1 - frac) * audioBuffer[int(indexD)] + (frac) *  audioBuffer[int(indexF)]

    # store the current output in appropriate index
    audioBuffer[int(indexC)] = inputsignal

    return out, audioBuffer


#########################################################################
#########################################################################

#NOTE: MUST BE 16-bit wav file. 48khz is OK.
#wav_fname = 'dspfiles/AfroCuban.wav'
#wav_fname = 'dspfiles/Harpsichord.wav'
#wav_fname = 'dspfiles/VitaminC.wav'
#wav_fname = 'dspfiles/Flashy808.wav'
#wav_fname = 'dspfiles/GrandPiano.wav'
wav_fname = 'dspfiles/GrandPiano30sec.wav'

fs, inputsignal = wav.read(wav_fname)

Ts = 1/fs

timelength = inputsignal.shape[0] / fs
samplelength = inputsignal.shape[0]

print(f"Sample Length = {timelength}s")

# Divide audio signal by max int value for signed 16 bit number
inputsignal = inputsignal/(np.iinfo(np.int16).max)

#Set up the time axis for the waveform
time = np.linspace(0, timelength, inputsignal.shape[0])

#Initialize the delay buffer
maxDelay = np.ceil(0.07*fs) #maximum delay of 70msecs

#Create a buffer filled with zeros 
audioBuffer1 = np.zeros(int(maxDelay)-1)
audioBuffer2 = np.zeros(int(maxDelay)-1)
audioBuffer3 = np.zeros(int(maxDelay)-1)
audioBuffer4 = np.zeros(int(maxDelay)-1)

#msecs of delay
d1 = np.fix(0.0297*fs)
d2 = np.fix(0.0371*fs)
d3 = np.fix(0.0411*fs)
d4 = np.fix(0.0437*fs)

#Gain value for feedforward and feedback paths
g11 = 0
g12 = 1
g13 = 1
g14 = 0

g21 = -1
g22 = 0
g23 = 0
g24 = -1

g31 = 1
g32 = 0
g33 = 0
g34 = -1

g41 = 0
g42 = 1
g43 = -1
g44 = 0

#LFO rate in Hz
rate1 = 0.6
rate2 = 0.71
rate3 = 0.83
rate4 = 0.95 

#Range of +/- samples for modulation delay
amp1 = 10
amp2 = 10
amp3 = 10
amp4 = 10

#initialize output signal
out = np.zeros(samplelength)

#init fb variables
fb1 = 0
fb2 = 0
fb3 = 0
fb4 = 0

#global gain to control reverb time
g = 0.69

#Run the function through all the samples
for n in range(0,samplelength):

    # Combine input with feedback for respective delay lines
    inDL1 = inputsignal[n,0] + fb1
    inDL2 = inputsignal[n,0] + fb2
    inDL3 = inputsignal[n,0] + fb3
    inDL4 = inputsignal[n,0] + fb4

    # Four parallel delay lines
    outDL1, audioBuffer1 = modDelay(inDL1, audioBuffer1, fs, n, d1, amp1, rate1)
    outDL2, audioBuffer2 = modDelay(inDL2, audioBuffer2, fs, n, d2, amp2, rate2)
    outDL3, audioBuffer3 = modDelay(inDL3, audioBuffer3, fs, n, d3, amp3, rate3)
    outDL4, audioBuffer4 = modDelay(inDL4, audioBuffer4, fs, n, d4, amp4, rate4)

    # Combine parallel paths
    out[n] = 0.25 * (outDL1 + outDL2 + outDL3 + outDL4)

    # Calculate feedback (including crossover)
    fb1 = g * (g11 * outDL1 + g21 * outDL2 + g31 * outDL3 + g41 * outDL4)
    fb2 = g * (g12 * outDL1 + g22 * outDL2 + g32 * outDL3 + g42 * outDL4)
    fb3 = g * (g13 * outDL1 + g23 * outDL2 + g33 * outDL3 + g43 * outDL4)
    fb4 = g * (g14 * outDL1 + g24 * outDL2 + g34 * outDL3 + g44 * outDL4)

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
wav.write("dspfiles/outputfiles/fdn4by4.wav", 48000, out)

print("Wav file written")

#plt.show()

