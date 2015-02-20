# -*- coding: utf-8 -*-

from scipy import stats
#import spike_trains
from CSTMD import *

import zaf_arrays as zaf

neurons_no = 10
SYNAPSES_NO = 500   #1005        # Syn: 0 - 1100, K: 0.015 - 0.08

# Synapses
D = 30 # Maximum distance between compartments that are connected with a synapse
dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D)


#dr.run_experiment(PLOTS = True)

import numpy as np

# Values from 0 to 20 depending on the illumination of the pixel
#image = []
#for i in range(4096) :
#    image.append(np.random.rand())

image = zaf.image

for i in range(len(image)) :
    #for y in range(4096) :
    #    image[y] = np.random.rand()
    times, ids = dr.run(time=40, rates=image[i])


spikes = []
for n in range(len(times)) :
    spikes.append(dict())
    spikes[-1]["times"] = list(times[n])
    spikes[-1]["ids"] = list(ids[n])

import pickle

with open('spike_trains.pkl', 'wb') as my_file :
    pickle.dump(spikes, my_file)

dr.plot()
# Return times and ids to the pattern recognition module
#print list(times), list(ids)



