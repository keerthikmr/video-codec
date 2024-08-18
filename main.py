import cv2
import ffmpeg
import zlib
import time

input_video_path = 'input.mp4'

# Fetch height and width of the video
height, width = cv2.VideoCapture(input_video_path).read()[1].shape[:2]

# Prevent overflow and underflow (bytes)
def clamp(x, min, max):
    if x < min:
        return min
    
    if x > max:
        return max
    
    return x


# Stores YUV values of the entire video using opencv method - takes more time (~40s for sample video)
# Not the default method
def get_yuv_cv():
    video_capture = cv2.VideoCapture(input_video_path)

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
    ffmpeg.input(input_video_path).output('video.rgb24', format='rawvideo', pix_fmt='rgb24').run()


# Read bytes of frames from the video
def get_byte_frames():
    frames = []

    # RGB24 format has 3 bytes (R, G, B) per pixel
    buffer_size = width*height*3

    with open('video.rgb24', 'rb') as file:
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
        
        # Formulae to convert RGB to YUV
        y = +0.299*r + 0.587*g + 0.114*b
        u = -0.169*r - 0.331*g + 0.449*b + 128
        v = 0.499*r - 0.418*g - 0.0813*b + 128

        Y.append(int(y))
        # U and V will be converted to intergers later
        U.append(u)
        V.append(v)

    return Y, U, V


# Average the U and V values of 2x2 pixels to downsample
def down_sample(U, V):

    down_sampled_V = []
    down_sampled_U = []

    for x in range(0, height, 2):
        for y in range (0, width, 2): 
            u = (U[x * width + y] + U[x * width + y + 1] + U[(x + 1) * width + y] + U[(x + 1) * width + y + 1]) / 4
            v = (V[x * width + y] + V[x * width + y + 1] + V[(x + 1) * width + y] + V[(x + 1) * width + y + 1]) / 4

            down_sampled_U.append(int(u))
            down_sampled_V.append(int(v))

    return down_sampled_U, down_sampled_V


# Get downsampled U and V values and append them to the Y values in planar format (Y->U->V)
def prepare_yuv_frames(frames):

    for i in range(len(frames)):
        Y, U, V = get_yuv(frames[i])

        down_sampled_U, down_sampled_V = down_sample(U, V)

        yuv_frame = Y + down_sampled_U + down_sampled_V

        frames[i] = bytearray(yuv_frame)
        
    return frames


# Save the YUV downsampled video to a file
def save_yuv_encode(frames):
    data = b"".join(frames)

    try:
        with open('encoded.yuv', 'wb') as f:
            f.write(data)
    except IOError as e:
        print(f"Error writing file: {e}")


# Only delta is impleted right now
def run_length_encoding(frames):
    # rle_encoded = []

    delta = []
    for i in range(len(frames)):
        delta_frame = []
        if i == 0:
            delta.append(bytearray(frames[0]))
            continue
        

        # Modulo 256 to handle overflow (wrap around for negative numbers)
        for j in range (len(frames[i])):
            delta_frame.append((frames[i][j] - frames[i-1][j]) % 256)
        
        delta.append(bytearray(delta_frame))

        # j = 0
        # run_length_encoding = []
        
        # while j < len(frames[i]):

        #     count = 0
        #     # Count the number of consecutive same values
        #     # Count should be less than 255 to fit in a byte
        #     while count < 255 and (j + count) < len(delta) and delta[j + count] == delta[j]:
        #         count += 1

        #     run_length_encoding.append(count)
        #     run_length_encoding.append(delta[j])

        #     j += count

        # rle_encoded.append(bytearray(run_length_encoding))

    return delta


def save_rle_encode(byte_rle_encoded):

    try:
        with open('rle_encoded.rle', 'wb') as f:
            f.write(byte_rle_encoded)

    except IOError as e:
        print(f"Error writing file: {e}")


def save_zlib_compressed(byte_rle_encoded):
    try:
        with open('zlib_encoded.bin', 'wb') as f:
            f.write(zlib.compress(byte_rle_encoded, level=9))

    except IOError as e:
        print(f"Error writing file: {e}")


def encode():
    convert_to_rgb()

    frames = get_byte_frames()

    frames = prepare_yuv_frames(frames)

    save_yuv_encode(frames)

    rle_encoded = run_length_encoding(frames)

    byte_rle_encoded = b"".join(rle_encoded)

    save_rle_encode(byte_rle_encoded)
    
    save_zlib_compressed(byte_rle_encoded)


# Read the encoded file and decompress it
def decompress():
    try:
        with open('zlib_encoded.bin', 'rb') as f:
            decompressed = zlib.decompress(f.read())

    except IOError as e:
        print(f"Error reading file: {e}")

    return decompressed


def get_decoded_frames(decompressed):
    frames = []
    
    # In the YUV downsampling step, each 2x2 pixel was substiuited with one value.
    # So the size would be half of the total RGB size
    buffer_size = (width*height*3)//2

    i = 0
    
    while (buffer_size * (i + 1) <= len(decompressed)):
        frame = decompressed[buffer_size * i : buffer_size * (i + 1)]

        frames.append(bytearray(frame))

        i += 1

    return frames


def reverse_delta(frames):

    for i in range(1, len(frames)):
        for j in range(len(frames[i])):
            frames[i][j] = (frames[i][j] + frames[i-1][j]) % 256
        
    return frames


def revert_to_rgb(yuv_frames):
    
    decoded_frames = []

    for frame in yuv_frames:

        Y = frame[:width*height]
        U = frame[width * height : width * height + (width * height // 4)]
        V = frame[width * height + width * height // 4:]

        rgb = []
        for j in range (height):
            for k in range(width):
                y = Y[j * width + k]
                try:
                    u = (U[(j // 2) * (width // 2) + (k // 2)]) - 128
                except IndexError:
                    print(int((j / 2) * (width / 2) + (k / 2)))
                v = (V[(j // 2) * (width // 2) + (k // 2)]) - 128

                r = clamp(y + 1.402 * v, 0, 255)
                g = clamp(y - 0.344 * u - 0.714 * v, 0, 255)
                b = clamp(y + 1.772 * u, 0, 255)

                rgb.append(int(r))
                rgb.append(int(g))
                rgb.append(int(b))

        decoded_frames.append(rgb)
    
    return decoded_frames


def save_yuv_decoded(yuv_frames):
    try:
        with open('decoded.yuv', 'wb') as f:
            for frame in yuv_frames:
                f.write(bytearray(frame))

    except IOError as e:
        print(f"Error writing file: {e}")

    
def save_decoded(decoded_frames):
    try:
        with open('decoded.rgb24', 'wb') as f:
            for frame in decoded_frames:
                f.write(bytearray(frame))

    except IOError as e:
        print(f"Error writing file: {e}")
    
    
# Revert all encoding steps in reverse order
def decode():

    decompressed = decompress()

    frames = get_decoded_frames(decompressed)

    yuv_frames = reverse_delta(frames)

    save_yuv_decoded(yuv_frames)

    decoded_frames = revert_to_rgb(yuv_frames)

    save_decoded(decoded_frames)
    

def main():
    encode()

    decode()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"Time taken: {end - start}")
