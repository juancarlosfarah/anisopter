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

    def test_run(self):
        """
        This method tests ActionSelection's run.
        """

        self.dummy_as.run()

        # Dummy test.
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()