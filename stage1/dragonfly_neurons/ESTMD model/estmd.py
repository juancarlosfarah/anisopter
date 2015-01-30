import cv2
import numpy as np
import math

def G(t):
    return 1.06 * math.exp(math.pow((-math.log(t / 0.505, 10)),2) / 0.0776) - 0.3356 * math.exp(math.pow((- math.log(t / 0.875)), 2) / 0.238)

cap = cv2.VideoCapture("Slow Motion Dragonfly Hunting.mov")

t0 = 0.001
t = t0

while(True):
    ret, frame = cap.read()
    
    # Convert to grayscale
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue,green,red = cv2.split(frame)

    if t < 0.1:
        print "green"
        print green

    # Blur and downsize image
    downsize = cv2.pyrDown(green)
    #small = cv2.resize(downsize,(100,100))

    """
    if t < 0.1:
        print "small"
        print small
    """
    # LMC filter

    downsize *= G(t)
    
    if t < 0.1:
        print "G(t)"
        print downsize

    CSscale = -1.0 / 9.0

    CSKernel = CSscale * np.ones((3,3))
    CSKernel[1][1] = 8.0 / 9.0

    pyr = cv2.filter2D(downsize, -1, CSKernel) 
    
    if t < 0.1:
        print "pyr"
        print pyr

    cv2.imshow('frame', pyr)

    # Increase time step
    t += 0.001

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
