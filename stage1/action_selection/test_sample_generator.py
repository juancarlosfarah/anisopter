__author__ = 'juancarlosfarah'

import unittest
import poisson_pattern_generator as sg
import numpy as np
import math


class SampleGeneratorTests(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        return

    def test_avg_hz(self):
        """ Tests if the sample has the appropriate average firing rate.

        :return: Void.
        """

        # Set up.
        dt = 0.001
        num_neurons = 2000
        sample_duration = 5000
        bin_size = 10
        target_rate = 54.0
        target_sigma = 2.0
        threshold = 100
        firing_rates = []
        spike_trains = sg.generate_spike_trains(num_neurons, sample_duration)

        # Sample rate over time bins.
        for i in range(0, spike_trains.shape[1] - bin_size, bin_size):
            total_spikes = np.sum(np.sum(spike_trains[:, i: i + bin_size]))
            actual_rate = total_spikes / (num_neurons * bin_size) / dt
            firing_rates.append(actual_rate)

        # Calculate mean and standard deviation.
        mean_rate = np.mean(firing_rates)
        actual_sigma = np.std(firing_rates)

        # Ensure that the actual figures are within the threshold.
        self.failUnless(math.fabs(target_rate - mean_rate) < threshold)
        self.failUnless(math.fabs(target_sigma - actual_sigma) < threshold)
        return

    def test_avg_hz_with_noise(self):
        """

        :return:
        """
        #   self.failIf()
        return

    def spacing(self):
        """

        :return:
        """
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