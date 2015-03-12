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
    if argv[i] == "-K" and len(argv) > i+1 :
        i += 1
        K = float(argv[i]) 
    elif argv[i] == "-Na" and len(argv) > i+1 :
        i += 1
        Na = float(argv[i]) 
    elif argv[i] == "-file" and len(argv) > i+1 :
        i += 1
        filename = argv[i] 
        from_file = True
        print "Loading file", filename
    elif argv[i] == "-no-input" :
        no_input = True
        print "Running without any inputs"
    i += 1

if not from_file and not no_input :
    from target_animation.target_animation import Animation
    from ESTMD_model.estmd import ESTMD

    # Set constants
    # =============
    out_directory = "input.avi"
    bg_image = "Target_animation/Images/test.jpg"
    bg_speed = 4

    # Create movie (tests target_animation.py)
    # ========================================
    test = Animation()
    test.add_target(2, start=[0,300], end=[500,300], size=6, v=5)
    test.add_target(2, start=[0,150], end=[500,150], size=6, v=5)
    test.add_background(bg_image, bg_speed)
    test.run(out_directory)



    # Change movies (tests estmd.py)
    # ==============================
    test_estmd = ESTMD()
    test_estmd.open_movie("input.avi")

    test_estmd.run(out_dir = "result.avi", by_frame = True)

    frame_list = []
    frame = True
    #while frame is not False:
    for i in range(80):
        frame = test_estmd.get_next_frame()
        frame_list.append(frame)

elif from_file :
    with open(filename, 'rb') as my_file :
        frame_list = pickle.load(my_file)
        #frame_list = frame_list[10:20]    
elif no_input :
    frame_list = []
    for i in range(10) :
        frame_list.append(np.zeros([32,32]))

# Load CSTMD neurons
# ==============================
neurons_no = 2
SYNAPSES_NO = 1000 #500
D = 25 #30
time_bet_frames = 10
electrds=2
dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D,electrds=electrds)


if K >= 0 :
    dr.K = K
if Na >= 0 :
    dr.Na = Na

neuron_idx = 0


for frame in frame_list :
    frame = frame.ravel()
    times, ids = dr.run(time = time_bet_frames, rates = frame)

FINAL_THING = []
for i in times[neuron_idx] :
    FINAL_THING.append(float(i))

with open("data.pkl", 'wb') as my_file :
    pickle.dump(FINAL_THING, my_file)



#dr.plot()
dr.sp_trains_save()


#SAVE_FRAMES = False
#if SAVE_FRAMES :
#    with open("frame_targets.pkl", 'wb') as my_file :
#        pickle.dump(frame_list, my_file)





