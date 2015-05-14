__author__ = 'eg1114'


import unittest
from action_selection.action_selection import *


class TestActionSelection(unittest.TestCase):
    """
    This class represents sequence of tests for class ActionSelection.
    """

    def setUp(self):
        """
        This method runs at start of each test.
        """
        self.dummy_as = ActionSelection()

    def test_general(self):
        """
        This method covers most of ActionSelection code.
        """

        self.dummy_as.run()
        self.dummy_as.save_plots("temp")
        self.dummy_as.animation.run("test1.avi", 10, 10)


if __name__ == '__main__':
    unittest.main()