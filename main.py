import cv2
import ffmpeg

video_path = 'output.mp4'

height, width = 216, 384

# Stores YUV values of the entire video using opencv method - takes more time (~40s for sample video)
# Not the default method
def get_yuv_cv():
    video_capture = cv2.VideoCapture(video_path)

    ret, frame = video_capture.read()
    
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


# Convert the video to RGB format using ffmpeg
def convert_to_rgb():
    # ffmpeg.input(video_path, format='rawvideo', pix_fmt='rgb24', s='216x384').output('output.rgb').run()
    ffmpeg.input("input.mp4").output('video.rgb24', format='rawvideo', pix_fmt='rgb24').run()


# Read bytes of frames from the video
def get_byte_frames():
    frames = []

    buffer_size = width*height*3

    with open(video_path, 'rb') as file:
        while True:
            frame = file.read(buffer_size)
            
            if not frame:
                break
                
            frames.append(frame)

    return frames


# Read RGB values from bytes and convert them to YUV
def get_yuv(frame):
    Y, U, V = [], [], []
    for j in range(width*height):
        r, g, b = frame[3*j], frame[3*j+1], frame[3*j+2]
        
        y = +0.299*r + 0.587*g + 0.114*b
        u = -0.169*r - 0.331*g + 0.449*b + 128
        v = 0.499*r - 0.418*g - 0.0813*b + 128

        Y.append(int(y))
        U.append(u)
        V.append(v)

    return Y, U, V


# Average the U and V values of 2x2 pixels to downsample
def down_sample(U, V):

    down_sampled_V = [0] * (width // 2 * height // 2)
    down_sampled_U = [0] * (width // 2 * height // 2)

    for x in range(0, height, 2):
        for y in range (0, width, 2): 
            u = (U[x*width+y] + U[x*width+y+1] + U[(x+1)*width+y] + U[(x+1)*width+y+1]) / 4
            v = (V[x*width+y] + V[x*width+y+1] + V[(x+1)*width+y] + V[(x+1)*width+y+1]) / 4

            downsampled_index = (x // 2) * (width // 2) + (y // 2)

            down_sampled_U[downsampled_index] = int(u)
            down_sampled_V[downsampled_index] = int(v)


    return down_sampled_U, down_sampled_V


def prepare_yuv_frames(frames):

    for i in range(len(frames)):
        Y, U, V = get_yuv(frames[i])

        down_sampled_U, down_sampled_V = down_sample(U, V)

        yuv_frame = Y + down_sampled_U + down_sampled_V

        frames[i] = bytearray(yuv_frame)
        
    return frames


def yuv_encode(frames):
    data = b"".join(frames)

    try:
        with open('encoded.yuv', 'wb') as f:
            f.write(data)
    except IOError as e:
        print(f"Error writing file: {e}")


def main():
    convert_to_rgb()
    
    frames = get_byte_frames()

    frames = prepare_yuv_frames(frames)

    yuv_encode(frames)


if __name__ == '__main__':
    main()
