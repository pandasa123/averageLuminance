'''
Using OpenCV 3.2+ and Numpy, we can calculate average percieved luminance of a video    
----
Dependencies
    - Python3
    - OpenCV 3.2+
    - Numpy
---
Run

$ python calculate.py [movie.mp4] [output.csv]
----
Output

Percieved Luminance = sqrt((0.299R)^2 + (0.587G)^2 + (0.114B)^2)
'''
import cv2
import os
import sys
import math
import numpy

def setup():
    if len(sys.argv) != 3:
        raise ValueError('Usage: python calculate.py [movie.mp4] [output.csv]')
    try:
        if os.path.exists(sys.argv[1]):
            print("Found video file!")
    except OSError:
        print('Error: No File')
    
    if os.path.exists(sys.argv[2]):
        os.remove(sys.argv[2]) 


# input: image
# output: (r,g,b)
def averageRGB(frame):
    rowavg = numpy.average(frame, axis=0)
    avg = numpy.average(rowavg, axis=0)
    # print(avg)
    return avg

# input: (r,g,b)
# output: luminance
def calculateLuminance(rgb):
    rval = 0.299*rgb[0]*rgb[0]
    gval = 0.587*rgb[1]*rgb[1]
    bval = 0.114*rgb[2]*rgb[2]
    return math.sqrt(rval + gval + bval)
    
from numba import double, jit 

if __name__ == "__main__":
    # Running preqs
    setup()
    f = open(sys.argv[2], 'a')
    # fastaverageRGB = jit(double[:,:])(averageRGB)
    # fastcalculateLuminance = jit(double[:,:,:])(calculateLuminance)
    
    # Playing video from file:
    currentFrame = 0
    # luminance = 0.0
    temp = 0.0

    video = cv2.VideoCapture(sys.argv[1])
    fps = math.ceil(video.get(cv2.CAP_PROP_FPS))
    reading, frame = video.read()
    reading = True

    while reading:

        reading, frame = video.read()
        if reading:
            averageRGB(frame)
            temp = calculateLuminance(averageRGB(frame)) + temp
            # print("Luminance for frame ", currentFrame, " = ", temp)
            if(currentFrame % fps == 0):
                f.write(str(temp/fps) + "\n")
                temp = 0.0
        else:
            break
            
        currentFrame += 1

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()

    # print("Average Luminance = ", luminance/currentFrame)