import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

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

GPIO.output(motorl[0], False)
GPIO.output(motorl[1], False)
GPIO.output(motorr[0], False)
GPIO.output(motorr[1], False)

import utlis
 
curveList = []
avgVal=10

#Setup camera
camera = PiCamera()
camera.resolution = (120, 60) #Set resolution
camera.framerate = 32 #Set framerate
rawCapture = PiRGBArray(camera, size=(120, 60))
 
#Give camera time to warmup
time.sleep(1)

# Setup streem
stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=(120, 60))
 
 
def getLaneCurve(img,display=2):
 
    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utlis.thresholding(img)
 
    #### STEP 2
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)
    
    #### STEP 2.5
    countours = np.copy(imgWarp)
    countours = cv2.erode(countours,(3,3),iterations = 1)
    
    driveable_area = utlis.detect_lane_area(countours)
     
    #### STEP 3
    middlePoint,imgHist = utlis.getHistogram(driveable_area,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(driveable_area, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
 
    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
 
#     #### STEP 5
#     if display != 0:
#         imgInvWarp = utlis.warpImg(driveable_area, points, wT, hT, inv=True)
#         imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
#         imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
#         imgLaneColor = np.zeros_like(img)
#         imgLaneColor[:] = 0, 255, 0
#         imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
#         imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
#         midY = 450
#         cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
#         cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
#         cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
#         for x in range(-30, 30):
#             w = wT // 20
#             cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
#                      (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
#         #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
#         #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
#     if display == 2:
#         imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, driveable_area],
#                                              [imgHist, imgLaneColor, imgResult]))
#         cv2.imshow('ImageStack', imgStacked)
#     elif display == 1:
#         cv2.imshow('Resutlt', imgResult)


    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve
 
 
def steering_dir():
    cap = cv2.VideoCapture('vid1.mp4')
    intialTrackBarVals = [3, 18, 0, 60 ]
    utlis.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1
        
        image = next(stream) #Grab new frames
        img = image.array #Convert to array for processing in opencv
        rawCapture.truncate(0) #Clear streem buffer 
        curve = getLaneCurve(img,display=2)
        print(curve)
        #cv2.imshow('Vid',img)l
        cv2.waitKey(1)
        #return curve
        
        if(curve>0):
            GPIO.output(motorl[0], True)
            GPIO.output(motorl[1], False)
            GPIO.output(motorr[0], False)
            GPIO.output(motorr[1], False)
            
        if(curve<0):
            GPIO.output(motorl[0], False)
            GPIO.output(motorl[1], False)
            GPIO.output(motorr[0], True)
            GPIO.output(motorr[1], False)
        
while True:
    steering_dir()
