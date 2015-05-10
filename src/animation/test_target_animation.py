"""
Unit tests for module Target_animation.
"""

import unittest
from animation.target_animation import *


class TestDragonfly(unittest.TestCase):
    """
    This class represents sequence of tests for class Dragonfly.
    """
    def setUp(self):
        """
        Method that runs at start of each test.
        """

        self.path = [[5, 5, 0.0], [10, 10, 0.5], [15, 15, 1.0]]
        self.dragon = Dragonfly(self.path)

    def test_init(self):
        self.assertEqual(self.dragon.pos, [5, 5])
        self.assertEqual(self.dragon.path, self.path)

    def test_get_position(self):
        time = 0.6
        loc = self.dragon.get_position(time)
        self.assertEqual(loc, [15, 15])

    def update(self):
        time = 0.6
        self.dragon.update(time)
        self.assertEqual(self.dragon.pos, [15, 15])


class TestBackground(unittest.TestCase):
    """
    This class represents sequence of tests for class Background.
    """

    def setUp(self):
        bg_dir = "images/test.jpg"
        self.bg = Background(bg_dir, 5)

    def test_init(self):
        self.assertEqual(self.bg.pos, [0, 0])

    def test_update(self):
        self.bg.update()
        self.assertEqual(self.bg.pos, [5, 5])


class TestTarget(unittest.TestCase):
    """
    This class represents sequence of tests for class Target.
    """

    def setUp(self):
        """
        Method that runs at start of each test.
        """
        pass
        
    def test_init(self):
        """
        Tests constructor of class Target.
        It tests that all attributes were set as expected.
        """
        
        type = 1
        start = [0, 0]
        vel = [1, 1]
        v = 5
        size = 10
        color = [0, 1, 2]
        
        target = Target(type, start, vel, v, size, color)
        
        self.assertEqual(target.type, type)
        self.assertEqual(target.start, start)
        self.assertEqual(target.pos, start)
        self.assertEqual(target.velocity, vel)
        self.assertEqual(target.v, v)
        self.assertEqual(target.size, size)
        self.assertEqual(target.color, color)
    
    def test_change_position(self):
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
        
    def test_next_position(self):
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

        target1 = Target(2, [0, 0], [0, 0], 5, 5, [0, 1, 2])
        target2 = Target(1, [0, 0], [1, 1], 5, 5, [0, 1, 2])
        target3 = Target(2, [0, 0], [0, 1], 5, 5, [0, 1, 2])
        target4 = Target(2, [0, 0], [1, 0], 5, 5, [0, 1, 2])
        target5 = Target(2, [0, 0], [1, 1], 5, 5, [0, 1, 2])
        
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

    def test_get_pos(self):
        target1 = Target(2, [0, 0], [0, 0], 5, 5, [0, 1, 2])
        target2 = Target(2, [0, 0], [1, 0], 5, 5, [0, 1, 2])
        target3 = Target(1, [5, 5])

        pos1 = target1.get_pos(5)
        pos2 = target2.get_pos(5)
        pos3 = target3.get_pos(5)

        self.assertEqual(pos1, [0, 0])
        self.assertEqual(pos2, [25, 0])
        self.assertEqual(pos3, [5, 5])


class TestAnimationWindow(unittest.TestCase):
    """
    This class represents sequence of tests for class AnimationWindow.
    """

    def setUp(self):
        """
        Method that runs at start of each test.
        """
        target1 = Target(1, [150, 150], [1, 1], 5, 5, [0, 0, 0])
        target2 = Target(2, [250, 250], [1, 1], 5, 5, [0, 0, 0])
        bg_dir = "images/test.jpg"
        path = [[5, 5, 0.0], [10, 10, 0.5], [15, 15, 1.0]]

        self.targets = [target1, target2]
        self.bg = Background(bg_dir)
        self.d_fly = Dragonfly(path)

        self.aw = AnimationWindow(self.targets, 640, 480, self.bg, self.d_fly)

    def test_init(self):
        self.assertEqual(self.aw.N, 2)
        self.assertEqual(self.aw.time, 0)

    def test_update_frame(self):
        """
        TO DO!
        """
        self.aw.update_frame(0.0)

    def test_draw(self):
        """
        TO DO!
        """
        self.aw.draw()
        img_name = "temp/scr" + str(self.aw.time) + ".png"
        self.assertTrue(os.path.exists(img_name))


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
        self.assertEqual(self.animation.bg, False)

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

        self.animation.add_target(1)
        target1 = Target(1, [0, 0], [1, 1], 5, 10, [0, 0, 0])

        self.animation.add_target(2, [10, 10])
        target2 = Target(2, [10, 10], [1, 1], 5, 10, [0, 0, 0])
        
        target_list = [target1, target2]
        target_list2 = self.animation.target_list
        
        self.assertEqual(self.animation.target_list, target_list)

    def test_add_dragonfly(self):
        """
        Tests if dragonfly is added.
        """

        path = [[5, 5, 0.5], [1, 1, 1.0]]

        self.animation.add_dragonfly(path)
        self.assertTrue(self.animation.dragonfly)

    def test_add_background(self):
        """
        Tests if background is added.
        """
        
        bg_image = "images/test.jpg"
    
        self.animation.add_background(bg_image)
        self.assertTrue(self.animation.bg)

    def test_get_target_position(self):
        """
        Tests if get target positions returns correct positions.
        """

        pos1 = [1, 1]
        pos2 = [3, 5]
        real_positions = [pos1, pos2]

        self.animation.add_target(2, pos1)
        self.animation.add_target(2, pos2)
        calc_positions = self.animation.get_targets_positions(0)
        
        self.assertEqual(real_positions, calc_positions)

    def test_run(self):
        """
        Tests if program runs and if it produces output.
        """
        out_directory = "result.test1.avi"
        self.animation.run(out_directory, 10, 10)
        self.assertTrue(os.path.exists(out_directory))


if __name__ == '__main__':
    unittest.main()
