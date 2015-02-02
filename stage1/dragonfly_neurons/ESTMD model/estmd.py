import cv2
import numpy as np
from scipy import signal
import math
from copy import deepcopy


# Function for applying LMC spatiotemporal filters
def G(t):
    return 1.06 * math.exp(math.pow((-math.log(t / 0.505, 10)),2) / 0.0776) - 0.3356 * math.exp(math.pow((- math.log(t / 0.875)), 2) / 0.238)

def RTC_exp(T_s, x):
    return math.exp(-T_s / x)

np.vectorize(RTC_exp)

cap = cv2.VideoCapture("Slow Motion Dragonfly Hunting.mov")

t0 = 0.001
t = t0
dt = 0.001
LMC_rec_depth = 8

frame_history = []

while(True):
    ret, frame = cap.read()
    
    # Convert to grayscale
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue,green,red = cv2.split(frame)

    # Blur and downsize image
    downsize = cv2.pyrDown(green)
    downsize = 1.0 * downsize / 256.0
    frame_history.append(downsize)
    if len(frame_history) < LMC_rec_depth:
        continue

    """
	if t < 0.1:
        print "small"
        print small
    """
    # LMC filter

<<<<<<< HEAD
#    if 0.005 < t < 0.055:
#        print "Before: "
#        print downsize

    b = [0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]
    a = [1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]
    n = LMC_rec_depth

    downsize = signal.lfilter(b, a, frame_history[-n:])[-1]

#    if 0.005 < t < 0.055:
#        print "After: "
#        print downsize
=======
    # Convert to float
    downsize = downsize.astype(float) / 256.0

    # LMC transfer function
    downsize *= G(t)

    if t < 0.1:
        print "G(t)"
        print downsize
>>>>>>> 2a0bdc6bf76f973e9ea114e5e8c9998b34016136

    # Center surround antagonism kernel applied
    CSscale = -1.0 / 9.0

    CSKernel = CSscale * np.ones((3,3))
    CSKernel[1][1] = 8.0 / 9.0

<<<<<<< HEAD
    downsize = cv2.filter2D(downsize, -1, CSKernel) 
=======
    pyr = cv2.filter2D(downsize, -1, CSKernel) 
    
    
    # Apply hyperbolic tan function before imshow
    pyr = np.tanh(pyr)

    if t < 0.1:
        print "pyr"
        print pyr
>>>>>>> 2a0bdc6bf76f973e9ea114e5e8c9998b34016136


    # RTC filter
      
    down_pos = deepcopy(downsize)
    down_neg = deepcopy(downsize)
    down_pos[down_pos < 0] = 0
    down_neg[down_neg > 0] = 0
    down_neg = -down_neg

    # On first step, instead of computing just save the image.
    if t == 0:
        v_pos_prev = deepcopy(down_pos)
        v_neg_prev = deepcopy(down_neg)
        down_pos_prev = deepcopy(down_pos)
        down_neg_prev = deepcopy(down_neg)  
        continue

    
    # Do everything for pos == ON
    thau_pos = down_pos - down_pos_prev
    thau_pos[thau_pos > 0] = 0.001
    thau_pos[thau_pos < 0] = 0.1
    mult = RTC_exp(dt, that_pos)
    v_pos = -(mult-1) * down_pos + mult * v_pos_prev
    v_pos_prev = deepcopy(v_pos)

    # Do everything for neg == OFF
    thau_neg = down_neg - down_neg_prev
    thau_neg[thau_neg > 0] = 0.001
    thau_neg[thau_neg < 0] = 0.1
    mult = RTC_exp(dt, that_pos)


    down_pos_prev = deepcopy(down_pos)
    down_neg_prev = deepcopy(down_neg)    

    ### Rinse and repeat
    cv2.imshow('frame', v_pos)
    t += dt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Run
cap.release()
cv2.destroyAllWindows()
