import cv2
import numpy as np
import time

video_path = 'output.mp4'

video_capture = cv2.VideoCapture(video_path)

ret, frame = video_capture.read()

# Stores YUV values of the entire video
def get_yuv():
    
    ret, frame = video_capture.read()
    
    height, width, _ = frame.shape

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break
        
        yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        
        # Stores YUV values of the frame
        Y, U, V = [], [], []

        # Get RGB values of each pixel in each frame and save it to a file
        for i in range(height):
            for j in range(width):

                y, u, v = yuv_frame[i, j]

                Y.append(y)
                U.append(u)
                V.append(v)

    video_capture.release()


start_time = time.time()

get_yuv()

end_time = time.time()

print(end_time-start_time)
