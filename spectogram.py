import wave
from graphics import *
import numpy
import struct

def main():
    speech = wave.open("si762.wav")
    print "number of audio channels: "
    print speech.getnchannels()
    print "sample width in bytes: "
    print speech.getsampwidth()
    print "number of audio frames: "
    nframes = speech.getnframes()
    print nframes 
    print "frame rate: "
    print speech.getframerate()
    print "compression type: "
    print speech.getcomptype()
    print speech.getcompname()
#    speech.rewind() # rewinds file pointer to beginning of audio stream
    window = GraphWin("Speech", 1000, 500)
    window.setCoords(0, -10000, nframes, 10000) #setCoords(xll, yll, xur, yur)
#     line = Line(Point(0, 0), Point(4500, 0))
#     line.setOutline("green")
#     line.setFill("green")
#     line.draw(window)
#     for i in range(0, 200):#nframes):
    by = 250
    for i in range(0, nframes/by):
        speech.readframes(by-1)
        raw = speech.readframes(1)
#         print "raw " + raw
        converted = struct.unpack("<h", raw)
#         print "converted: "
#         print converted
        print "i: " + str(i*by) 
        frame = int(converted[0])
        
        print frame
        point1 = Point(i*by, 0) 
        point2 = Point(i*by + .8, frame)
#         point1.draw(window)
#         point2.draw(window)
#         point1 = Point(i, 0) 
#         point2 = Point((i+1), 20)
        rect = Rectangle(point1, point2)
#         rect = Rectangle(Point(i, 0), Point(i+.8, 5))
#         rect.setFill("green")
        rect.draw(window)
    window.getMouse() # pause for click in window
    window.close()

#     for speech.readframes(10) # reads and returns at most n frames of audio, as a string of bytes
    
    

    
    
    speech.close() 
    
#     win = GraphWin("Window", 200, 200)
#     msg = Text(Point(100, 50), 'Original message...')
#     msg.draw(win)
#     # ...
#     # ... just important that there is a drawn Text object
#     win.promptClose(msg)

if __name__ == "__main__":
    main()