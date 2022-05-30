import cv2  # Open CV
import numpy as np  # Numpy

import time

import utlis  # Supporting functions

# Global vars
curveList = []  # List of latest curve values
avgVal = 10  # Set max length of curveList


def getLaneCurve(img, display=2):  # Takes an image as input and calculates the curve (direction of the lane)
                                   # img is the input image and display determines if we should visualize the sub steps (set to 0 to disable and 1 to enable)

    imgCopy = img.copy()  # Create copy of img
    imgResult = img.copy()  # Create second copy of img

    # Convert image to binary, so that everything is black except of the road markings
    imgThres = utlis.thresholding(img)

    # Warap the image so it resembles what it would look like from above
    hT, wT, c = img.shape  # Extract img hight width and channels to variables
    points = utlis.valTrackbars()  # Grab reference points to warp image
    imgWarp = utlis.warpImg(imgThres, points, wT, hT)  # Preform the warp
    imgWarpPoints = utlis.drawPoints(imgCopy, points)  # Visualize the reference points

    # Erode the img, removes some noise
    countours = cv2.erode(imgWarp, (3, 3), iterations=1)

    # Detect the drivable area from the processed img, retuned imgage/array has drivable pixels set 1 and all other set to 0
    driveable_area = utlis.detect_lane_area(countours)

    # Calculate midpoint of drivalbe area using a historam
    middlePoint, imgHist = utlis.getHistogram(driveable_area, display=True, minPer=0.5,
                                              region=4)  # Calcualte midoint of lane directly in front of car
    curveAveragePoint, imgHist = utlis.getHistogram(driveable_area, display=True,
                                                    minPer=0.9)  # Calculate midpoint of lane area
    curveRaw = curveAveragePoint - middlePoint  # Calculate curve value be taking difference between points

    curveList.append(curveRaw)  # Store result in list
    if len(curveList) > avgVal:  # Clear 1 element if list is to long
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))  # Take average value

    # Finaly, visualize the steps if display is not set to 0
    if display != 0:
        # The following comands processes the images from some of the substeps and puts them besieds eachother in 3x2 grid for visualization
        imgInvWarp = utlis.warpImg(driveable_area, points, wT, hT, inv=True)
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

    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, driveable_area],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    ##We previously had a second debug option for display == 1 but it has been removed

    # Normalize the curve value to stay in relative close proximity to 0 (max of 1 and min of -1)
    curve = curve / 100
    if curve > 1: curve == 1
    if curve < -1: curve == -1

    return curve


# Initial setup
intialTrackBarVals = [3, 18, 0, 60]  # Set default values for the trackbar which are used to warp the image
utlis.initializeTrackbars(intialTrackBarVals)  # Add the default values to the trackbars

