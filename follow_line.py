#Import modules
import cv2 #OpenCV for video processing
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO


#pins used for motors, first uses pwm, second does not
motorl = [13, 5] #left motor pins
motorr = [12, 6] #right motor pins

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Set all motor pins as output
GPIO.setup(motorl[0], GPIO.OUT)
GPIO.setup(motorl[1], GPIO.OUT)
GPIO.setup(motorr[0], GPIO.OUT)
GPIO.setup(motorr[1], GPIO.OUT)

#PWM setup
pwml = GPIO.PWM(motorl[0], 1000)
pwmr = GPIO.PWM(motorr[0], 1000)

#PWM start
pwml.start(0)
pwmr.start(0)

#setup distancesensor, making object ultrasonic
#global ultrasonic
#ultrasonic = DistanceSensor(echo=ec, trigger=trig, max_distance=2.0)

#all motor pins = 0
GPIO.output(motorl[0], False)
GPIO.output(motorl[1], False)
GPIO.output(motorr[0], False)
GPIO.output(motorr[1], False)

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
    img = image.array #Convert to array for processing in opencv
    rawCapture.truncate(0) #Clear streem buffer 

    
    # convert to hsv colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower bound and upper bound for Green color
    lower_bound = np.array([0, 0, 140])   
    upper_bound = np.array([255, 50, 255])
    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
  
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, (10,10))
    
    edges = cv2.Canny(mask,50,150)
    
    mask2 = np.zeros_like(edges)
    ignore_mask_color = 255
    
    
    imshape = edges.shape
    vertices = np.array([[(0,imshape[0]),(0, 360), (640, 360), (imshape[1],imshape[0])]], dtype=np.int32)
    cv2.fillPoly(mask2, vertices, ignore_mask_color)
    masked_edges = cv2.bitwise_and(mask, mask2)
      
    edges = cv2.Canny(masked_edges,100,200)
    
    rho = 2 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 40     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40 #minimum number of pixels making up a line
    max_line_gap = 10    # maximum gap in pixels between connectable line segments
    line_image = np.copy(edges)*0 # creating a blank to draw lines on
    lines_acc_ang = 0
    
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)

    if lines is not None:
        for i in range(0, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            if (abs(y2-y1) > 20): 
                cv2.line(line_image, (x1, y1), (x2, y2), (255,255,0), 3, cv2.LINE_AA)
                #Get line ang
                ang = abs(x1-x2) / (y1-y2)
                #print(ang)
                if (abs(ang) < 1.7): 
                    lines_acc_ang += ang
                
    print(lines_acc_ang)
    cv2.imshow("Result", line_image)

    pace_r = 50
    pace_l = 50
    
    if(lines_acc_ang < 0):
        pace_r += 5*abs(lines_acc_ang)
        pace_l -=5*abs(lines_acc_ang)
    else:
        pace_r -= 5*abs(lines_acc_ang)
        pace_l += 5*abs(lines_acc_ang)
    
    pwml.ChangeDutyCycle(pace_l)
    GPIO.output(motorl[1], False)
    pwmr.ChangeDutyCycle(pace_r)
    GPIO.output(motorr[1], False)


    if cv2.waitKey(1) == ord('q'): #Break if q is pressed
        break
