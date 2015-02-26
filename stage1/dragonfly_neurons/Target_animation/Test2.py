"""
Unit tests for part of module Target_animation.
"""

import pdb
import unittest
from Target_animation import *

class TestOnDraw(unittest.TestCase):
    """
    Separate class to test AnimationWindow's on_draw method.
    """
       
    def make_directory(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def setUp(self):
        """
        Method that runs at the start of each test.
        """
        
        self.N = 3
        self.pos = [[0, 0], [20, 20], [50, 50]]
        self.target0 = Target(0, self.pos[0], [100, 100], 5, 5, [0, 0, 0])
        self.target1 = Target(1, self.pos[1], [100, 100], 5, 5, [0, 0, 0])
        self.target2 = Target(2, self.pos[2], [0, 100], 5, 5, [0, 0, 0])
        
        self.target_list = [self.target0, self.target1, self.target2]
        self.width = 640
        self.height = 480
        self.bg_image = "Images/test.jpg"
        self.bg_speed = 5
        
        self.window = AnimationWindow(self.target_list, self.width, 
                                       self.height, False, 0)
        
    def test_on_draw(self):
        """
        Tests if AnimationsWindows' method on_draw works correctly. It also
        implicitly checks correctness of method circle.
        This function works by drawing one image and saving it. It than checks
        if there are circles at those points as expected and that self.time
        was updated.
        TO DO(ask): Is implicit testing ok? How to improve this part?
        """
        
        print "HERE"
        self.make_directory("temp")
        
        pyglet.clock.schedule_once(self.window.update_frames, 0.001)
        pyglet.clock.schedule_once(self.window.stop, 0.001)
        pyglet.app.run()
        
        self.assertEqual(self.window.time, 2)
        
        img1 = cv2.imread("temp/scr0.png")
        for i in range(self.N):
            x = self.pos[i][0]
            y = self.pos[i][1]
            print x, y, " --> ", img1[x][y][0]
            self.assertTrue(img1[x][y][0] > 0)
        
        print
        print img1[0]
        print
        print
        print img1[1]
        print
        print
        print img1[2]
        print
        print
        print len(img1[0][0])

        self.assertTrue(img1[100][150][0] == 0)
        self.assertTrue(img1[200][150][0] == 0)
        
        
if __name__ == '__main__':
    unittest.main()
            
