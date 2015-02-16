################################################################################
# File: Example.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Example of how to use Target_animation.py          
################################################################################

from Target_animation import Animation

# Set constants
# =============
out_directory = "../ESTMD model/test.avi"
bg_image = "Images/test.jpg"
bg_speed = 4

# Add targets and background. At the end run movie.
# =================================================
test = Animation()

#test.add_target(2, start=[0,150], end=[500,150], size=30, v=5)
#test.add_target(2, start=[0,250], end=[500,250], size=3, v=5)
test.add_target(2, start=[0,300], end=[500,300], size=4, v=5)
test.add_target(2, start=[0,350], end=[500,350], size=5, v=5)
test.add_target(2, start=[0,400], end=[500,400], size=6, v=5)
test.add_target(2, start=[0,450], end=[500,450], size=7, v=5)
test.add_target(2, start=[500,0], end=[0,500], size = 5, v=10)
test.add_target(0, start=[0, 250], size=5, v=20)
test.add_background(bg_image, bg_speed)

test.run(out_directory)

