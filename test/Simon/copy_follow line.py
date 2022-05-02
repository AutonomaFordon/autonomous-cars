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
    lower_bound = np.array([0, 70, 30])   
    upper_bound = np.array([70, 255, 255])
    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
  
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (5,5))
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, (5,5))
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 4) 
    edges = cv2.Canny(mask,50,100)
    #	cv.HoughLinesP(	image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]]	)
    lines = cv2.HoughLinesP(edges, 1, math.pi / 180, 80, 5, 5)
    
    cv2.imshow("Img", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("edges", edges)
    cv2.imshow("Lines", lines) #FEL!
#     
#     #pwml.ChangeDutyCycle(pace_l)
#     GPIO.output(motorl[1], False)
#     #pwmr.ChangeDutyCycle(pace_r)
#     GPIO.output(motorr[1], False)

    if cv2.waitKey(1) == ord('q'): #Break if q is pressed
        break

