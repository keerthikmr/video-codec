import cv2

file_path = 'video.mp4'

vid = cv2.VideoCapture(file_path)

height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

print(f'Height: {height}, Width: {width}')