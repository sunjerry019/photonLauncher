# -*- coding: utf-8 -*-
"""
WOS 2015 - Signal Processing Day 1 
Fourier Transform Analysis

Created on Tue Jun 09 08:42:58 2015
@author: YZhanyou
"""

#%%
from __future__ import division
from scipy.io import wavfile
import matplotlib.pyplot as plt
import wave
import numpy as num
import pyaudio
import time


###############################  Functions   ##################################

def sinegen(fsamp,fsig,nsamp):
    tsamp = 1/fsamp
    t = num.r_[0:(nsamp)]*tsamp
    y = num.sin(2*num.pi*fsig*t).astype('float32')
    return (y,t)

def cosgen(fsamp,fsig,nsamp):
    tsamp = 1/fsamp
    t = num.r_[0:(nsamp)]*tsamp
    y = num.cos(2*num.pi*fsig*t).astype('float32')
    return (y,t)
    
def rect(fsamp,rectlen,nsamp):
    if rectlen > nsamp:
        print "Warning: rectlen cannot be larger than nsamp"
    else:
        tsamp = 1/fsamp
        t = num.r_[0:(nsamp)]*tsamp
        y = num.zeros(nsamp)
        y[0:rectlen] = num.ones(rectlen)        
        return (y,t)
        
def FFT_Block(sig,fsamp):
    N = len(sig);   
    fbin=num.r_[-N/2:N/2]/N*fsamp; 
    X = num.fft.fftshift(num.fft.fft(sig,N));
    return (X,fbin)
    
def IFFT_Block(sig,fsamp):
    N = len(sig); 
    tsamp = 1/fsamp;
    tbin=num.r_[0:N]*tsamp; 
    x = num.fft.ifft(sig,N);
    return (x,tbin)         

def Play_Sound(sig):    
    p = pyaudio.PyAudio()
    stream = p.open(rate=44100, channels=1, format=pyaudio.paFloat32, output=True)
    stream.write(sig.tostring())
     
def Record_Sound(wav_output_filename,record_time):    
    CHUNK = 1024;
    RATE = 44100;
    CHANNELS = 1;
    FORMAT = pyaudio.paFloat32;
    p = pyaudio.PyAudio()
    stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True, frames_per_buffer = CHUNK)
    frames = [];

    print("*start recording");    
    
    for i in range(0,int(RATE/CHUNK*record_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("*done recording");
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    
    wf = wave.open(wav_output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
  
    #read in wav file 
    rate1,dat1 = wavfile.read(wav_output_filename)
    return dat1
    
def pause(time_sec):
    time.sleep(time_sec)       
    
#%%
######################    FFT of Sinewave   ##############################    
fs = 4000;   # Sampling Frequency
N = 4000;    # Number of Samples

# Generate Sinewave
x_sin1, tbin1 = sinegen(fs,10,N)  # Sinewave
x_sin2, tbin2 = sinegen(fs,50,N)  # Sinewave    

# FFT to Freq Domain
SigX1,fbin1 = FFT_Block(x_sin1,fs)
SigX2,fbin2 = FFT_Block(x_sin2,fs)
    
# Plot Signals  
plt.figure(1)
# Time Domain
plt.subplot(211); plt.plot(tbin2,x_sin2)
plt.xlabel('Time (s)');plt.ylabel('Amplitude');plt.title('Time Domain')
# Frequency Domain
plt.subplot(212); plt.plot(fbin2,abs(SigX2)/N)
plt.xlabel('Frequency (Hz)');plt.ylabel('Amplitude');plt.title('Frequency Domain')   
 
#%%
######################    FFT of Cosine   ##############################    

##               TRY IT YOURSELF!!

   
#%%
######################    Multiple Sinewaves   ##############################   
x_sin1, tbin1 = sinegen(fs,10,N)  # Sinewave 1 
x_sin2, tbin2 = sinegen(fs,500,N)  # Sinewave 2
x_sin3, tbin3 = sinegen(fs,1000,N)  # Sinewave 3    

# Sum 3 sinewaves
Sine_add = 0.5*x_sin1 + 0.05*x_sin2 + 1*x_sin3

# FFT to Freq Domain
SigSum,fbin1 = FFT_Block(Sine_add,fs)

# Plot Signals  
plt.figure(2)
# Time Domain
plt.subplot(211); plt.plot(tbin1,Sine_add)
plt.xlabel('Time (s)');plt.ylabel('Amplitude');plt.title('Time Domain')
# Frequency Domain
plt.subplot(212); plt.plot(fbin1,abs(SigSum)/N)
plt.xlabel('Frequency (Hz)');plt.ylabel('Amplitude');plt.title('Frequency Domain')   


    
#%% 
######################     Rect Wave     #########################
rect1,tbin3 = rect(fs,N/200,N)       
SigRect1,fbin3 = FFT_Block(rect1,fs) 
 
# Plot Signals  
plt.figure(3)
# Time Domain
plt.subplot(211); plt.plot(tbin3,rect1)
plt.xlabel('Time (s)');plt.ylabel('Amplitude');plt.title('Time Domain')
# Frequency Domain
plt.subplot(212); plt.plot(fbin3,abs(SigRect1)/N)
plt.xlabel('Frequency (Hz)');plt.ylabel('Amplitude');plt.title('Frequency Domain')   



#%%
##################   Record Your Own Speech!!   ######################   
Speech1 = Record_Sound("save.wav",3)

#%% 
#################     Analyse Speech Signal   #################### 
fs1 = 44100;
tbin_s = num.r_[0:len(Speech1)]/fs1; 
SigSp1,fbin4 = FFT_Block(Speech1,fs1)  
 
# Plot Signals  
plt.figure(4)
# Time Domain
plt.subplot(211); plt.plot(tbin_s,Speech1)
plt.xlabel('Time (s)');plt.ylabel('Amplitude');plt.title('Time Domain')
# Frequency Domain
plt.subplot(212); plt.plot(fbin4,abs(SigSp1)/N)
plt.xlabel('Frequency (Hz)');plt.ylabel('Amplitude');plt.title('Frequency Domain')    
 
 
 
 