import wave
from graphics import *
import numpy
import struct
import math

def main():
#     speech = wave.open("si762.wav")
#     nframes = speech.getnframes()
#     
#     window = GraphWin("Speech", 1000, 500)
#     window.setCoords(0, -10000, nframes, 10000) #setCoords(xll, yll, xur, yur)
#     
#     by = 250
#     for i in range(0, nframes/by):
#         speech.readframes(by-1)
#         raw = speech.readframes(1)
#         converted = struct.unpack("<h", raw)
#         frame = int(converted[0])
#         point1 = Point(i*by, 0) 
#         point2 = Point(i*by + .8, frame)
#         rect = Rectangle(point1, point2)
#         rect.draw(window)
#     window.getMouse()
#     window.close()
#     speech.close()
    
    speech = wave.open("o.wav")
    nframes = speech.getnframes()
    print nframes
    window = 25.0
    sampling_rate = speech.getframerate()
    samps_per_window = int(sampling_rate*(window/1000))
    nyquist = samps_per_window/2
    ms = window/1000.0
    
    time_steps = {}
    window_start = 0
    max = 0
    while window_start < (nframes - samps_per_window):
        samples = []
        
        speech.readframes(window_start) # catch up to correct location
        
        for i in range(0, samps_per_window):
            raw = speech.readframes(1)
            converted = struct.unpack("<h", raw)
            samples = samples + [int(converted[0])]
        samples_array = numpy.array(samples)
        dft_matrix = numpy.fft.fft(samples_array)

        magnitudes = []
        for i in range(0, nyquist):
            real = numpy.real(dft_matrix[i])
            imag = numpy.imag(dft_matrix[i])
            sq_mag = math.sqrt(math.pow(real, 2) + math.pow(real, 2))
            mag = 2*sq_mag/samps_per_window
            log_mag = 10*math.log10(mag)
            if log_mag > max:
                max = log_mag
            magnitudes = magnitudes + [log_mag]
        time_steps[window_start] = magnitudes
        window_start += 10
        speech.rewind()
    
    window = GraphWin("Spectrograph", 1000, 500)
    bound = nyquist/ms
    window.setCoords(0, 0, nyquist, bound) #setCoords(xll, yll, xur, yur)
    print len(time_steps)
    for i in range(0, len(time_steps)-1):    
        for j in time_steps[i*10]:
            print i, j
            print "-" 
            freq = j/ms
            print freq
            print log_mag
            print bound
            print "--"
            val = 255*(1 - j/log_mag)
            window.plot(i, freq, color_rgb(val, val, val))
    window.getMouse()
    window.close()
# A black-and-white image, with time along the x-axis, 
# (where each 10ms window is 1 pixel of width), 
# frequency along the y-axis and 
# intensity indicated by the darkness of the pixel, 
#         with white meaning 0 intensity and 
#         black meaning maximum intensity.


# am I reading the data in correct?
# what should my upper bound be and nothing is reaching it?
    
    
    speech.close() 
    
if __name__ == "__main__":
    main()