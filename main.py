import cv2
import numpy as np

video_path = 'output.mp4'

video_capture = cv2.VideoCapture(video_path)

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    # Default is BGR, switch to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, width, _ = frame_rgb.shape

    file = open("output.txt", "w")

    # Get RGB values of each pixel in each frame and save it to a file
    for y in range(height):
        for x in range(width):

            r, g, b = frame_rgb[y, x]

            file.write((str(r) + " "+ str(g)+ " "+ str(b)) + "\n")

video_capture.release()
