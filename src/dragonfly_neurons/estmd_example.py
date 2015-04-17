from src.ESTMD_model.ESTMD_model.estmd import ESTMD

# Set constants
# =============
out_directory = "input.avi"
bg_image = "target_animation/images/test.jpg"
bg_speed = 4

"""
# Create movie (tests target_animation.py)
# ========================================
test = Animation()
#test.add_target(2, start=[150,0], end=[150,500], size=6, v=3)
#test.add_target(2, start=[250,0], end=[250,500], size=6, v=3)
test.add_target(2, start=[0,0], end=[500,500], size=6, v=3)
test.add_background(bg_image, bg_speed)
test.run(out_directory, total_frames = 200)
"""


# Change movies (tests estmd.py)
# ==============================
test_estmd = ESTMD()
test_estmd.open_movie("input.avi")

test_estmd.run(out_dir = "result.avi", by_frame = False)

