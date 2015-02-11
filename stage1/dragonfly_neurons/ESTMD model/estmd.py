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
cap = cv2.VideoCapture("test.avi")

while(True):
    ret, frame = cap.read()

    # Split to basic colors and keep green color.
    blue,green,red = cv2.split(frame)

    # Blur and downsize image.
    #downsize = cv2.resize(green,(200,200))
    #downsize = cv2.pyrDown(green)
    #cv2.imshow("Pre", downsize)
    #downsize = cv2.GaussianBlur(green, (5, 5), 1)
    #cv2.imshow("After", downsize)

    #cv2.imshow("pre division by 256", cv2.resize(downsize, (500,500)))

    downsize = green

    cv2.imshow("orig", downsize)

    downsize = 1.0 * downsize / 256.0

    frame_history.append(downsize)
    """
    if len(frame_history) < LMC_rec_depth:
        continue
    """

    #cv2.imshow('pre time filter', cv2.resize(downsize, (500,500)))

    b = [0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]
    a = [1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]
    n = LMC_rec_depth

    downsize = signal.lfilter(b, a, frame_history[-n:], axis = 0)[-1]

    # Convert to float
    #downsize = downsize.astype(float) #/ 256.0

    cv2.imshow('pre CS', cv2.resize(downsize,(500,500)))

    # Center surround antagonism kernel applied.
    CSscale = -1.0 / 9.0

    CSKernel = CSscale * np.ones((3,3))
    CSKernel[1][1] = 8.0 / 9.0

    downsize = cv2.filter2D(downsize, -1, CSKernel) 

    if 0.01 < t < 0.02:
        print "max", np.amax(downsize), "min", np.amin(downsize)

    # RTC filter.
    u_pos = deepcopy(downsize)
    u_neg = deepcopy(downsize)
    u_pos[u_pos < 0] = 0
    u_neg[u_neg > 0] = 0
    u_neg = -u_neg

    # On first step, instead of computing just save the images.
    if t == T0:
        v_pos_prev = deepcopy(u_pos)
        v_neg_prev = deepcopy(u_neg)
        u_pos_prev = deepcopy(u_pos)
        u_neg_prev = deepcopy(u_neg)  
        #t += dt
        #continue

    # Do everything for pos == ON.
    tau_pos = u_pos - u_pos_prev
    tau_pos[tau_pos >= 0] = 0.001
    tau_pos[tau_pos < 0] = 0.1
    mult_pos = RTC_exp(dt, tau_pos)
    v_pos = -(mult_pos-1) * u_pos + mult_pos * v_pos_prev
    v_pos_prev = deepcopy(v_pos)

    # Do everything for neg == OFF.
    tau_neg = u_neg - u_neg_prev
    tau_neg[tau_neg >= 0] = 0.001
    tau_neg[tau_neg < 0] = 0.1
    mult_neg = RTC_exp(dt, tau_neg)
    v_neg = -(mult_neg-1) * u_neg + mult_neg * v_neg_prev
    v_neg_prev = deepcopy(v_neg)

    # keep track of previous u.
    u_pos_prev = deepcopy(u_pos)
    u_neg_prev = deepcopy(u_neg)    

    # Subtract v from u to give the output of each channel
    out_pos = u_pos - v_pos
    out_neg = u_neg - v_neg

    # Now apply yet another filter to both parts.
    out_pos = cv2.filter2D(out_pos, -1, H_filter) 
    out_neg = cv2.filter2D(out_neg, -1, H_filter) 

    # TO DO: figure out if you turn negative to 0 or to absolute value.
    out_pos[out_pos < 0] = 0
    out_neg[out_neg < 0] = 0
    
    #cv2.imshow("outpos", cv2.resize(out_pos,(500,500)))
    #cv2.imshow("outneg", cv2.resize(out_neg,(500,500)))
    
    if t == (T0):
        out_neg_prev = deepcopy(out_neg)

    # delay off channel 
    b1 = [1.0, 1.0]
    a1 = [51.0, -49.0]
    
    out_neg = signal.lfilter(b1, a1, [out_neg_prev, out_neg], axis = 0)[-1]
    out_neg_prev = out_neg
    downsize = out_neg * out_pos

    # Show image.
    downsize = 10000*(downsize)
    # Threshold
    downsize[downsize < 0.6] = 0
    if 0.00 < t < 0.02:
        print "maxpost", np.amax(downsize), "minpost", np.amin(downsize)
    cv2.imshow('frame', cv2.resize(downsize,(500,500)))

    # Rinse and repeat.
    t += dt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Run.s
cap.release()
cv2.destroyAllWindows()
