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
K = -1
Na= -1
while i < len(argv) :
    if argv[i] == "-file" and len(argv) > i+1 :
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
SYNAPSES_NO = 500
D = 30
electrds=50

#Already have default values
K=0.06
Na=0.48
PIXEL_NO = len(frame_list[0])
MAX_CURRENT = 30
MIN_CURRENT = 2.0
MIN = 0.000005
MAX = 0.00005
PLOT_ACTIVITY = False
runtime=10

dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D,electrds=electrds,
K=K,Na=Na,PIXEL_NO=PIXEL_NO,MAX_CURRENT=MAX_CURRENT,MIN_CURRENT=MIN_CURRENT,MIN=MIN,MAX=MAX,PLOT_ACTIVITY =PLOT_ACTIVITY,runtime=runtime,input=frame_list)

times=dr.run()
if PLOT_ACTIVITY:
	dr.plot()
neuron_idx = 0
FINAL_THING = []
for i in times[neuron_idx] :
    FINAL_THING.append(float(i))

with open("data.pkl", 'wb') as my_file :
    pickle.dump(FINAL_THING, my_file)




