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
    ####################################################################################################################
    edges = cv2.Canny(img,100,200)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, (5,5))
    
    cv2.imshow("Img", edges)


























    pace_r = 50
    pace_l = 50
    #pwml.ChangeDutyCycle(pace_l)
    GPIO.output(motorl[1], False)
    #pwmr.ChangeDutyCycle(pace_r)
    GPIO.output(motorr[1], False)

    if cv2.waitKey(1) == ord('q'): #Break if q is pressed
        break
