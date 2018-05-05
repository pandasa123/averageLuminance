# Calculating Perceived Luminance 

Using OpenCV 3.2+ and Numpy, this script was initially created to analyse the Perceived Luminance of DC movies and comparing them to Marvel movies. Perceived Luminance is perceived brightness, a formula given by [Digital ITU BT.601](http://www.itu.int/rec/R-REC-BT.601):

L = sqrt(0.299\*R^2 + 0.587\*G^2 + 0.114\*B^2)

## calculate.py

$ `python calculate.py [movie.mp4] [output.csv]`

## Running multiple instances concurrently

I haven't enabled multiprocessing or subprocessing due to the size of the I/O undermining concurrent processes. That being said, if you do want to run multiple processes of `calculate.py`, here's how you can do it: 

* Windows (Option 1): `start python calculate.py [movie.mp4] [output.csv]` for each video file in a `.dat` script. This opens a new terminal instance and runs `calculate.py` in the new terminal and you can still monitor the progress of each operation
* Windows (Option 2): `python calculate.py [movie.mp4] [output.csv] > nu1`for each video file in a `.sh` script. This surpresses the `STDOUT` output 
* Linux: `python calculate.py [movie.mp4] [output.csv] &` for each video file in a `.sh` script. This surpresses the `STDOUT` output 

## Notes 

### Source video handling

For this to be an effective measure of luminance and, by extension, average luminance, make sure to remove opening and ending credits since they aren't fully representative of the movie as a whole

### Data Size

The script takes a measurement every `CAP_PROP_FPS` number of frames (FPS of source video). For instance, if we have Justice League (~1:47:49 theatrical release) = 6439 seconds with each second containing an average of the luminance of `CAP_PROP_FPS` number of frames. I'd personally just stick to visualising an average comparision since A) Law of Averages and B) with multiple films analysed, we'll have an incomprehensible amount of data visualised

Justice League: 6439s 
Batman vs Superman Dawn of Justice: 10466s 
Man of Steel: 7913s

