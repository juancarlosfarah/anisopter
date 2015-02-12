# -*- coding: utf-8 -*-

from scipy import stats
#import spike_trains
from Dragonfly import *

neurons_no = 2
SYNAPSES_NO = 500   #1005        # Syn: 0 - 1100, K: 0.015 - 0.08

# Synapses
D = 30 # Maximum distance between compartments that are connected with a synapse



dr = Dragonfly(2)

dr.run_experiment(synapses_no = SYNAPSES_NO, D=D, PLOTS = True)

