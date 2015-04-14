# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:24:34 2013
@author: zfountas
"""
from brian import *

def make_input(angle = 50, pick = 300, duration = 300, delay = 50) :
    if angle > int(duration/2) :
        print "ERROR: The angle is too big!"
        return
    centre = duration - 2*angle
    P = NeuronGroup(1,model='x : Hz',threshold=PoissonThreshold(state='x'))
    M = SpikeMonitor(P)
    
    if delay > 0 :
        P.x = 0 * Hz
        run(delay*ms)

    for i in range(0, angle):
        P.x = i * Hz
        run(1*ms)

    if centre > 0 :
        P.x = pick * Hz
        run(centre*ms)
    
    for i in range(0, angle):
        P.x = (angle-i-1) * Hz
        run(1*ms)
    
    #raster_plot(M)
    #show()
    spikes3=[int(1000*float(t)) for i,t in M.spikes if i==0]
    return spikes3

#print make_input()


"""
import numpy
import matplotlib.pyplot as plt

import random


spike_times = []

tstop = 10.0

for rate in range(1,100) :
    number = int(2*tstop*rate/1000.0)
    tempList = (numpy.add.accumulate(numpy.random.exponential(1000.0/rate, size=number))).tolist()
    tempList = [x+tstop*rate for x in tempList]
    spike_times = spike_times + tempList
    
    

t = []
for i in range(len(spike_times)):
    t.append(0.0)

plt.figure(1)
plt.scatter(spike_times, t)
plt.show()
"""