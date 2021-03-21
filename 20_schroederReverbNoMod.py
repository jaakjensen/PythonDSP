
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

#########################################################################
#########################################################################

def apf(inputsignal, audioBuffer, fs, n, delay, gain, amp, rate):
    
    #Calculate current time in seconds for the current sample
    t = n/fs
    frac = 0
    intDelay = 0
    fracDelay = 0

    #Determine indexes for circular buffer
    bufferLength = len(audioBuffer)
    indexC = ( n % bufferLength )                               #Current index
    indexD = ( ( n - delay + intDelay) % bufferLength )         #Delay index
    indexF = ( ( n - delay + intDelay + 1 ) % bufferLength )    #Fractional index

    #Temp variable for output of delay buffer
    w = (1 - frac) * audioBuffer[int(indexD)] + (frac) *  audioBuffer[int(indexF)]

    #Temp variable used for the node after the input sum
    v = inputsignal - ( gain * w )

    # Summation at output
    out = ( gain * v ) + w

    # Store the current input to delay buffer
    audioBuffer[int(indexC)] = v 

    return out, audioBuffer


def fbcf(inputsignal, audioBuffer, fs, n, delay, fbGain, amp, rate):
    
    #Calculate current time in seconds for the current sample
    t = n/fs
    frac = 0
    intDelay = 0
    fracDelay = 0

    #Determine indexes for circular buffer
    bufferLength = len(audioBuffer)
    indexC = ( n % bufferLength )                               #Current index
    indexD = ( ( n - delay + intDelay) % bufferLength )         #Delay index
    indexF = ( ( n - delay + intDelay + 1 ) % bufferLength )    #Fractional index

    out = (1 - frac) * audioBuffer[int(indexD)] + (frac) *  audioBuffer[int(indexF)]

    audioBuffer[int(indexC)] = inputsignal + fbGain*out

    return out, audioBuffer


#########################################################################
#########################################################################

#NOTE: MUST BE 16-bit wav file. 48khz is OK.
#wav_fname = 'dspfiles/AfroCuban.wav'
#wav_fname = 'dspfiles/Harpsichord.wav'
#wav_fname = 'dspfiles/VitaminC.wav'
wav_fname = 'dspfiles/Flashy808.wav'


fs, inputsignal = wav.read(wav_fname)

Ts = 1/fs

timelength = inputsignal.shape[0] / fs
samplelength = inputsignal.shape[0]

print(f"Sample Length = {timelength}s")

# Divide audio signal by max int value for signed 16 bit number
inputsignal = inputsignal/np.iinfo(np.int16).max

#Set up the time axis for the waveform
time = np.linspace(0, timelength, inputsignal.shape[0])

#Initialize the delay buffer
maxDelay = np.ceil(0.07*fs) #maximum delay of 70msecs

#Create a buffer filled with zeros 
audioBuffer1 = np.zeros(int(maxDelay))
audioBuffer2 = np.zeros(int(maxDelay))
audioBuffer3 = np.zeros(int(maxDelay))
audioBuffer4 = np.zeros(int(maxDelay))
audioBuffer5 = np.zeros(int(maxDelay))
audioBuffer6 = np.zeros(int(maxDelay))

#msecs of delay
d1 = np.fix(0.0297*fs)
d2 = np.fix(0.0371*fs)
d3 = np.fix(0.0411*fs)
d4 = np.fix(0.0437*fs)
d5 = np.fix(0.005*fs)
d6 = np.fix(0.0017*fs)

#Gain value for feedforward and feedback paths
g1 = 0.95
g2 = -0.95
g3 = 0.95
g4 = -0.95
g5 = 0.9
g6 = 0.9

#LFO rate in Hz
rate1 = 0.6
rate2 = 0.71
rate3 = 0.83
rate4 = 0.95
rate5 = 1.07 
rate6 = 1.19

#Range of +/- samples for modulation delay
amp1 = 8
amp2 = 8
amp3 = 8
amp4 = 8
amp5 = 8
amp6 = 8

#initialize output signal
out = np.zeros(samplelength)

#Run the function through all the samples
for n in range(0,samplelength):

    # Four parallel FBCF
    w1, audioBuffer1 = fbcf(inputsignal[n,0], audioBuffer1, fs, n, d1, g1, amp1, rate1)
    w2, audioBuffer2 = fbcf(inputsignal[n,0], audioBuffer2, fs, n, d2, g2, amp2, rate2)
    w3, audioBuffer3 = fbcf(inputsignal[n,0], audioBuffer3, fs, n, d3, g3, amp3, rate3)
    w4, audioBuffer4 = fbcf(inputsignal[n,0], audioBuffer4, fs, n, d4, g4, amp4, rate4)

    # Combine parallel paths
    combPar = 0.25 * (w1 + w2 + w3 + w4)

    # Two series all-pass filters
    w5, audioBuffer5 = apf(combPar, audioBuffer5, fs, n, d1, g5, amp5, rate5)
    out[n], audioBuffer6 = apf(w5, audioBuffer6, fs, n, d2, g6, amp6, rate6)


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
wav.write("dspfiles/outputfiles/schroederReverbNoMod.wav", 48000, out)

print("Wav file written")

#plt.show()

