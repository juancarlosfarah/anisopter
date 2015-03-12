################################################################################
# File: example.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Example of how to use target_animation.py and estmd.py together.
################################################################################

from NEURON_code_for_CSTMD1.first_attempt.CSTMD import CSTMD
from sys import argv 
import pickle
import numpy as np

filename = ""
from_file = False
no_input = False
if len(argv) > 1 :
    if argv[1] == "-file" and len(argv) > 2 :
        filename = argv[2] 
        from_file = True
        print "Loading file", filename
    if argv[1] == "-no-input" :
        no_input = True
        print "Running without any inputs"

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
        frame_list = frame_list[20:25]    
elif no_input :
    frame_list = []
    for i in range(10) :
        frame_list.append(np.zeros([32,32]))

# Load CSTMD neurons
# ==============================
neurons_no = 5
SYNAPSES_NO = 500
D = 30
electrds=50
dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D,electrds=electrds)


all_times = []
all_ids = []
for frame in frame_list :
    frame = frame.ravel()
    times, ids = dr.run(time = 10, rates = frame)
    all_times.append(times)
    all_ids.append(ids)
#dr.plot()
dr.sp_trains_save()


SAVE_FRAMES = False
if SAVE_FRAMES :
    with open("frame_targets.pkl", 'wb') as my_file :
        pickle.dump(frame_list, my_file)





