################################################################################
# File: Example.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Example of how to use Target_animation.py          
################################################################################

from Target_animation import Animation

# Set constants
# =============
out_directory = "../ESTMD model/output.avi"
bg_image = "Images/test.jpg"
bg_speed = 5

# Add targets and background. At the end run movie.
# =================================================
test = Animation()
test.add_target(2, start=[200,0], end=[200,500], size=2, v=20)
test.add_target(1, start=[500, 250], size=2, v=20)
test.add_target(2, start=[0,0], end=[500,500], size=2, v=20)
test.add_target(0, start=[300, 250], size=2, v=20)
test.add_background(bg_image, bg_speed)

test.run(out_directory)

