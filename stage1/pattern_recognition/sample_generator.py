__author__ = 'Juan Carlos Farah,' \
             'Panagiotis Almpouras'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk,' \
                  'panagiotis.almpouras12@imperial.ac.uk'

import math
import sys
import matplotlib.pylab as mpl
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy


"""
Constants
=========
"""

SEED = 1                        # Seed for the random generator.

# Set seed.
np.random.seed(SEED)


class SampleGenerator:
    """
    Generates sample input spike trains.
    """
    def __init__(self, duration, num_patterns, num_neurons=2000):
        self.duration = duration
        self.num_patterns = num_patterns
        self.num_neurons = num_neurons

        # Initialise containers
        self.spike_trains = np.zeros((num_neurons, duration), dtype=np.float)
        self.start_positions = []

        self.pattern_duration = 50  # Duration of the spike pattern.
        self.dt = 0.001             # Time step in seconds.
        self.rep_ratio = 0.25       # Ratio of pattern in the overall sample.
        self.inv_ratio = 0.5        # Ratio of afferents in the pattern.
        self.noise = 10.0           # Noise in Hz.

        self.r_min = 0.0            # Minimum firing rate in Hz.
        self.r_max = 90.0           # Maximum firing rate in Hz.
        self.s_min = -1800.0        # Minimum negative rate of change in Hz/s.
        self.s_max = 1800.0         # Maximum positive rate of change in Hz/s.
        self.ds_min = -360.0        # Maximum change of rate of change in Hz/s.
        self.ds_max = 360.0         # Maximum change of rate of change in Hz/s.

    def generate_spike_train(self):
        """
        Generates spike train for one neuron.
        :return:
        """

        # Container for spike train.
        spike_train = np.zeros(self.duration)

        # Set initial rate of change.
        s = np.random.uniform(self.s_min, self.s_max)
        r = np.random.uniform(self.r_min, self.r_max)

        for i in range(0, self.duration):

            # Calculate probability of giving a spike at given time step.
            p = r * self.dt

            # Ensure that all afferent spikes at
            # least once every given pattern length.
            if i >= self.pattern_duration:
                spike_sum = np.sum(spike_train[i - self.pattern_duration: i])
            else:
                spike_sum = 1

            if spike_sum < 1:
                spike_train[i] = 1

            # Fire if p is > random number between 0 and 1.
            elif p > np.random.uniform(0, 1):
                spike_train[i] = 1

            # Calculate change in r, apply and clip.
            dr = s * self.dt
            r += dr
            r = min(self.r_max, max(r, self.r_min))

            # Calculate rate of change and clip.
            ds = np.random.uniform(self.ds_min, self.ds_max)
            s += ds
            s = min(self.s_max, max(self.s_min, s))

        return spike_train

    def generate_spike_trains(self):
        """
        Generates spike trains for all the afferents in the sample.
        :return:
        """

        # Container for spike trains.
        spike_trains = np.zeros((self.num_neurons, self.duration))

        for i in range(0, self.num_neurons):
            spike_train = self.generate_spike_train()
            spike_trains[i, :] = spike_train

            # Track progress
            progress = (i / float(self.num_neurons)) * 100
            sys.stdout.write("Generating spike trains: %d%% \r" % progress)
            sys.stdout.flush()

        self.spike_trains = spike_trains

    def generate_pattern(self):
        """

        :param spike_trains:
        :return:
        """

        # Number of neurons involved in the pattern.
        num_neurons = self.num_neurons * self.inv_ratio

        # Identify a pattern of given length.
        start = np.random.randint(0, self.duration - self.pattern_duration)
        end = start + self.pattern_duration

        # Display the pattern.
        pattern = deepcopy(self.spike_trains[:num_neurons, start: end])

        return pattern

    def add_noise(self, spike_train):
        """
        Adds noise to a given spike train.
        :param spike_train: Input spike train.
        :return: Spike train with noise added.
        """

        # Get indices without spikes.
        indices = [i for i, dt in enumerate(spike_train) if dt == 0]

        # Add spikes to indices randomly with given probability.
        p = self.noise * self.dt
        for index in indices:
            if np.random.uniform(0, 1) < p:
                spike_train[index] = 1

        return spike_train

    def generate_sample(self):
        """
        Generates the sample.
        :return:
        """

        # Generate background spike trains.
        self.generate_spike_trains()

        # Generate pattern from spike trains.
        pattern = self.generate_pattern()

        # Get the start positions for the pattern to be inserted.
        starts = self.generate_start_positions()

        # Insert the pattern at start positions.
        num_neurons_in_pattern = self.num_neurons * self.inv_ratio
        for left in starts:
            right = left + self.pattern_duration
            self.spike_trains[:num_neurons_in_pattern, left: right] = pattern

        # Add noise to all spike trains.
        for i in range(self.num_neurons):
            self.spike_trains[i, :] = self.add_noise(self.spike_trains[i, :])

        # Package everything nicely.
        self.start_positions = starts

    def generate_start_positions(self):
        """
        Gets the start position of a repeating pattern within the noise.
        :return: A list of the column indexes where the pattern starts.
        """
        effective_factor = 1.25
        num_buckets = self.duration / self.pattern_duration
        positions = np.random.uniform(0, 1, num_buckets)
        start_positions = []
        count = 0
        effective_ratio = self.rep_ratio * effective_factor
        while count < num_buckets:

            # Mark as bucket and skip next bucket.
            if positions[count] < effective_ratio:
                start_positions.append(count * self.pattern_duration)
                count += 2
            else:
                count += 1

        return start_positions

    """
    def generate_pattern(num_neurons, bg_len, pattern_len=50, seed=SEED):
        # Create the spike trains using a Poisson distribution.
        # Returns a dictionary with the spike trains and the time steps
        # where the pattern begins.
        #
        # :param num_neurons: Number of neurons.
        # :param bg_len: Length in ms of observation period.
        # :param pattern_len: Length in ms of repeating pattern.
        # :param seed: Seed to use for random generation.
        # :return: Pseudo-random-generated observation matrix.

        # Set seed.
        np.random.seed(seed)

        # Ensure that pattern is always shorter than total lengths.
        if pattern_len > bg_len:
            pattern_len = bg_len - 1

        # Create a num_neurons * bg_len matrix that contains
        # values uniformly distributed between 0 and 1.
        vt = np.random.uniform(0, 1, (num_neurons, bg_len))

        spikes = deepcopy(vt)

        # When probability is lower afferent does not spike.
        spikes[vt > F_PROB] = 0

        # When probability is lower afferent spikes.
        spikes[vt < F_PROB] = 1

        # Identify a pattern of given length.
        start = np.random.randint(0, bg_len - pattern_len)

        # Make only half of the neurons display the pattern.
        pattern = deepcopy(spikes[NUM_NEURONS / 2:, start: start + pattern_len])

        # Ensure that all afferents spike at least once in the pattern.
        for i in range(0, pattern.shape[0]):
            spike_sum = np.sum(pattern[i, :])
            if spike_sum < 1:
                rand_col = np.random.randint(0, pattern_len)
                pattern[i, rand_col] = 1

        # Calculate number of times that pattern will be repeated.
        reps = math.floor((bg_len * REPETITION_RATIO) / pattern_len)

        # Get the start positions for the pattern to be inserted.
        start_positions = get_start_positions(pattern_len, bg_len, reps)
        start_positions.sort()

        # Insert the pattern at start positions.
        for left in start_positions:
            right = left + pattern_len
            spikes[NUM_NEURONS / 2:, left: right] = pattern

        rvalue = dict()
        rvalue['spikes'] = spikes
        rvalue['start_positions'] = start_positions

        return rvalue

    def load_sample(filename):
        #TODO: erase this function
        f = open(filename)

        spike_trains = np.array([])
        start_positions = map(int, (f.readline()).split())
        lines = f.read().split('\n')
        num_neurons = len(lines)
        count = 0.0
        for line in lines:
            if line != [] and line != ['\n'] and line != '':
                if spike_trains.size == 0:
                    spike_trains = map(int, line.split())
                    spike_trains = np.reshape(spike_trains, (1, len(spike_trains)))
                else:
                    spike_trains = np.vstack((spike_trains, map(int, line.split())))

            progress = (count / num_neurons) * 100
            sys.stdout.write("Loading spike trains: %d%% \r" % progress)
            sys.stdout.flush()
            count += 1
        f.close()

        # Package everything nicely.
        rvalue = dict()
        rvalue['spike_trains'] = spike_trains
        rvalue['start_positions'] = start_positions

        return rvalue

    def save_sample(filename, sample):
        #TODO: Erase this function
        #Old version
        start_positions = sample['start_positions']
        spike_trains = sample['spike_trains']
        f = open(filename, 'w')
        for start in range(len(start_positions)):
            f.write('%d ' % start_positions[start])
        f.write('\n')

        num_neurons = spike_trains.shape[0]
        for row in range(num_neurons):
            for col in range(spike_trains.shape[1]):
                f.write('%0.1d ' % spike_trains[row, col])
            f.write('\n')
            progress = (row / float(num_neurons)) * 100
            sys.stdout.write("Saving spike trains: %d%% \r" % progress)
            sys.stdout.flush()
        f.write('\n\n')
        f.close()
    """

    def save(self):
        filename = "samples/{}_{}_{}_{}_{}_{}_{}".format(SEED,
                                                         self.num_neurons,
                                                         self.duration,
                                                         self.pattern_duration,
                                                         self.rep_ratio,
                                                         self.inv_ratio,
                                                         self.noise)
        np.savez(filename,
                 start_positions=self.start_positions,
                 spike_trains=self.spike_trains)


# if __name__ == '__main__':
    # sample = generate_sample(NUM_NEURONS, TOTAL_MS, PATTERN_MS)
    # spike_trains = sample['spike_trains']
    # mpl.imshow(spike_trains[0:2000, 0:2000],
    #            interpolation='nearest',
    #            cmap=mpl.cm.Greys)
    # mpl.title('Spike Trains')
    # mpl.ylabel('# Afferent')
    # mpl.xlabel('Time (ms)')
    # mpl.show()
