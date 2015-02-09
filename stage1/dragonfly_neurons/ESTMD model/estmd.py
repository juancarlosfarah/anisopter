import cv2
import numpy as np
from scipy import signal
import math
from copy import deepcopy

# Run some filter function on non-negative matrix "x".
def RTC_exp(T_s, x):
    x[x > 0] = 1 / x[x >0]
    x[x > 0] = np.exp(-T_s * x[x > 0])
    return x

T0 = 0.001
LMC_rec_depth = 8
dt = 0.001
H_filter = np.array ([[-1, -1, -1, -1, -1],
                      [-1,  0,  0,  0, -1],
                      [-1,  0,  2,  0, -1],
                      [-1,  0,  0,  0, -1],
                      [-1, -1, -1, -1, -1]])

t = T0
frame_history = []
cap = cv2.VideoCapture("target.mov")

while(True):
    ret, frame = cap.read()

    # Split to basic colors and keep green color.
    blue,green,red = cv2.split(frame)

    # Blur and downsize image.
    downsize = cv2.pyrDown(green)
    downsize = 1.0 * downsize / 256.0

    frame_history.append(downsize)
    if len(frame_history) < LMC_rec_depth:
        continue


    b = [0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]
    a = [1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]
    n = LMC_rec_depth

    downsize = signal.lfilter(b, a, frame_history[-n:])[-1]

    # Convert to float
    #downsize = downsize.astype(float) #/ 256.0

    # Center surround antagonism kernel applied.
    CSscale = -1.0 / 9.0

    CSKernel = CSscale * np.ones((3,3))
    CSKernel[1][1] = 8.0 / 9.0

    downsize = cv2.filter2D(downsize, -1, CSKernel) 

    cv2.imshow('pre RTC', downsize)

    if 0.01 < t < 0.02:
        print "max", np.amax(downsize), "min", np.amin(downsize)

    # RTC filter.
    down_pos = deepcopy(downsize)
    down_neg = deepcopy(downsize)
    down_pos[down_pos < 0] = 0
    down_neg[down_neg > 0] = 0
    down_neg = -down_neg

    # On first step, instead of computing just save the images.
    if t == T0:
        v_pos_prev = deepcopy(down_pos)
        v_neg_prev = deepcopy(down_neg)
        down_pos_prev = deepcopy(down_pos)
        down_neg_prev = deepcopy(down_neg)  
        t += dt
        continue

    # Do everything for pos == ON.
    thau_pos = down_pos - down_pos_prev
    thau_pos[thau_pos >= 0] = 0.001
    thau_pos[thau_pos < 0] = 0.1
    mult_pos = RTC_exp(dt, thau_pos)
    v_pos = -(mult_pos-1) * down_pos + mult_pos * v_pos_prev
    v_pos_prev = deepcopy(v_pos)

    # Do everything for neg == OFF.
    thau_neg = down_neg - down_neg_prev
    thau_neg[thau_neg >= 0] = 0.001
    thau_neg[thau_neg < 0] = 0.1
    mult_neg = RTC_exp(dt, thau_neg)
    v_neg = -(mult_neg-1) * down_neg + mult_neg * v_neg_prev
    v_neg_prev = deepcopy(v_neg)

    down_pos_prev = deepcopy(down_pos)
    down_neg_prev = deepcopy(down_neg)    

    # Now apply yet another filter to both parts.
    v_pos = cv2.filter2D(v_pos, -1, H_filter) 
    v_neg = cv2.filter2D(v_neg, -1, H_filter) 
    
    # TO DO: figure out if you turn negative to 0 or to absolute value.
    v_pos[v_pos < 0] = 0
    v_neg[v_neg < 0] = 0

    b1 = [1.0, 1.0]
    a1 = [51.0, -49.0]
    v_neg = signal.lfilter(b1, a1, [v_neg_prev, v_neg])[-1]

    downsize = v_neg * v_pos

    # Show image.
    downsize *= 10000
    if 0.01 < t < 0.02:
        print "maxpost", np.amax(downsize), "minpost", np.amin(downsize)
    cv2.imshow('frame', downsize)

    # Rinse and repeat.
    t += dt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Run.s
cap.release()
cv2.destroyAllWindows()
