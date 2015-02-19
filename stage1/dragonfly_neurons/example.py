################################################################################
# File: Example.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Example of how to use Target_animation.py and estmd.py together.         
################################################################################

from Target_animation.Target_animation import Animation
from ESTMD_model.estmd import ESTMD
from NEURON_code_for_CSTMD1.first_attempt.CSTMD import CSTMD

# Set constants
# =============
out_directory = "input.avi"
bg_image = "Target_animation/Images/test.jpg"
bg_speed = 4

# Create movie (tests Target_animation.py)
# ========================================
#test = Animation()

#test.add_target(2, start=[0,300], end=[500,300], size=4, v=5)
#test.add_target(2, start=[0,350], end=[500,350], size=5, v=5)
#test.add_background(bg_image, bg_speed)

#test.run(out_directory)

# Load CSTMD neurons
# ==============================
neurons_no = 2
SYNAPSES_NO = 500
D = 30
dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D)


# Change movies (tests estmd.py)
# ==============================
test_estmd = ESTMD()
test_estmd.open_movie("input.avi")
test_estmd.run(out_dir = "result.avi", by_frame = True)
frame = True
#while frame is not False:
for i in range(40):
	frame = test_estmd.get_next_frame()
        frame = frame.ravel()
	times, ids = dr.run(time = 40, rates = frame)
dr.plot()
