################################################################################
# File: estmd.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Doc: 
#
################################################################################

import cv2
import math
import numpy as np
from scipy import signal
from copy import deepcopy

# Class: ESTMD
# ============
# Missing description !!!
#
class ESTMD:
    # Constants.
    T0 = 0.001
    LMC_rec_depth = 8
    dt = 0.001
    H_filter = np.array ([[-1, -1, -1, -1, -1],
                          [-1,  0,  0,  0, -1],
                          [-1,  0,  2,  0, -1],
                          [-1,  0,  0,  0, -1],
                          [-1, -1, -1, -1, -1]])
    cap = False  # Movie that we are capturing - "cap" - is set to false
                 # before we run "open_movie" method.
    by_frame = False
    # ---                
                          
    def RTC_exp(self, T_s, x):
        x[x > 0] = 1 / x[x >0]
        x[x > 0] = np.exp(-T_s * x[x > 0])
        return x

    def __init__(self):
        pass
        
    def open_movie(self, movie_dir):
        self.cap = cv2.VideoCapture(movie_dir)
                                    
    def run(self, by_frame = False, cod = "PIM1", out_dir = "result.avi"):
        if not self.cap:
            "You need to run 'open_movie' method first!!! (refer to doc)"
            return
        self.by_frame = by_frame
        codec = cv2.cv.CV_FOURCC(cod[0], cod[1], cod[2], cod[3])
        self.video = cv2.VideoWriter(out_dir, codec, 
                                     20.0, (500,500), isColor = 0)
        self.t = self.T0
        self.frame_history = []
        if not by_frame:
            self.create_movie()
    
    def get_next_frame(self):
        # You can extract next frame only in by_frame mode.
        if not self.by_frame:
            "Run video in by_frame method! (refer to doc)"
            return
            
        return next_frame()   
        
    def create_movie(self):
        while(True):
            frame = self.next_frame()
            if frame is False:
                break
            self.video.write(frame)

        # Run.
        self.video.release()
        self.cap.release()
        cv2.destroyAllWindows() 
        
    def next_frame(self):
        ret, frame = self.cap.read()

        # Split to basic colors and keep green color.
        blue,green,red = cv2.split(frame)
        downsize = green
        cv2.imshow("Input", downsize)
        
        downsize = 1.0 * downsize / 256.0
        self.frame_history.append(downsize)

        b = [0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]
        a = [1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]
        n = self.LMC_rec_depth

        downsize = signal.lfilter(b, a, self.frame_history[-n:], 
                                  axis = 0)[-1]

        # Center surround antagonism kernel applied.
        CSscale = -1.0 / 9.0
        CSKernel = CSscale * np.ones((3,3))
        CSKernel[1][1] = 8.0 / 9.0

        downsize = cv2.filter2D(downsize, -1, CSKernel) 

        # RTC filter.
        u_pos = deepcopy(downsize)
        u_neg = deepcopy(downsize)
        u_pos[u_pos < 0] = 0
        u_neg[u_neg > 0] = 0
        u_neg = -u_neg

        # On first step, instead of computing just save the images.
        if self.t == self.T0:
            print "Setting values"
            self.v_pos_prev = deepcopy(u_pos)
            self.v_neg_prev = deepcopy(u_neg)
            self.u_pos_prev = deepcopy(u_pos)
            self.u_neg_prev = deepcopy(u_neg)  

        # Do everything for pos == ON.
        tau_pos = u_pos - self.u_pos_prev
        tau_pos[tau_pos >= 0] = 0.001
        tau_pos[tau_pos < 0] = 0.1
        mult_pos = self.RTC_exp(self.dt, tau_pos)
        v_pos = -(mult_pos-1) * u_pos + mult_pos * self.v_pos_prev
        self.v_pos_prev = deepcopy(v_pos)

        # Do everything for neg == OFF.
        tau_neg = u_neg - self.u_neg_prev
        tau_neg[tau_neg >= 0] = 0.001
        tau_neg[tau_neg < 0] = 0.1
        mult_neg = self.RTC_exp(self.dt, tau_neg)
        v_neg = -(mult_neg-1) * u_neg + mult_neg * self.v_neg_prev
        self.v_neg_prev = deepcopy(v_neg)

        # keep track of previous u.
        self.u_pos_prev = deepcopy(u_pos)
        self.u_neg_prev = deepcopy(u_neg)    

        # Subtract v from u to give the output of each channel.
        out_pos = u_pos - v_pos
        out_neg = u_neg - v_neg

        # Now apply yet another filter to both parts.
        out_pos = cv2.filter2D(out_pos, -1, self.H_filter) 
        out_neg = cv2.filter2D(out_neg, -1, self.H_filter) 
        out_pos[out_pos < 0] = 0
        out_neg[out_neg < 0] = 0
        
        if self.t == self.T0:
            self.out_neg_prev = deepcopy(out_neg)

        # Delay off channel.
        b1 = [1.0, 1.0]
        a1 = [51.0, -49.0]
        
        out_neg = signal.lfilter(b1, a1, [self.out_neg_prev, out_neg], 
                                 axis = 0)[-1]
        out_neg_prev = out_neg
        downsize = out_neg * out_pos

        # Show image.
        downsize = 10000*(downsize)
        
        # Threshold.
        downsize[downsize < 0.6] = 0

        # Resize image.
        downsize = cv2.resize(downsize,(500,500))
        processed = (downsize * 255.0).astype('u1')
        cv2.imshow('Output', processed)
        
        self.t += self.dt

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        else:
            return processed
        