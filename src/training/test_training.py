__author__ = 'eg1114'


import unittest
import os

from training import training as tr


class TestTraining(unittest.TestCase):
    """
    This class represents sequence of tests for class Training.
    Methods named "test_some_name" tests method "some_name" in class Training.
    """

    def setUp(self):
        """
        Function that runs at beginning of each test.
        :return:
        """

        self.t = tr.Training()

    def test_init(self):
        """
        Tests of constructor created objected.
        :return:
        """

        self.assertTrue(self.t)

    def test_make_temp_directory(self):
        """

        :return:
        """

        name = "abcdefgh12345"
        if not os.path.exists(name):
            os.makedirs(name)
        open(name+"/dummy.txt", 'a').close()

        tr.Training.make_temp_directory(name)
        content = os.listdir(name)

        self.assertTrue(os.path.exists(name))
        self.assertEqual(content, [])


if __name__ == '__main__':
    unittest.main()