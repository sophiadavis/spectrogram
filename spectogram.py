import wave
from graphics import *
import numpy
import math
import array

def main():
# ************ #
#     make sure I'm getting the samples 
#     speech = wave.open("si762.wav")
#     n_samps = speech.getnframes()
#     window = GraphWin("Speech", 1000, 500)
#     window.setCoords(0, -35000, n_samps, 35000) #setCoords(xll, yll, xur, yur)
#     
#     
#     stream = speech.readframes(n_samps)
#     stream_converted = array.array('h', stream)
#     print type(stream_converted)
#     stream_converted = stream_converted.tolist()
#     print type(stream_converted)
#     
#     print max(stream_converted)
#     print n_samps
#     print len(stream_converted)
#     by = 25
#     
#     for i in range(0, n_samps):
#         frame = stream_converted[i]
#         point1 = Point(i, 0) 
#         point2 = Point(i + .8, frame)
#         rect = Rectangle(point1, point2)
#         rect.draw(window)
#     window.getMouse()
#     window.close()  
#     speech.close()
# ************ #

    speech = wave.open("si762.wav")
    
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
    
    print "n frames, samps per window, samps per by: "
    print n_samps, samps_per_window, windowby_samps
    
    ### store information about each window's spectrum in dictionary 
    # index by time step 
    time_steps = {}

    window_start = 0
    time_step = 0
    maximum = 0
    minimum = 0

    ### perform Discrete Fourier Transfer given samples in each window 
    # use DFT at each frequency to determine magnitude 
    while (window_start + samps_per_window) < n_samps:
#         window_max = 0
#         window_min = 0
        print "window start, time step: "
        print window_start, time_step
        print "nyquist, window in ms, highest_freq "
        print nyquist, (window_len_ms/1000.0), nyquist/(window_len_ms/1000.0), int(nyquist/(window_len_ms/1000.0))
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
#             if log_mag > window_max:
#                 window_max = log_mag
            if log_mag < minimum:
                minimum = log_mag
            if log_mag == 0:
                "I'm 0!!!"
#             if log_mag < window_min:
#                 window_max = log_mag
            magnitudes = magnitudes + [log_mag]
            
        # store magnitudes and maximum/minimum on current window 
        time_steps[time_step] = [magnitudes, max(magnitudes), min(magnitudes)]
        
        # increment window_start by number of samples separating each window starting position
        # increment index for storing magnitudes by 1
        window_start += windowby_samps
        time_step += 1
    
    ### graph spectogram
    window = GraphWin("Spectrogram", 400, 200)
    highest_freq = int(nyquist/(window_len_ms/1000.0))
    window.setCoords(0, 0, time_step, highest_freq) #setCoords(xll, yll, xur, yur)
    
    # at each time step, plot all frequencies at gray-scale intensity corresponding to magnitude    
    for i in range(0, time_step):
        window_maximum = time_steps[i][1]
        window_minimum = time_steps[i][2]
                
        # spectrum = GraphWin("Spectrum", 400, 200)  
#         spectrum.setCoords(0, 0, highest_freq, window_maximum)
#         line = Line(Point(400, 0), Point(400, window_maximum))
#         line.draw(spectrum)

        for j in range(0, nyquist):
            mag = time_steps[i][0][j]
            freq = j/(window_len_ms/1000.0)
#             val = 255*(1 - j/maximum)
#             val = 255*((mag - minimum)/(maximum - minimum))
#             val = 255 - 255*((mag - minimum)/(maximum-minimum))
            val = 255 - 255*((mag - window_minimum)/(window_maximum-window_minimum))
            window.plot(i, freq, color_rgb(val, val, val))
            # point1 = Point(freq, 0) 
#             point2 = Point(freq + 1, mag)
#             rect = Rectangle(point1, point2)
#             rect.draw(spectrum)
#         spectrum.getMouse()
#         spectrum.close()
    
    window.getMouse()
    window.close()
    
    speech.close() 
    
if __name__ == "__main__":
    main()