# Calculating Perceived Luminance 

Using OpenCV 3.2+ and Numpy, this script was initially created to analyse the Perceived Luminance of DC movies and comparing them to Marvel movies. Perceived Luminance is perceived brightness, a formula given by [Digital ITU BT.601](http://www.itu.int/rec/R-REC-BT.601):

L = sqrt( 0.299R^2 + 0.587G^2 + 0.114B^2 )

## calculate.py

$ `python calculate.py [movie.mp4] [output.csv]`

* Uses OpenCV's VideoCapture to go through the source video
* Calculates average RGB 
* Applies Luminance over 1 second of source video 
* Writes to `output.csv`

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

#### DC Movie

* Man of Steel: 7913
* Batman vs Superman Dawn of Justice: 10466
* (Academy Award Winning) Suicide Squad: 7417
* Justice League: 6439

= 32245

#### Marvel Movie

* Iron Man: 6988
* The Incredible Hulk: 6144
* Iron Man 2: 6983
* Thor: 6269
* Captain America The First Avenger: 6782
* The Avengers: 7973
* Iron Man 3: 7171
* Thor The Dark World: 6074
* Captain America The Winter Soldier: 7576
* Guardians of the Galaxy: 6845
* Avengers Age of Ultron: 7834
* Ant-Man: 6445
* Captain America Civil War: 8199
* Doctor Strange: 6260
* Guardians of the Galaxy Vol 2: 7592
* Spider-Man Homecoming: 7338
* Thor Ragnarok: 7202
* Black Panther: 7360
* Avengers Infinity War: 8192

= 135227

Total Number of Datapoints = `167472`