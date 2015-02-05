__author__ = 'juancarlosfarah'

import srm_lif_neuron
import unittest


class NeuronTests(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        return

    def test_time_delta(self):
        """
        Checks that the function calculate_time_delta returns the correct output
        :return:
        """
        spike_train = np.array([1,0,1,1,0,1,0,0,0])
        time_delta = calculate_time_delta(spike_train)
        self.failUnless(time_delta==4)
        return

    def test_avg_hz_with_noise(self):
        """

        :return:
        """
        #   self.failIf()
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
