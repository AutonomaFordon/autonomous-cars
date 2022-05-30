import cv2 #Open CV
import numpy as np #Numpy

#Convert image to binary, so that everyhing is black except of the road markings
def thresholding(img):
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # converts image values to HSV
    lowerWhite = np.array([0,40,70]) #lower bound
    upperWhite = np.array([50,255,255]) #higher bound
    maskWhite = cv2.inRange(imgHsv,lowerWhite,upperWhite) #if x camerapixel is within the lower and higher bound, x pixel will be white, 
    #if not, x pixel will be black
    return maskWhite

#Waraps the image so it resembles what it would look like from above
def warpImg(img,points,w,h,inv = False):
    pts1 = np.float32(points) #Copy if input img/array
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]]) #Create new/empty array with supplied dimensions 
    if inv: #If inverted
        matrix = cv2.getPerspectiveTransform(pts2, pts1) #Get inverted matrix
    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2) #Get matrix
    imgWarp = cv2.warpPerspective(img,matrix,(w,h)) #Preform the transformation
    return imgWarp

#Creates a widow where the user dynamicly can change the values that determine the warping of the image
def initializeTrackbars(intialTracbarVals,wT=120, hT=60):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 600, 400)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)

    
def valTrackbars(wT=120, hT=60):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points
 
def drawPoints(img,points):
    for x in range(4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv2.FILLED)
    return img
 
def getHistogram(img,minPer=0.1,display= False,region=1):
 
    if region ==1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0]//region:,:], axis=0)
 
    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
 
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    #print(basePoint)
 
    if display:
        imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),1)
            cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return basePoint,imgHist
 
    return basePoint
 
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def detect_lane_area(img):
    
    #cv2.imshow("Test:", img)
    
    height, width = img.shape
    driveable_area = np.zeros(img.shape, np.uint8)
    
    points = []
    
    for row in range(0, height, 10):
        pixel_l = int(width/2)
        while img[row][pixel_l] == 0 and pixel_l != 0:
            pixel_l -= 1
        #Add coordinate
        #points = np.append(points, [row, pixel_l])
        points.append([pixel_l, row])
        
        pixel_r = int(width/2)
        while img[row][pixel_r] == 0 and pixel_r != width-1:
            pixel_r += 1
        #Add c
        #points = np.append(arr=points, values=[row, pixel_r])
        points.insert(0,[pixel_r, row])
    
    points2 = np.copy(points)
    cv2.fillPoly(driveable_area, [points2], color=(255))
    return driveable_area



