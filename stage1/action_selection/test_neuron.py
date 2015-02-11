__author__ = 'juancarlosfarah'

import srm_lif_neuron
import numpy as np
import math
import unittest


class NeuronTests(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        return

    def test_time_delta(self):
        """
        Checks that srm_lif_neuron.calculate_time_delta 
        returns the correct output
        :return:
        """
        spike_train = np.array([1,0,1,1,0,1,0,0,0])
        time_delta = srm_lif_neuron.calculate_time_delta(spike_train)
        self.failUnless(time_delta==-3)
        return

    def test_ltp(self):
        """
        Checks srm_lif_neuron.calculate_ltp returns the correct output
        :return:
        """
        ltp = srm_lif_neuron.calculate_ltp(-3)
        tolerance = math.fabs(ltp-0.0261395096029)
        self.failIf(tolerance>0.000001)
        return

    def test_ltd(self):
        """
        Checks srm_lif_neuron.calculate_ltd returns the correct output
        :return:
        """
        ltd = srm_lif_neuron.calculate_ltd(3)
        tolerance = math.fabs(ltd+0.0243000807934)
        self.failIf(tolerance>0.000001)
        return

    def test_heavy_side(self):
        """
        Checks srm_lif_neuron.calculate_heavy_side_step returns the correct output
        :return:
        """
        pos_val = 1
        neg_val = -1
        pos_result = srm_lif_neuron.calculate_heavyside_step(pos_val)
        self.failIf(pos_result != 1)
        neg_result = srm_lif_neuron.calculate_heavyside_step(neg_val)
        self.failIf(pos_result != 0)
        return

    def tearDown(self):
        """

        :return:
        """
        return


def main():
    unittest.main()

if __name__ == '__main__':
    main()
