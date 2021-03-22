
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

#########################################################################
#########################################################################

def apf(inputsignal, audioBuffer, fs, n, delay, gain, amp, rate):
    
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

    #Temp variable for output of delay buffer
    w = (1 - frac) * audioBuffer[int(indexD)] + (frac) *  audioBuffer[int(indexF)]

    #Temp variable used for the node after the input sum
    v = inputsignal - ( gain * w )

    # Summation at output
    out = ( gain * v ) + w

    # Store the current input to delay buffer
    audioBuffer[int(indexC)] = v 

    return out, audioBuffer


def fblpcf(inputsignal, audioBuffer, fs, n, delay, fbGain, amp, rate, fbLPF):
    
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
    # The LPF is created by adding the current output
    # with the previous sample, both are weighted 0.5
    audioBuffer[int(indexC)] = inputsignal + fbGain*( 0.5 * out + 0.5 * fbLPF )
    
    # Store the current output for the feedback LPF
    # to be used with the next sample
    fbLPF = out

    return out, audioBuffer, fbLPF


def earlyReflections(inputsignal, audioBuffer, fs, n):

    # Delay times converted from milliseconds
    delayTimes = [0, 0.01277, 0.01283, 0.01293, 0.01333,
                0.01566, 0.02404, 0.02679, 0.02731, 0.02737, 0.02914,
                0.02920, 0.02981, 0.03389, 0.04518, 0.04522,
                0.04527, 0.05452, 0.06958]

    delayTimes = np.fix( [element * fs for element in delayTimes] )
            
    # There must be a "gain" for each of the "delayTimes"
    gains = [0.8, 0.1526, -0.4097, 0.2984, 0.1553, 0.1442,
            -0.3124, -0.4176, -0.9391, 0.6926, -0.5787, 0.5782,
            0.4206, 0.3958, 0.3450, -0.5361, 0.417, 0.1948, 0.1548]

    #Determine indexes for circular buffer
    bufferLength = len(audioBuffer)
    indexC = ( n % bufferLength ) #Current index
    audioBuffer[int(indexC)] = inputsignal

    #Initialize the output to be used in the loop
    out = 0

    # Loop through all the taps
    for tap in range(0,len(delayTimes)):

        # Find the circular buffer index for the current tap
        indexTDL =  ( ( n - delayTimes[tap] ) % bufferLength )

        # "Tap" the delay line and add current tap with output
        out = out + ( gains[tap] * audioBuffer[int(indexTDL)] )

    return out, audioBuffer

#########################################################################
#########################################################################

#NOTE: MUST BE 16-bit wav file. 48khz is OK.
wav_fname = 'dspfiles/AfroCuban.wav'
#wav_fname = 'dspfiles/Harpsichord.wav'
#wav_fname = 'dspfiles/VitaminC.wav'
#wav_fname = 'dspfiles/Flashy808.wav'


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
audioBufferER = np.zeros(int(maxDelay)-1)
audioBuffer1 = np.zeros(int(maxDelay)-1)
audioBuffer2 = np.zeros(int(maxDelay)-1)
audioBuffer3 = np.zeros(int(maxDelay)-1)
audioBuffer4 = np.zeros(int(maxDelay)-1)
audioBuffer5 = np.zeros(int(maxDelay)-1)
audioBuffer6 = np.zeros(int(maxDelay)-1)

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
g5 = 0.7
g6 = 0.7

#LFO rate in Hz
rate1 = 0.6
rate2 = 0.71
rate3 = 0.83
rate4 = 0.95
rate5 = 1.07 
rate6 = 1.19

#Range of +/- samples for modulation delay
amp1 = 12
amp2 = 12
amp3 = 12
amp4 = 12
amp5 = 12
amp6 = 12

#initialize output signal
out = np.zeros(samplelength)

#init fbLPF variables
fbLPF1 = 0
fbLPF2 = 0
fbLPF3 = 0
fbLPF4 = 0

#Run the function through all the samples
for n in range(0,samplelength):

    # Early reflections TDL
    w0, audioBufferER = earlyReflections(inputsignal[n,0], audioBufferER, fs, n)

    # Four parallel FBCF
    w1, audioBuffer1, fbLPF1 = fblpcf(w0, audioBuffer1, fs, n, d1, g1, amp1, rate1, fbLPF1)
    w2, audioBuffer2, fbLPF2 = fblpcf(w0, audioBuffer2, fs, n, d2, g2, amp2, rate2, fbLPF2)
    w3, audioBuffer3, fbLPF3 = fblpcf(w0, audioBuffer3, fs, n, d3, g3, amp3, rate3, fbLPF3)
    w4, audioBuffer4, fbLPF4 = fblpcf(w0, audioBuffer4, fs, n, d4, g4, amp4, rate4, fbLPF4)

    # Combine parallel paths
    combPar = 0.25 * (w1 + w2 + w3 + w4)

    # Two series all-pass filters
    w5, audioBuffer5 = apf(combPar, audioBuffer5, fs, n, d5, g5, amp5, rate5)
    out[n], audioBuffer6 = apf(w5, audioBuffer6, fs, n, d6, g6, amp6, rate6)


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
wav.write("dspfiles/outputfiles/moorerReverbMod12.wav", 48000, out)

print("Wav file written")

#plt.show()

