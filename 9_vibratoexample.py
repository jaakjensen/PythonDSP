
import matplotlib.pyplot as plt 
import numpy as np
import scipy.io.wavfile as wav


########################################################################################
########################################################################################


def vibratoEffect(inputdata, audioBuffer, fs, n, wowdepth, wowrate, flutdepth, flutrate, gain):
    
    #Calculate lfo for current sample
    t=(n)/fs  
    lfo = wowdepth/2 * np.sin(2*np.pi*wowrate*t) + wowdepth
    lfo2 = flutdepth/2 * np.sin(2*np.pi*flutrate*t) + flutdepth

    lfo = lfo + lfo2

    #Determine indexes for circular buffer
    samplelength = len(audioBuffer)
    indexC = (n % samplelength)

    fracDelay = ((n-lfo) % (samplelength))          
    intDelay = np.floor(fracDelay)
    frac = fracDelay - intDelay

    nextSamp = ((intDelay + 1) % (samplelength))

    out = (1-frac) * audioBuffer[int(intDelay)] + (frac) * audioBuffer[int(nextSamp)]

    #Saturate the output signal using ArcTan clipping
    out = (2/np.pi)*np.arctanh(alpha*out)

    #Store the current output in appropriate index
    audioBuffer[indexC] = inputdata[0]

    return out, audioBuffer

########################################################################################
########################################################################################


wav_fname = 'dspfiles/tapestester.wav'

fs, data = wav.read(wav_fname)

Ts = 1/fs

timelength = data.shape[0] / fs
samplelength = data.shape[0]

print(f"timelength = {timelength}s")

# Divide audio signal by max int value for signed 16 bit number
data = data/np.iinfo(np.int16).max

#Set up the time axis for the waveform
time = np.linspace(0, timelength, data.shape[0])

#Initialize the delay buffer
maxDelay = 1000 #samples

#Create a 1 x maxDelay buffer filled with zeros 
audioBuffer = np.zeros(maxDelay)

#LFO Parameters
t = np.arange(0,samplelength)*Ts
wowrate = 0.5    #Frequency of LFO in Hz
wowdepth = 96  #Range of samples of delay

flutrate = 4
flutdepth = 50

#Amount of soft clipping
alpha = 4

#initialize output signal
out = np.zeros(samplelength)


#Run the function through all the samples
for n in range(0,samplelength):

    out[n], audioBuffer = vibratoEffect(data[n], audioBuffer, fs, n, wowdepth, wowrate, flutdepth, flutrate, alpha)


print("DSP complete")

#set up the graphs
#fig, axes = plt.subplots(nrows=2,ncols=1)

#plot the original waveform
#axes[0].plot(time, data, label="Original Audio Signal")
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
wav.write("dspfiles/outputfiles/wowandflutter.wav", 44100, out)

print("Wav file written")

#plt.show()
