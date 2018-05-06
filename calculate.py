'''
Using OpenCV 3.2+, Numpy, and Pillow, we can calculate average percieved luminance of a video    
----
Dependencies
    - Python3
    - OpenCV 3.2+
    - Numpy
    - Pillow
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
import time
from PIL import Image, ImageStat

from numba import double, njit 

import matplotlib.pyplot as plt
import csv

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
# output: (b,g,r)
def averageBGR(frame):
    rowavg = numpy.average(frame, axis=0)
    avg = numpy.average(rowavg, axis=0)
    # print(avg)
    return avg

# input: (r,g,b)
# output: luminance
@njit(parallel=True)
def calculateLuminance(rgb):
    bval = 0.114*rgb[2]*rgb[2]
    gval = 0.587*rgb[1]*rgb[1]
    rval = 0.299*rgb[0]*rgb[0]
    return math.sqrt(rval + gval + bval)

# @njit(parallel=True)
def brightness( frame ):
    frame = Image.fromarray(frame)
    stat = ImageStat.Stat(frame)
    r,g,b = stat.mean
    return math.sqrt(0.299*(r**2) + 0.587*(g**2) + 0.114*(b**2))

def plot(filename):

    x = []
    y = []

    x, y = numpy.loadtxt(filename, delimiter=',', unpack=True)

    plt.plot(x,y, label='Luminance')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Average Luminance over time')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Running preqs
    start = time.time()
    setup()
    f = open(sys.argv[2], 'a')
    # f.write("time,luminance\n")

    
    # Playing video from file:
    currentFrame = 0
    luminance = 0.0
    temp = 0.0

    video = cv2.VideoCapture(sys.argv[1])
    fps = math.ceil(video.get(cv2.CAP_PROP_FPS))
    reading, frame = video.read()
    reading = True

    while reading:

        reading, frame = video.read()
        if reading:
            # averageBGR(frame)
            # temp = calculateLuminance(averageBGR(frame)) + temp
            # print("Luminance for " + sys.argv[1] + " frame ", currentFrame, " = ", temp)
            temp = brightness(frame) + temp
            if(currentFrame % fps == 0):
                # f.write(str(currentFrame/fps) + "," + str(temp/fps) + "\n")
                luminance = luminance + temp
                temp = 0.0
        else:
            break

        currentFrame += 1

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()
    # plot(sys.argv[2])
    f.write(str(luminance/currentFrame))
    f.write("\nElapsed: " + str(time.time()-start))