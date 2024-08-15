# Developmental notes

## FFmpeg commands

**Show video metadata:**

`ffprobe -v error -show_format -show_streams input.mp4`  
<br/>

**Convert a rgb24 format to mp4:**

`ffmpeg -f rawvideo -pix_fmt rgb24 -s DIMENSION -r FRAMERATE -i video.rgb24 -c:v libx264 output.mp4`  
_Dimension has to be the same as the original source_  
<br/>

**Convert mp4 to rgb/rgb24:**

`ffmpeg -i input.mp4 -f rawvideo -pix_fmt rgb24 output.rgb`  
<br/>

## Project notes

#### With rgb24 format

Reading from an rgb24 format and derving yuv from rgb using numerical formula takes **~290ms** in golang

Converting the 8 second 384x216 video to rgb format takes **~0.7s**  


#### Time optimizations:

Fetching the RGB values of each pixel in the 8 second 384x216 video takes **~35s**

Using the `yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)` method takes only **~40s**

Reading bytes from rgb24 format and converting values to yuv using the numerical formula takes **~17s** in python
