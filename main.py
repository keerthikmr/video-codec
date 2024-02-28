import cv2
from PIL import Image
import numpy as np

file_path = 'short-video.mp4'

vid = cv2.VideoCapture(file_path)

height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

print(f'Height: {height}, Width: {width}')

frames = []

while True:
    frame = vid.read()
    if frame[0] == False:
        break
    frames.append(frame)

print(frames)
