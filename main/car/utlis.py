import cv2 #Open CV
import numpy as np #Numpy

#Convert image to binary, so that everything is black except of the road markings
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

#Function that grabs the values from the trackbars and return them as a array
def valTrackbars(wT=120, hT=60):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points

#Function that based on a set of points draw a circle
def drawPoints(img,points):
    for x in range(4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv2.FILLED)
    return img

#Sums all pixels in every column and calculates the average points x coordinate from the sums
def getHistogram(img,minPer=0.1,display= False,region=1):

    if region ==1: #If region 1 one
        histValues = np.sum(img, axis=0) #Sum all pixels
    else: #Else
        histValues = np.sum(img[img.shape[0]//region:,:], axis=0) #Sum the pixels in lover part of the image

    maxValue = np.max(histValues) #Calc max value
    minValue = minPer*maxValue #Create minimum value filter based on max value and parameter

    indexArray = np.where(histValues >= minValue) #Filter out to small values
    basePoint = int(np.average(indexArray)) #Create avg point from remaining values

    #Create a visualization image if display is set to 1
    if display:
        imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),1)
            cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return basePoint,imgHist

    return basePoint

#Stacks the 6 (in our case) images in a 3x2 grid
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
        hor = np.hstack(imgArray)
        ver = hor
    return ver

#Detects the drivable area on a binary image free of noise
def detect_lane_area(img):

    height, width = img.shape #Get dimensions
    driveable_area = np.zeros(img.shape, np.uint8) # Create blank area to draw the drivable area on
    points = [] #Array to store points that define the borders of the drivable area

    for row in range(0, height, 10): #For every 10th row in the input image
        pixel_l = int(width/2) #Find/reset midpoint

        #Walk "step by step" from middle to the left until we find the road markings/a white pixel
        #If we don’t find any road markings we add assume all area to the left at that point is drivable
        while img[row][pixel_l] == 0 and pixel_l != 0:
            pixel_l -= 1
        #When we find the border add coordinate where we found it to points array
        points.append([pixel_l, row])

        #Repeat process but this time rom middle to the right
        pixel_r = int(width/2)
        while img[row][pixel_r] == 0 and pixel_r != width-1:
            pixel_r += 1
        #Add cordinate
        points.insert(0,[pixel_r, row])

    points2 = np.copy(points) #Create a new array with correct datatype
    cv2.fillPoly(driveable_area, [points2], color=(255)) #Fill the driveable area using fillPoly and the found edges on the drivable area
    return driveable_area

