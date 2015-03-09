from Target_animation.Target_animation import Animation
from ESTMD_model.estmd import ESTMD
import numpy as np
import pickle

# Set constants
# =============
out_directory = "input.avi"
bg_image = "Target_animation/Images/test.jpg"
bg_speed = 4

# Create movie (tests Target_animation.py)
# ========================================
test = Animation()
#test.add_target(2, start=[150,0], end=[150,500], size=6, v=3)
#test.add_target(2, start=[250,0], end=[250,500], size=6, v=3)
test.add_target(2, start=[0,0], end=[500,500], size=6, v=3)
#test.add_background(bg_image, bg_speed)
test.run(out_directory, total_frames = 200)



# Change movies (tests estmd.py)
# ==============================
test_estmd = ESTMD()
test_estmd.open_movie("input.avi")

test_estmd.run(out_dir = "result.avi", by_frame = True)

frame_list = []
frame = True
#while frame is not False:
for i in range(200):
    frame = test_estmd.get_next_frame()
    frame_list.append(frame)
    print np.mean(frame)

SAVE_FRAMES = True
if SAVE_FRAMES :
    with open("64x64_diag_200.pkl", 'wb') as my_file :
        pickle.dump(frame_list, my_file)
