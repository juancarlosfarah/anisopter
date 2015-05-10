"""
Unit tests for module ESTMD.
"""

import unittest

from estmd.estmd import *


class TestESTMD(unittest.TestCase):
    """
    This class represents sequence of tests for class ESTMD.
    """

    def setUp(self):
        """
        Method that runs at start of each test.
        """

        self.estmd = ESTMD()

    def test_RTC_exp(self):
        input = [0, 1, 0.001, 2]
        expected_result = [0, np.exp(-1), 0, np.exp(-0.5)]

        T_s = 1
        x = np.array(input)
        result = [i for i in self.estmd.rtc_exp(T_s, x)]

        self.assertEqual(result, expected_result)

    def test_open_movie(self):
        wrong_dir = "Random12345.avi"
        correct_dir = "test_movies/test.avi"

        with self.assertRaises(NameError):
            self.estmd.open_movie(wrong_dir)

        self.estmd.open_movie(correct_dir)

    def test_get_next_frame(self):
        input_dir = "test_movies/test.avi"

        result = self.estmd.get_next_frame()
        self.assertEqual(result, False)

        self.estmd.open_movie(input_dir)
        self.estmd.run(by_frame = True)
        img = self.estmd.get_next_frame()
        x, y = img.shape
        self.assertEqual(x, 64)
        self.assertEqual(y, 64)

    def test_run(self):
        input_dir = "test_movies/test.avi"

        result = self.estmd.run(out_dir = "test_result.avi")
        self.assertEqual(result, False)

        self.estmd.open_movie(input_dir)
        result = self.estmd.run(out_dir = "test_result.avi")
        self.assertTrue(result)
        

if __name__ == '__main__':
    unittest.main()
