"""
Unit tests for module Target_animation.
"""

import unittest

from src.animation.target_animation import *


class TestTarget(unittest.TestCase):
    """
    This class represents sequence of tests for class Target.
    """

    def setUp(self):
        """
        Method that runs at start of each test.
        """
        pass
        
    def test_Target_init(self):
        """
        Tests constructor of class Target.
        It tests that all attributes were set as expected.
        """
        
        type = 1
        start = [0, 0]
        end = [10, 10]
        v = 5
        size = 10
        color = [0, 1, 2]
        
        target = Target(type, start, end, v, size, color)
        
        self.assertEqual(target.type, type)
        self.assertEqual(target.start, start)
        self.assertEqual(target.pos, start)
        self.assertEqual(target.end, end)
        self.assertEqual(target.v, v)
        self.assertEqual(target.size, size)
        self.assertEqual(target.color, color)
    
    def test_Target_change_position(self):
        """
        Tests Target's method change_position.
        """
        
        self.target1 = Target(0, [0, 0], [100, 100], 5, 5, [0, 1, 2])
        
        self.assertEqual(self.target1.pos, [0, 0])
        self.target1.change_position(5, 5)
        self.assertEqual(self.target1.pos, [5, 5])
        self.target1.change_position(5, 5)
        self.assertEqual(self.target1.pos, [10, 10])
        self.target1.change_position(5, 5)
        self.assertEqual(self.target1.pos, [15, 15])
        self.target1.change_position(10, 5)
        self.assertEqual(self.target1.pos, [25, 20])
        
    def test_Target_next_position(self):
        """
        Tests Target's method next_position.
        It tests 5 different movements:
            - Stationary fly stays stationary.
            - Random fly doesn't move randomly more than it should.
            - Straight moving fly moves right.
            - Straight moving fly moves up.
            - Straight moving fly moves diagonally.
            
        We use eps of 1e-8 to allow some floating precision error.
        """
        
        eps = 1e-8
        
        target1 = Target(0, [0, 0], [100, 100], 5, 5, [0, 1, 2])
        target2 = Target(1, [0, 0], [100, 100], 5, 5, [0, 1, 2])
        target3 = Target(2, [0, 0], [0, 100], 5, 5, [0, 1, 2])
        target4 = Target(2, [0, 0], [100, 0], 5, 5, [0, 1, 2])
        target5 = Target(2, [0, 0], [100, 100], 5, 5, [0, 1, 2])
        
        target1.next_position()
        self.assertEqual(target1.pos, [0, 0])
        target2.next_position()
        pos_change = target2.pos
        self.assertTrue(pos_change[0] <= 5 and pos_change[1] <= 5)
        target3.next_position()
        self.assertTrue(abs(target3.pos[0] - 0) < eps)
        self.assertTrue(abs(target3.pos[1] - 5) < eps)
        target4.next_position()
        self.assertTrue(abs(target4.pos[0] - 5) < eps)
        self.assertTrue(abs(target4.pos[1] - 0) < eps)
        target5.next_position()
        self.assertTrue(abs(target5.pos[0] - sqrt(25.0/2)) < eps)
        self.assertTrue(abs(target5.pos[1] - sqrt(25.0/2)) < eps)
       
        
class TestAnimationWindow(unittest.TestCase):
    """
    This class represents sequence of tests for class AnimationWindow.
    """
            
    def make_window1(self):
        self.window = AnimationWindow(self.target_list, self.width, self.height, 
                                      self.bg_image, self.bg_speed)
    
    def make_window2(self):
        self.window2 = AnimationWindow(self.target_list, self.width, 
                                       self.height, False, 0)
    
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
        self.bg_image = "images/test.jpg"
        self.bg_speed = 5
        
        self.make_window1()
        self.make_window2()
                                       
    def tearDown(self):
        """
        Method that runs at the end of each test.
        """
        
        self.window.close()
        self.window2.close()
            
    def test_AnimationWindow_init(self):
        """
        Tests constructor of class AnimationWindow constructor.
        It tests that all attributes were set as expected.
        """

        self.assertEqual(self.window.bg_image, self.bg_image)
        self.assertEqual(self.window.bg_speed, self.bg_speed)
        self.assertEqual(self.window.target_list, self.target_list)
        self.assertEqual(self.window.N, self.N)
        self.assertEqual(self.window.time, 0)
        self.assertTrue(self.window.background)
        
        self.assertEqual(self.window2.bg_image, False)
        with self.assertRaises(AttributeError):
             self.window2.background
        
    def test_update_frames(self):
        """
        Tests if AnimationWindow's method update_frames works correctly.
        Assumption is made that Target's method next_position works correctly.
        """
        
        self.window.update_frames(0)
        self.target0.next_position()
        self.target1.next_position()
        self.target2.next_position()
        
        self.assertEqual(self.target_list, self.window.target_list)


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
        self.bg_image = "images/test.jpg"
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

        # First run animation without background.
        self.make_directory("temp")
        
        pyglet.clock.schedule_once(self.window.update_frames, 0.001)
        pyglet.clock.schedule_once(self.window.stop, 0.001)
        pyglet.app.run()

        self.assertEqual(self.window.time, 2)
        
        img1 = cv2.imread("temp/scr0.png")
        for i in range(1):
            x = self.height - self.pos[i][0] - 1
            y = self.pos[i][1]

            self.assertTrue(img1[x][y][0] == 0)

        self.assertTrue(img1[100][150][0] > 0)
        self.assertTrue(img1[200][150][0] > 0)

        # Second run animation with background.
        self.window.close()

        self.window2 = AnimationWindow(self.target_list, self.width,
                                       self.height, self.bg_image,
                                       self.bg_speed)

        pyglet.clock.schedule_once(self.window2.update_frames, 0.001)
        pyglet.clock.schedule_once(self.window2.stop, 0.001)
        pyglet.app.run()

        img1 = cv2.imread("temp/scr0.png")
        for i in range(1):
            x = self.height - self.pos[i][0] - 1
            y = self.pos[i][1]

            self.assertTrue(img1[x][y][0] == 0)
        

class TestAnimation(unittest.TestCase):
    """
    This class represents sequence of tests for class Animation.
    """
    
    def setUp(self):
        """
        Method that runs at the start of each test.
        """
        
        self.width = 640
        self.height = 480
        self.animation = Animation(self.width, self.height)
  
    def test_init(self):
        """
        Test constructor.
        """
        
        self.assertEqual(self.animation.target_list, [])
        self.assertEqual(self.animation.width, self.width)
        self.assertEqual(self.animation.height, self.height)
        self.assertEqual(self.animation.bg_image, False)
        self.assertEqual(self.animation.bg_speed, 0)
        
    def test_make_directory(self):
        """
        Tests if make_directory actually creates directory.
        """
    
        random_dir_name = "aaabbbcccdddeeefffghijkl"
        self.animation.make_directory(random_dir_name)
        self.assertTrue(os.path.exists(random_dir_name))
        self.animation.make_directory(random_dir_name)
        os.rmdir(random_dir_name)
        
    def test_add_target(self):
        """
        Tests if target is added.
        """
    
        self.animation.add_target(0)
        target1 = Target(0, [0, 0], [100, 100], 5, 10, [0, 0, 0])
        self.animation.add_target(1, start=[10, 10])
        target2 = Target(1, [10, 10], [100, 100], 5, 10, [0, 0, 0])
        
        target_list = [target1, target2]
        target_list2 = self.animation.target_list
        
        self.assertEqual(self.animation.target_list, target_list)
        
    def test_add_background(self):
        """
        Tests if background is added.
        """
        
        bg_image = "random_test"
        bg_speed = 123
    
        self.animation.add_background(bg_image, bg_speed)
        self.assertEqual(self.animation.bg_image, bg_image)
        self.assertEqual(self.animation.bg_speed, bg_speed)
        
    def test_run(self):
        out_directory = "result.test1.avi"
        self.animation.run(out_directory, 10, 10)
        self.assertTrue(os.path.exists(out_directory))
    
    
if __name__ == '__main__':
    unittest.main()
