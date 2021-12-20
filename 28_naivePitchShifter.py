
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav

wav_fname = 'dspfiles/BibioGuitar.wav'

fs, inputSignal = wav.read(wav_fname)

Ts = 1/fs

semitones = 7               #how many semitones do we increase by?
tr = 2**(semitones/12)
dRate = 1 - tr              #Delay rate of change

#Initialize the delay buffer
maxDelay = int(0.05 * fs)        #may delay is 50 msecs

#Conditional to handle pitch up and pitch down
if dRate > 0:   #Pitch decrease
    d = 0
else :          #Pitch increase
    #initialize delay so it is always positive
    d = maxDelay - 1

timelength = inputSignal.shape[0] / fs
samplelength = inputSignal.shape[0]

print(f"timelength = {timelength}s")

# Divide audio signal by max int value for signed 16 bit number
inputSignal = inputSignal/np.iinfo(np.int16).max
print(inputSignal.shape)

#Set up the time axis for the waveform (for plotting)
time = np.linspace(0, timelength, inputSignal.shape[0])

#initialize output signal
out = np.zeros(samplelength)

#Create a 1 x maxDelay buffer filled with zeros 
audioBuffer = np.zeros(maxDelay)

#LFO Parameters
lfo = np.zeros(samplelength)



#Run the function through all the samples
for n in range(0,samplelength):

    #Determine output of delay buffer, which could be a fractional delay time
    intDelay = int(np.floor(d))
    nextSamp = ((intDelay + 1) % (maxDelay))
    frac = d - intDelay

    if intDelay == 0: #when delay time = zero
                     #"out" comes "in", not just delay buffer
        out[n] = (1-frac) * inputSignal[n,1] + frac * audioBuffer[0]
    else:
        out[n] = (1-frac) * audioBuffer[intDelay] + frac * audioBuffer[nextSamp]

    audioBuffer[1:] = audioBuffer[0:-1]
    audioBuffer[0] = inputSignal[n,1]

    # Store the current delay in signal for plotting
    lfo[n] = d

    d = d+dRate #Change the delay time for the next loop

    #if necessary, start a new cycle in LFO
    if d<0:
        d = maxDelay - 1
    elif d > maxDelay - 1:
        d = 0

########################################################################

print("DSP complete")

#set up the graphs
#fig, axes = plt.subplots(nrows=2,ncols=1)

#plot the original waveform
#axes[0].plot(time, inputSignal, label="Original Audio Signal")
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
wav.write("dspfiles/outputfiles/naivePitchShift.wav", 44100, out)

print("Wav file written")

#plt.show()
