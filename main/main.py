#M import motorfunctions as motor
import motorFunctionsParallell as motors
import LaneDetection
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from threading import Thread

#lobal vars
global stream
global rawCapture

<<<<<<< HEAD
=======

>>>>>>> 1f0452d4526c8e513d26dc4de3ff1ac3a2c8b618
def setup():
    global stream
    global rawCapture
    
    #Setup motors
    t1 = Thread(target=motors.trackSpeed)
    t1.start()
    #M motor.calibrate()
    
    while(True):
        motors.setSpeed(20,20)
    
    #Setup Camera
    camera = PiCamera()
    camera.resolution = (120, 60) #Set resolution
    camera.framerate = 32 #Set framerate
    rawCapture = PiRGBArray(camera, size=(120, 60))
    time.sleep(1)#Give camera time to warmup
    # Setup streem
    stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=(120, 60))

def get_frame():
    global rawCapture
    image = next(stream) #Grab new frames
    img = image.array #Convert to array for processing in opencv
    rawCapture.truncate(0) #Clear streem buffer 
    return img

setup()

while True:
    #Get image
    img = get_frame()
    
    #Calculate curve and visualize
    curve = LaneDetection.getLaneCurve(img,display=0)
    cv2.waitKey(1)
    
    #Update motors
    if(curve == 0.0):
        motor.drive(pl=2.5 ,pr=2.5)
    elif(curve<0.00 and curve>-0.03):
        motor.drive(pl=1,pr=2)
    elif(curve<=-0.03):
        motor.drive(pl=0 ,pr=2)
    elif(curve>0.00 and curve<0.03):
        motor.drive(pl=2 ,pr=1)
    else:
        motor.drive(pl=2 ,pr=0)
    
    print(curve)
