import cv2
import numpy as np

video_path = 'output.mp4'

video_capture = cv2.VideoCapture(video_path)

def get_rgb():
    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        # Default is BGR, switch to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, _ = frame_rgb.shape

        file = open("output.txt", "w")

        # Get RGB values of each pixel in each frame and save it to a file
        for a in range(height):
            for b in range(width):

                r, g, b = frame_rgb[a, b]

                y = 0.299*r + 0.587*g + 0.114*b
                u = -0.169*r - 0.331*g + 0.449*b + 128
                v = 0.499*r - 0.418*g - 0.0813*b + 128

                file.write((str(r) + " "+ str(g)+ " "+ str(b)) + "\n")

    video_capture.release()

