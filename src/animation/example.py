"""
File: Example.py
Author: Erik Grabljevec
E-mail: erikgrabljevec5@gmail.com
Doc: Example of how to use Target_animation.py          
"""

from animation.target_animation import Animation


# Set constants
# =============
out_directory = "result.avi"
bg_speed = 4

# Create simple movie.
# ====================
test = Animation()
test.add_target(2, start=[100,0], velocity=[1,0.5], size=5, v=25)
test.add_target(2, start=[250,400], velocity=[-1,-0.5], size=7, v=25)
test.add_target(1, start=[400,250], size=4)
test.add_target(1, start=[500, 300], size=5, v=15)

test.add_background("images/test.jpg", 2)
test.add_dragonfly([[300, 300, 0.0], [250, 300, 0.5], [250, 200, 1.1]])

test.run(out_directory, 10, 10)
