################################################################################
# File: example.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Example of how to use target_animation.py and estmd.py together.
################################################################################

from CSTMD import CSTMD
from sys import argv 
import pickle
import numpy as np

filename = ""
from_file = False
no_input = False

i = 1
K = 0.06
Na= 0.48
SYNAPSES_NO = 500
save="dat.pkl"
while i < len(argv) :
    if argv[i] == "-K" and len(argv) > i+1 :
        i += 1
        K = float(argv[i]) 
    elif argv[i] == "-Na" and len(argv) > i+1 :
        i += 1
        Na = float(argv[i])
    elif argv[i] == "-SYN" and len(argv) > i+1 :
        i += 1
        SYNAPSES_NO = float(argv[i]) 
    elif argv[i] == "d" and len(argv) > i+1 :
        i += 1
        save = argv[i] 
    elif argv[i] == "-file" and len(argv) > i+1 :
        i += 1
        filename = argv[i] 
        from_file = True
        print "Loading file", filename
    elif argv[i] == "-no-input" :
        no_input = True
        print "Running without any inputs"
    i += 1

if from_file :
    with open(filename, 'rb') as my_file :
        frame_list = pickle.load(my_file)
        #frame_list = frame_list[10:20]    
elif no_input :
    frame_list = []
    for i in range(10) :
        frame_list.append(np.zeros([32,32]))

for i in range(len(frame_list)) :
    frame_list[i] = frame_list[i].ravel()

# Load CSTMD neurons
# ==============================


neurons_no = 5

D = 30
electrds=50

#Already have default values

PIXEL_NO = len(frame_list[0])
MAX_CURRENT = 30
MIN_CURRENT = 3.0
MIN = 0.000005
MAX = 0.00005
PLOT_ACTIVITY = False
runtime=10
prints=False

print "K ",K," Na ",Na," Syn ",SYNAPSES_NO
dr = CSTMD(num_neurons=neurons_no, num_synapses=SYNAPSES_NO, synaptic_distance=D,num_electrodes=electrds,
potassium=K,sodium=Na,num_pixels=PIXEL_NO,max_current=MAX_CURRENT,min_current=MIN_CURRENT,min_weight=MIN,max_weight=MAX,plot_activity =PLOT_ACTIVITY,duration=runtime,input=frame_list,verbose=prints)

times=dr.run()
if PLOT_ACTIVITY:
	dr.plot()

#dump the spike times of the first neuron
neuron_idx = 0
spiketimes = []
for i in times[neuron_idx] :
    spiketimes.append(float(i))

#spike occurences are recorded per 1 ms of simulation
spikesPerMs=[0]*(len(frame_list)*runtime)

if len(spiketimes)!=0:
    for st in spiketimes :
        spikesPerMs[int(st)] += 1

with open(save, 'wb') as my_file :
    pickle.dump(spikesPerMs, my_file)





