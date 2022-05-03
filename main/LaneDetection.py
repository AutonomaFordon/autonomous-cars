import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

import utlis
 
curveList = []
avgVal=10

#Setup camera
camera = PiCamera()
camera.resolution = (480, 240) #Set resolution
camera.framerate = 32 #Set framerate
rawCapture = PiRGBArray(camera, size=(480, 240))
 
#Give camera time to warmup
time.sleep(1)

# Setup streem
stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=(480, 240))
 
 
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
    
    height,width,channel = img.shape
    
    contours, hierarchy = cv2.findContours(imgWarp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

    contour_area = []

    for c in contours:

        print('area:', cv2.contourArea(c))

        contour_area.append((cv2.contourArea(c), c))

    print('--- contour_area ---')

    for item in contour_area:

        print('contour_area:', item[0])

        

    # sort list with `(area, contour)` using only `area`    

    contour_area = sorted(contour_area, key=lambda x:x[0], reverse=True)

    print('--- contour_area - sorted ---')

    for item in contour_area:

        print('contour_area:', item[0])

        

    # get two the biggest contours    

    print('--- two the biggest contours ---')    

    print('p0:', contour_area[0][0])

    print('p1:', contour_area[1][0])

    image2 = np.zeros((height, width, 3), dtype = "uint8")

    # draw them

    coords1 = np.vstack([contour_area[0][1], contour_area[1][1]])

    cv2.fillPoly(image2, [coords1], (255, 255, 255))

    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) 

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))

    c2=np.stack((coords[:,1], coords[:,0]), axis=-1)

    cv2.fillPoly(imgWarp, [c2], (255, 255, 255))
        
     
    #### STEP 3
    middlePoint,imgHist = utlis.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
 
    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
 
    #### STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)
 
    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve
 
 
if __name__ == '__main__':
    cap = cv2.VideoCapture('vid1.mp4')
    intialTrackBarVals = [70, 70, 0, 240 ]
    utlis.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1

        image = next(stream) #Grab new frames
        img = image.array #Convert to array for processing in opencv
        rawCapture.truncate(0) #Clear streem buffer 
        curve = getLaneCurve(img,display=2)
        print(curve)
        #cv2.imshow('Vid',img)
        cv2.waitKey(1)
