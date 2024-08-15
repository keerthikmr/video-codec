### Developmental notes

## FFmpeg commands

**Show video metadata**

`ffprobe -v error -show_format -show_streams input.mp4`


**Convert a rgb24 format to mp4**

`ffmpeg -f rawvideo -pix_fmt rgb24 -s DIMENSION -r FRAMERATE -i video.rgb24 -c:v libx264 output.mp4`
_Dimension has to be the same as the original source _


**Convert mp4 to rgb/rgb24**

`ffmpeg -i input.mp4 -f rawvideo -pix_fmt rgb24 output.rgb`


## Project notes

**Time optimizations**

Fetching the RGB values of each pixel in the 8 second 384x216 video takes ~35 seconds

Converting rgb to yuv using numerical formula takes upto ~570 seconds

Using the `yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)` method takes only 40 seconds
