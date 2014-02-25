"""
spectrogram.py, Sophia Davis, for 11/1/2013

This program takes a .wav file as a command line argument, calculates the 
Discrete Fourier Transform based on samples within windows of 25ms 
(offsetting each window starting position by 10ms), and plots the spectrogram
of the file.
"""
import sys
import wave
from graphics import *
import Tkinter as TK
import numpy
import math
import array

def main():
    if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' file.wav')
		sys.exit(1)
    file = sys.argv[1]

    speech = wave.open(file)
    
    ### define parameters
    n_samps = speech.getnframes() # total number of samples
    window_len_ms = 25.0 # window length in milliseconds
    windowby_ms = 10.0 # milliseconds between consecutive window starting positions 
    sampling_rate = speech.getframerate() # samples per second
    samps_per_window = int(sampling_rate*(window_len_ms/1000)) # samples per window
    windowby_samps = int(sampling_rate*(windowby_ms/1000)) # samples between between consecutive window starting positions
    nyquist = samps_per_window/2 # nyquist frequency
    
    ### read in .wav file as string of bytes, convert to list of usable samples
    stream = speech.readframes(n_samps)
    stream_converted = array.array('h', stream)
    stream_converted = stream_converted.tolist()
    speech.close()
    
    ### store information about each window's spectrum in dictionary 
    # index by time step 
    time_steps = {}

    window_start = 0
    time_step = 0
    maximum = 0
    minimum = 0

    ### perform Discrete Fourier Transform given samples in each window 
    # use DFT at each frequency to determine magnitude 
    while (window_start + samps_per_window) < n_samps:
        current_window = stream_converted[window_start : window_start + samps_per_window]
        dft_values = numpy.fft.fft(current_window)
        
        # calculate log magnitude at each frequency
        magnitudes = []
        for i in range(0, nyquist):
            real = numpy.real(dft_values[i])
            imag = numpy.imag(dft_values[i])
            sq_mag = math.sqrt(math.pow(real, 2) + math.pow(imag, 2))
            log_mag = 10*math.log10(sq_mag)
            if log_mag > maximum:
                maximum = log_mag
            if log_mag < minimum:
                minimum = log_mag
            magnitudes = magnitudes + [log_mag]
            
        # store magnitudes for current window 
        time_steps[time_step] = magnitudes
        
        # increment window_start by number of samples separating each window starting position
        # increment index for storing magnitudes by 1
        window_start += windowby_samps
        time_step += 1
    
    ### graph spectrogram
    highest_freq = int(nyquist/(window_len_ms/1000.0))
    window = GraphWin("Spectrogram", time_step, 200)
    window.setCoords(0, 0, time_step, highest_freq)
    
    # at each time step, plot all frequencies at gray-scale intensity corresponding to magnitude    
    # maximum magnitude is black, minimum is white 
    for i in range(0, time_step):

        for j in range(0, nyquist):
            mag = time_steps[i][j]
            freq = j/(window_len_ms/1000.0)
            val = 255 - 255*((mag - minimum)/(maximum-minimum))
            window.plot(i, freq, color_rgb(val, val, val))
    
    window.getMouse()
    TK.mainloop() 
    
if __name__ == "__main__":
    main()