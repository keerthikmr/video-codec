import cv2

video_path = 'video.rgb24'

video_capture = cv2.VideoCapture(video_path)

ret, frame = video_capture.read()

# height, width, _ = frame.shape
height, width = 216, 384

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

frames = []

def get_byte_frames():

    buffer_size = width*height*3

    with open(video_path, 'rb') as file:
        while True:
            frame = file.read(buffer_size)
            
            if not frame:
                break
                
            frames.append(frame)

get_byte_frames()


# Read RGB values directly from bytes and convert to YUV
def get_yuv():
    
    Y, U, V = [], [], []

    for frame in frames:
        for j in range(width*height):
            r, g, b = frame[3*j], frame[3*j+1], frame[3*j+2]
            
            y = +0.299*r + 0.587*g + 0.114*b
            u = -0.169*r - 0.331*g + 0.449*b + 128
            v = 0.499*r - 0.418*g - 0.0813*b + 128

            Y.append(y)
            U.append(u)
            V.append(v)

get_yuv()
