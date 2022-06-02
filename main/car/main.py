import motorFunctionsParallell as motors
import LaneDetection #Includes necessary functions to detect Lane and intersections
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 #Opencv
from threading import Thread #Used to run multiple threads for parallell operations
from gpiozero import DistanceSensor

#Global variable definition 
global stream
global rawCapture

global ultrasonic

def setup(): #Setup function, run only once
    #Declare global variables
    global stream
    global rawCapture
    global ultrasonic

    #Setup Camera
    camera = PiCamera() #Create camera instance
    camera.resolution = (120, 60) #Set resolution
    camera.framerate = 32 #Set framerate
    rawCapture = PiRGBArray(camera, size=(120, 60)) #Create rawCapture stream
    time.sleep(1 )#Give camera time to warmup
    # Setup streem
    stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=(120, 60))
    
    ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=0.5)

def get_frame():
    global rawCapture #Declare golbal variable
    image = next(stream) #Grab new/next frame
    img = image.array #Convert to array for processing in opencv
    rawCapture.truncate(0) #Clear streem buffer 
    return img #Return new frame

setup() #Run setup
while True: 
    global ultrasonic
    
    img = get_frame()  #Get next image
    
    
    curve = LaneDetection.getLaneCurve(img,display=2) #Calculate curve (direction of the lane)
    dist = ultrasonic.distance
    
    if(dist>0.3):
        dist = 0.3
    if(dist<0.05):
        dist = 0
    
    #Update motors according to curve value
    motors.setSpeed(curve,dist*3.3333)
    
    print(dist)

    cv2.waitKey(1) #Keep visualization window visable for 1 ms (only used when the debugg window is visable) 
    #print(curve) #Print the curve  value to the console
