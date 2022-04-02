#Import modules
import cv2 #OpenCV for video processing
import numpy as np
import math

#Setup video feed
cap = cv2.VideoCapture(0) #Create videocapture object
cap.set(3, 1600) #Set video stream width
cap.set(4, 900) #Set video stream height
cap.set(cv2.CAP_PROP_EXPOSURE,-1) #Set fixed exposure (SHOULD BE CHANGED TO AUTOEXPOSURE? !!!)
if not cap.isOpened(): #Check if camera feed is ok
    print("Cannot open camera")
    exit()


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert to grayscale
    
    #Canny edge detection
    edges = cv2.Canny(gray,50,200, None, 3)
    
    #Hough line detection
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv2.LINE_AA)

    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", frame)
    
    # Display the resulting frame
    #cv2.imshow('Video output', edges)
    if cv2.waitKey(1) == ord('q'): #Break if q is pressed
        break

#Clean and free resources
cap.release()
cv2.destroyAllWindows()