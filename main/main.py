import motorFunctionsParallell as motors
import LaneDetection #Includes necessary functions to detect Lane and intersections
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 #Opencv
from threading import Thread #Used to run multiple threads for parallell operations

#Global variable definition 
global stream
global rawCapture

def setup(): #Setup function, run only once
    #Declare global variables
    global stream
    global rawCapture
    
    #Setup motors
    #The trackSpeed function continuously monitors and adjusts motor voltage to keep speed at set value
    t1 = Thread(target=motors.trackSpeed) #Create parallell thread for controling motors
    t1.start() #Start motor control thread 
    
    #Setup Camera
    camera = PiCamera() #Create camera instance
    camera.resolution = (120, 60) #Set resolution
    camera.framerate = 32 #Set framerate
    rawCapture = PiRGBArray(camera, size=(120, 60)) #Create rawCapture stream
    time.sleep(1 )#Give camera time to warmup
    # Setup streem
    stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=(120, 60))

def get_frame():
    global rawCapture #Declare golbal variable
    image = next(stream) #Grab new/next frame
    img = image.array #Convert to array for processing in opencv
    rawCapture.truncate(0) #Clear streem buffer 
    return img #Return new frame

setup() #Run setup
while True: 
    img = get_frame()  #Get next image
    
    
    curve = LaneDetection.getLaneCurve(img,display=0) #Calculate curve (direction of the lane)
    
    cv2.waitKey(1) #Keep visualization window visable for 1 ms (only used when the debugg window is visable) 
    
    #Update motors according to curve value
    if(curve == 0.0): #If zero - straight forward
        motors.setSpeed(4,4)
    elif(curve<0.00 and curve>-0.03): #If a litle to the right
        motors.setSpeed(1,2)
    elif(curve<=-0.03): #If a more to the right
        motors.setSpeed(0,4)
    elif(curve>0.00 and curve<0.03): #If a litle to the left
        motors.setSpeed(2,1)
    else: #If a more to the left
        motors.setSpeed(4,0)
    
    print(curve) #Print the curve value to the console
