#Import modules
import cv2 #OpenCV for video processing
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

#Setup camera
camera = PiCamera()
camera.resolution = (640, 480) #Set resolution
camera.framerate = 32 #Set framerate
rawCapture = PiRGBArray(camera, size=(640, 480))

#Give camera time to warmup
time.sleep(1)

# Set up streem
stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=(640, 480))

while(True):
    image = next(stream) #Grab new frames
    frame = image.array #Convert to array for processing in opencv
    rawCapture.truncate(0) #Clear streem buffer 
    
    #Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert to grayscale
    gray = cv2.GaussianBlur(gray,(5, 5),0)

    
    #Canny edge detection
    edges = cv2.Canny(frame,50,150, None, 3)
    
    mask = np.zeros_like(edges)
    ignore_mask_color = 255
    
    imshape = frame.shape
    vertices = np.array([[(0,imshape[0]),(100, 160), (540, 160), (imshape[1],imshape[0])]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_edges = cv2.bitwise_and(edges, mask)

    rho = 2 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 15     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40 #minimum number of pixels making up a line
    max_line_gap = 30    # maximum gap in pixels between connectable line segments
    line_image = np.copy(frame)*0 # creating a blank to draw lines on

    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)


    
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)

    cv2.imshow("Result", masked_edges)

    if cv2.waitKey(1) == ord('q'): #Break if q is pressed
        break

#Clean and free resources
cv2.destroyAllWindows()
