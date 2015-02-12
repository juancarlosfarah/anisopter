# -*- coding: utf-8 -*-

from scipy import stats
#import spike_trains
from CSTMD import *

neurons_no = 2
SYNAPSES_NO = 500   #1005        # Syn: 0 - 1100, K: 0.015 - 0.08

# Synapses
D = 30 # Maximum distance between compartments that are connected with a synapse
dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D)


#dr.run_experiment(PLOTS = True)

import numpy as np

# Values from 0 to 20 depending on the illumination of the pixel
image = []
for i in range(64) :
    image.append(np.random.rand())

for i in range(4) :
    for y in range(64) :
        image[y] = np.random.rand()
    times, ids = dr.run(time=100, rates=image)

dr.plot()
# Return times and ids to the pattern recognition module
#print list(times), list(ids)



