'''
Using OpenCV 3.2+ and Pillow, we can calculate average percieved luminance of a video    
----
Dependencies
    - Python3
    - OpenCV 3.2+
    - Pillow
---
Run

$ python calculate.py [movie.mp4] [output.csv]
----
Output

Percieved Luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B`
'''
import cv2
import os
import sys
import math
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

# @njit(parallel=True)
def brightness( frame ):
    frame = Image.fromarray(frame)
    stat = ImageStat.Stat(frame)
    r,g,b = (stat.mean/255)
    return math.sqrt(0.2126*(relative(r)) + 0.7152*(relative(g)) + 0.0722*(relative(b)))

def relative( colour ):
    if((colour) <= 0.03928):
        return (colour/12.92)
    else:
        return (((colour + 0.055)/1.055)**2.4)

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

    f.write(str(luminance/currentFrame))
    f.write("\nElapsed: " + str(time.time()-start))