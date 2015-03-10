"""
Creating test movie, where 25% of the movie represents repeating pattern.
"""

from Target_animation import Animation
import cv2


NUMBER_OF_REPS = 15
pat_dir = "Pattern.avi"
ran_dir = "Random.avi"
out_dir = "Result.avi"

"""
Create animation, which is joint of several animations.
"""

for i in range(NUMBER_OF_REPS):
    pat = Animation()
    pat.add_target(2, start=[200,300], end=[500,300], size=6, v=5)

    ran = Animation()
    ran.add_target(1, start=[250,300], end=[500,300], size=6, v=10)
    
    pat.run(pat_dir, total_frames=10)
    ran.run(ran_dir, total_frames=30)
    
    cap1 = cv2.VideoCapture(pat_dir)
    cap2 = cv2.VideoCapture(ran_dir)
    
    if i == 0:
        ret, frame = cap1.read()
        blue,green,red = cv2.split(frame)
        height, width = green.shape
        cod="PIM1"
        codec = cv2.cv.CV_FOURCC(cod[0], cod[1], cod[2], cod[3])
        video = cv2.VideoWriter(out_dir, codec, 20.0, 
                                    (width, height), 
                                    isColor=0)
                                    
    while True:
        try:                        
            ret, frame = cap1.read()
            blue,green,red = cv2.split(frame)
        except:
            break

        video.write(green)
        
    while True:          
        try:                     
            ret, frame = cap2.read()
            blue,green,red = cv2.split(frame)
        except:
            break

        video.write(green)


video.release()
cap1.release()
cap2.release()
cv2.destroyAllWindows() 
                                    
    
