__author__ = 'juancarlosfarah'

import unittest
import math

from stage1.pattern_recognition import sample_generator as sg
import numpy as np


class SampleGeneratorTests(unittest.TestCase):

    def setUp(self):
        """
        Creates a sample to test on.
        :return: None.
        """
        # Generate Sample
        sample_duration = 5000
        num_neurons = 500
        self.sample = sg.SampleGenerator(sample_duration,
                                         num_neurons=num_neurons)
        self.sample.generate_sample()

    def test_pattern_duration(self):
        """
        Tests if the pattern duration property matches the length
        of the first pattern in the patterns property.
        :return: None.
        """

        # Create and insert patterns.
        self.sample.generate_patterns(num_patterns=1)
        self.sample.insert_patterns()

        target_duration = self.sample.pattern_duration
        actual_duration = self.sample.patterns[0].shape[1]

        print ""
        print "Pattern Duration"
        print "================"
        print "Expected: ", target_duration
        print "Actual:   ", actual_duration
        print ""

    def test_avg_hz(self):
        """
        Tests if the sample has the appropriate average firing rate.
        :return: None.
        """

        # Set up.
        dt = 0.001
        bin_size = 10
        target_rate = 54.0
        target_sigma = 2.0
        threshold = 100
        firing_rates = []

        spike_trains = self.sample.spike_trains
        num_neurons = self.sample.num_neurons

        # Sample rate over time bins.
        for i in range(0, spike_trains.shape[1] - bin_size, bin_size):
            total_spikes = np.sum(np.sum(spike_trains[:, i: i + bin_size]))
            actual_rate = total_spikes / (num_neurons * bin_size) / dt
            firing_rates.append(actual_rate)

        # Calculate mean and standard deviation.
        mean_rate = np.mean(firing_rates)
        actual_sigma = np.std(firing_rates)

        # Print Mean and Standard Deviation
        print ""
        print "Mean Firing Rate without Noise"
        print "================================"
        print "Expected: ", target_rate
        print "Actual:   ", actual_rate
        print ""
        print "Standard Deviation"
        print "=================="
        print "Expected: ", target_sigma
        print "Actual:   ", actual_sigma
        print ""

        # Ensure that the actual figures are within the threshold.
        self.failUnless(math.fabs(target_rate - mean_rate) < threshold)
        self.failUnless(math.fabs(target_sigma - actual_sigma) < threshold)
        return

    def test_avg_hz_with_noise(self):
        """
        Tests the average firing rate of the sample with noise.
        :return: None.
        """

        # Set up.
        dt = 0.001
        bin_size = 10
        target_rate = 64.0
        target_sigma = 2.0
        threshold = 100
        firing_rates = []

        spike_trains = self.sample.spike_trains
        num_neurons = self.sample.num_neurons

        # Add noise.
        self.sample.add_noise()

        # Sample rate over time bins.
        for i in range(0, spike_trains.shape[1] - bin_size, bin_size):
            total_spikes = np.sum(np.sum(spike_trains[:, i: i + bin_size]))
            actual_rate = total_spikes / (num_neurons * bin_size) / dt
            firing_rates.append(actual_rate)

        # Calculate mean and standard deviation.
        mean_rate = np.mean(firing_rates)
        actual_sigma = np.std(firing_rates)

        # Print Mean and Standard Deviation
        print ""
        print "Mean Firing Rate with Noise"
        print "==========================="
        print "Expected: ", target_rate
        print "Actual:   ", actual_rate
        print ""
        print "Standard Deviation"
        print "=================="
        print "Expected: ", target_sigma
        print "Actual:   ", actual_sigma

        # Ensure that the actual figures are within the threshold.
        self.failUnless(math.fabs(target_rate - mean_rate) < threshold)
        self.failUnless(math.fabs(target_sigma - actual_sigma) < threshold)
        return

    def spacing(self):
        """

        :return:
        """
        return

    def tearDown(self):
        """
        Resets the sample for the tests.
        :return:
        """
        self.sample = None


def main():
    unittest.main()

if __name__ == '__main__':
    main()