"""
Unit tests for module CSTMD.
"""
from CSTMD import CSTMD
import unittest
import numpy as np

class TestCSTMD(unittest.TestCase):
    """
    This class represents sequence of tests for class CSTMD.
    """

    def setUp(self):
        """
        Method that runs at start of each test.
        """
        neurons_no = 2
        SYNAPSES_NO = 500
        D = 30
        electrds = 50

        self.cstmd = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D,electrds=electrds)

    def test_run(self):
        frame_list = []
        for i in range(10) :
            frame_list.append(np.zeros([32,32]))

        for frame in frame_list :
            frame = frame.ravel()
            times, ids = self.cstmd.run(time = 10, rates = frame)

if __name__ == '__main__':
    unittest.main()