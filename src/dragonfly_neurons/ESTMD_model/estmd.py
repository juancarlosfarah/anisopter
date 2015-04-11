"""
Tool to isolate targets from video. You can generate appropriate videos
using module Target_animation.
"""


from copy import deepcopy
import math
import os

import numpy as np
from scipy import signal

import cv2


class ESTMD(object):
    """
    With this class we set parameters and extract targets from movie.
    
    User should interact with next methods:
        - open_movie: To set movie.
        - run: To make new_movie.
        - get_next_frame: To extract next frame in by_frame mode.
    For more information refer to method run.
    """

    # Constants.
    T0 = 0.001  # Starting time.
    LMC_rec_depth = 8   # Sets how smoothly we want to apply "signal.lfilter".
    dt = 0.001  # Time step.
    H_filter = np.array ([[-1, -1, -1, -1, -1],
                          [-1,  0,  0,  0, -1],
                          [-1,  0,  2,  0, -1],
                          [-1,  0,  0,  0, -1],
                          [-1, -1, -1, -1, -1]])
    cap = False  # Movie that we are capturing - "cap" - is set to false
                 # before we run "open_movie" method.
    by_frame = None
    # ---                
                          
    def RTC_exp(self, T_s, x):
        x[x > 0] = 1 / x[x > 0]
        x[x > 0] = np.exp(-T_s * x[x > 0])
        return x

    def __init__(self):
        pass
        
    def open_movie(self, movie_dir):
        """
        This method sets movie that we'll try to modify.
        
        Args:
            movie_dir: Directory of input we want to modify.
        """

        if not os.path.exists(movie_dir):
            raise NameError

        self.cap = cv2.VideoCapture(movie_dir)
                                    
    def run(self, by_frame=False, cod="PIM1", out_dir="result.avi", 
            image_width = 64, image_height = 64):
        """
        This method runs modification on the movie that we previously added
        using "open_movie" method.
        
        We have two options on how to process movie. We can either set 
        "by_frame" to True and than extract new video frame by frame using 
        method "get_next_frame". Other option we have is to set "by_frame"
        to False. In that case the movie will be exported to directory
        "out_dir" in format that we encode using argument "cod".
        
        Args:
            by_frame: Do we want to convert entire movie or by frame.
            cod: Encoding in which we want output movie.
            out_dir: Directory in which we output converted movie.
        """
        
        if not self.cap:
            "You need to run 'open_movie' method first!"
            return False

        self.by_frame = by_frame
        
        self.image_width = image_width
        self.image_height = image_height
        
        self.t = self.T0
        self.frame_history = []
        if not by_frame:
            self.create_movie(cod, out_dir)
        return True
    
    def get_next_frame(self):
        """
        Extract next frame.
        
        Only works if we ran method "run" with argument "by_frame" set to True.
        """
        
        # You can extract next frame only in by_frame mode.
        if not self.by_frame:
            "Run video in by_frame method! (refer to doc)"
            return False

        frame = self.next_frame()
        frame = cv2.resize(frame, (self.image_width, self.image_height))
        
        return frame
        
    def create_movie(self, cod, out_dir):
        img = self.next_frame()
        height, width =  img.shape
        codec = cv2.cv.CV_FOURCC(cod[0], cod[1], cod[2], cod[3])
        self.video = cv2.VideoWriter(out_dir, codec, 20.0, 
                                    (width, height), 
                                    isColor=0)
        while(True):

            frame = self.next_frame()
            if frame is False:
                break
            frame = (frame * 255.0).astype('u1')
            self.video.write(frame)

        self.video.release()
        self.cap.release()
        cv2.destroyAllWindows() 
        
    def next_frame(self):
        """
        The engine of the class.
        
        Applies concepts from paper:
        'Discrete Implementation of Biologically Inspired Image Processing for
         Target Detection' by K. H., S. W., B. C. and D. C. from
        The Univerity of Adelaide, Australia.
        """
        
        try:
            ret, frame = self.cap.read()
            # Split to basic colors and keep green color.
            blue,green,red = cv2.split(frame)
        except:
            return False
            
        downsize = green
        #cv2.imshow("Input", downsize)
        
        downsize = 1.0 * downsize / 256.0
        self.frame_history.append(downsize)

        b = [0.0, 0.00006, -0.00076, 0.0044, 
             -0.016, 0.043, -0.057, 0.1789, -0.1524]
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
        downsize = np.tanh(downsize)
        
        # Threshold.
        downsize[downsize < 0.6] = 0

        # Resize image.
        #downsize = cv2.resize(downsize, (self.image_width, self.image_height))
        #downsize = cv2.resize(downsize, (500,500))
        cv2.imshow('Output', downsize)
        
        self.t += self.dt

        return downsize
