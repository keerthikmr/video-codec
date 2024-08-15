import cv2
import numpy as np
import time

video_path = 'video.rgb24'

video_capture = cv2.VideoCapture(video_path)

ret, frame = video_capture.read()

height, width = 216, 384

frames = []

# Stores YUV values of the entire video using opencv method
def get_yuv_cv():

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


def get_byte_frames():

    buffer_size = width*height*3

    with open(video_path, 'rb') as file:
        while True:
            frame = file.read(buffer_size)
            
            if not frame:
                break
                
            frames.append(frame)

get_byte_frames()

