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
test.add_target(2, start=[250,0], end=[250,500], size=5, v=4)
test.add_target(2, start=[250,250], end=[250,500], size=5, v=6)


test.add_background("images/test.jpg", 2)
test.add_dragonfly([[320, 240, 0.0], [300, 220, 0.5], [250, 200, 1.0]])

print test.get_distance(0.2)

test.run(out_directory, 10, 10)
