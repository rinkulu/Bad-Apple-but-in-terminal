import sys, os, time, array
import cv2 as cv

def generate_indexes(nPixels, step):
    indexes = [0]
    current_index = 0
    while current_index + step <= nPixels-1:
        indexes.append(round(current_index+step))
        current_index += step
    result = array.array('I', indexes)
    return result


#filename = sys.argv[1]
filename = "video.mp4"
file = cv.VideoCapture(filename)
if not file.isOpened():
    print("could not open file")
    exit(1)

FPS = file.get(cv.CAP_PROP_FPS)
FRAME_INTERVAL = 1 / FPS

FRAME_WIDTH = int(file.get(cv.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT = int(file.get(cv.CAP_PROP_FRAME_HEIGHT))
TER_WIDTH, TER_HEIGHT = os.get_terminal_size()
SCALE = max(FRAME_HEIGHT/TER_HEIGHT, FRAME_WIDTH/TER_WIDTH)

LINE_INDEXES = generate_indexes(FRAME_HEIGHT, SCALE)
CLMN_INDEXES = generate_indexes(FRAME_WIDTH, SCALE)
HEIGHT = len(LINE_INDEXES)
WIDTH = len(CLMN_INDEXES)

buffer = array.array('B', b'\0' * (HEIGHT*(WIDTH+1)))
while 1:
    start = time.perf_counter()
    ret, frame = file.read()
    if not ret: 
        break

    for l, line in enumerate(LINE_INDEXES):
        buffer[l*(WIDTH+1)-1] = 10          # \n
        for c, column in enumerate(CLMN_INDEXES):
            pixel = frame[line][column]
            buffer[l*WIDTH+c+l] = 35 if pixel[0] >= 128 else 32      # "#" or "\s"
    
    os.system('cls' if os.name == "nt" else 'clear')
    print(buffer.tobytes().decode())

    end = time.perf_counter()
    time.sleep(FRAME_INTERVAL-(end-start+0.00035))

file.release()