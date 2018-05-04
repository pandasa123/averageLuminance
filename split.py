'''
Using OpenCV 3.2+, we can split video files into individual frames
----
Dependencies
    - Python3
    - OpenCV 3.2+
    - Numpy
---
Run

$ python split.py [movie.mp4] [destination]
----
Output

This creates directory [destination] with 1 fps frames from [movie.mp4]
'''
import cv2
import numpy as np
import os
import sys


def setup():
    if len(sys.argv) != 3:
        raise ValueError('Usage: python split.py [movie.mp4] [destination]')
    try:
        if os.path.exists(sys.argv[1]):
            print("Found video file!")
    except OSError:
        print('Error: No File')

    try:
        if not os.path.exists(sys.argv[2]):
            print("Making directory!")
            os.makedirs(sys.argv[2])
    except OSError:
        print('Error: Creating destination')


def extract():
    # Playing video from file:
    currentFrame = 0

    video = cv2.VideoCapture(sys.argv[1])
    reading, frame = video.read()
    reading = True

    while reading:

        # Capture at 1 fps
        video.set(cv2.CAP_PROP_POS_MSEC, (currentFrame * 1000))
        reading, frame = video.read()

        # Saves image of the current frame in jpg file
        cv2.imwrite(sys.argv[2] + "\\frame%d.jpg" % currentFrame, frame)
        print('Saving frame: ', currentFrame)

        # To stop duplicate images
        currentFrame += 1

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Running preqs
    setup()
    extract()