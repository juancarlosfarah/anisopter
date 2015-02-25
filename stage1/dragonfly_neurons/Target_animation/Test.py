"""
Unit tests for module Target_animation.py.
"""

import unittest
from Target_animation import *


class TestSequenceFunctions(unittest.TestCase):
    """
    This class represents sequence of tests for module Target_animation.
    """

    def setUp(self):
        """
        Method that runs at start each time.
        """
        pass
        
    def test_Target_init(self):
        """
        Tests constructor of class Target.
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
       
       
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
