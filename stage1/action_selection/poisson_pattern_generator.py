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
DT = 0.001                      # Time step in seconds.
SPIKES_PER_S = 64               # spikes per second, on average
F_PROB = SPIKES_PER_S * DT      # probability of a neuron firing in a timestep
TOTAL_MS = 5000               # Length of sample.
SEED = 1                        # Seed for the random generator.
NUM_NEURONS = 2000              # Number of afferents.
PATTERN_MS = 50                 # Duration of the spike pattern.
REPETITION_RATIO = 0.25         # Ratio of pattern in the overall sample.
INVOLVEMENT_RATIO = 0.5         # Ratio of afferents involved in the pattern.
NOISE = 10.0                    # Noise in Hz.

R_MIN = 0.0                     # Minimum firing rate in Hz.
R_MAX = 90.0                    # Maximum firing rate in Hz.
S_MIN = -1800.0                 # Minimum negative rate of change in Hz/s.
S_MAX = 1800.0                  # Maximum positive rate of change in Hz/s.
DS_MIN = -360.0                 # Maximum change of rate of change in Hz/s.
DS_MAX = 360.0                  # Maximum change of rate of change in Hz/s.


def generate_spike_train(duration, period):
    """

    :param duration:
    :param period:
    :return:
    """

    # Container for spike train.
    spike_train = np.zeros(duration)

    # Set initial rate of change.
    s = np.random.uniform(S_MIN, S_MAX)
    r = np.random.uniform(R_MIN, R_MAX)

    for i in range(0, duration):

        # Calculate probability of giving a spike at given time step.
        p = r * DT

        # Ensure that all afferent spikes at least once every given period.
        if i >= period:
            spike_sum = np.sum(spike_train[i - period: i])
        else:
            spike_sum = 1

        if spike_sum < 1:
            spike_train[i] = 1

        # Fire if p is > random number between 0 and 1.
        elif p > np.random.uniform(0, 1):
            spike_train[i] = 1

        # Calculate change in r, apply and clip.
        dr = s * DT
        r += dr
        r = min(R_MAX, max(r, R_MIN))

        # Calculate rate of change and clip.
        ds = np.random.uniform(DS_MIN, DS_MAX)
        s += ds
        s = min(S_MAX, max(S_MIN, s))

    return spike_train


def generate_spike_trains(num_neurons, sample_duration):
    """

    :param num_neurons:
    :param sample_duration:
    :return:
    """

    # Container for spike trains.
    spike_trains = np.zeros((num_neurons, sample_duration))

    for i in range(0, num_neurons):
        spike_train = generate_spike_train(sample_duration, 50)
        spike_trains[i, :] = spike_train

        # Track progress
        progress = (i / float(num_neurons)) * 100
        sys.stdout.write("Generating spike trains: %d%% \r" % progress)
        sys.stdout.flush()

    return spike_trains


def generate_pattern(spike_trains, duration=PATTERN_MS,
                     involvement_ratio=INVOLVEMENT_RATIO):
    """

    :param spike_trains:
    :param duration:
    :param involvement_ratio:
    :return:
    """

    # Number of neurons involved in the pattern.
    num_neurons = spike_trains.shape[0] * involvement_ratio

    # Identify a pattern of given length.
    start = np.random.randint(0, spike_trains.shape[1] - duration)
    end = start + duration

    # Display the pattern.
    pattern = deepcopy(spike_trains[:num_neurons, start: end])

    return pattern


def add_noise(sample, frequency=NOISE):
    """

    :param sample:
    :param frequency:
    :return:
    """

    # Get indices without spikes.
    indices = [i for i, dt in enumerate(sample) if dt == 0]

    # Add spikes to indices randomly with given probability.
    p = frequency * DT
    for index in indices:
        if np.random.uniform(0, 1) < p:
            sample[index] = 1

    return sample


def generate_sample(num_neurons,
                    sample_duration,
                    pattern_duration,
                    involvement_ratio=INVOLVEMENT_RATIO,
                    repetition_ratio=REPETITION_RATIO):
    """

    :param num_neurons:
    :param sample_duration:
    :param pattern_duration:
    :param involvement_ratio:
    :param repetition_ratio:
    :return:
    """

    # Generate background spike trains.
    spike_trains = generate_spike_trains(num_neurons, sample_duration)

    # TODO: Make into warning.
    print sum(sum(spike_trains)) / (num_neurons * sample_duration) / DT

    # Generate pattern from spike trains.
    pattern = generate_pattern(spike_trains,
                               pattern_duration,
                               involvement_ratio)

    # Calculate number of times that pattern will be repeated.
    reps = math.floor((sample_duration * repetition_ratio) / pattern_duration)

    # Get the start positions for the pattern to be inserted.
    starts = get_start_positions(pattern_duration, sample_duration, reps)
    starts.sort()

    # Insert the pattern at start positions.
    num_neurons_in_pattern = num_neurons * involvement_ratio
    for left in starts:
        right = left + pattern_duration
        spike_trains[:num_neurons_in_pattern, left: right] = pattern

    # Add noise to all spike trains.
    for i in range(num_neurons):
        spike_trains[i, :] = add_noise(spike_trains[i, :], NOISE)

    # TODO: Make into warning.
    print sum(sum(spike_trains)) / (num_neurons * sample_duration) / DT

    # Package everything nicely.
    rvalue = dict()
    rvalue['spike_trains'] = spike_trains
    rvalue['start_positions'] = starts

    return rvalue


# Predefined functions in pattern_generator.py
def get_start_positions(pattern_len, bg_len, reps):
    """ Gets the start position of a repeating pattern within the noise.

    :param pattern_len: Length of repeating pattern.
    :param bg_len: Length of total observation period.
    :param reps: Number of repetitions of pattern in the observation period.
    :return: A list of the column indexes where the pattern starts.
    """

    start_positions = []
    upper_limit = bg_len - pattern_len

    # Insert positions into start_positions
    while reps > 0:
        is_valid_start = True
        start_pos = np.random.randint(0, upper_limit)

        # Check that it is a valid start position given
        # the existing start positions in the list.
        for pos in start_positions:
            if math.fabs(pos - start_pos) < pattern_len * 2:
                is_valid_start = False

        # Only insert pos if it is a valid start position.
        if is_valid_start:
            start_positions.append(start_pos)
            reps -= 1

    return start_positions


# def generate_pattern(num_neurons, bg_len, pattern_len=50, seed=SEED):
#     """ Create the spike trains using a Poisson distribution.
#         Returns a dictionary with the spike trains and the time steps where the pattern begins
#
#     :param num_neurons: Number of neurons.
#     :param bg_len: Length in ms of observation period.
#     :param pattern_len: Length in ms of repeating pattern.
#     :param seed: Seed to use for random generation.
#     :return: Pseudo-random-generated observation matrix.
#     """
#
#     # Set seed.
#     np.random.seed(seed)
#
#     # Ensure that pattern is always shorter than total lengths.
#     if pattern_len > bg_len:
#         pattern_len = bg_len - 1
#
#     # Create a num_neurons * bg_len matrix that contains
#     # values uniformly distributed between 0 and 1.
#     vt = np.random.uniform(0, 1, (num_neurons, bg_len))
#
#     spikes = deepcopy(vt)
#
#     # When probability is lower afferent does not spike.
#     spikes[vt > F_PROB] = 0
#
#     # When probability is lower afferent spikes.
#     spikes[vt < F_PROB] = 1
#
#     # Identify a pattern of given length.
#     start = np.random.randint(0, bg_len - pattern_len)
#
#     # Make only half of the neurons display the pattern.
#     pattern = deepcopy(spikes[NUM_NEURONS / 2:, start: start + pattern_len])
#
#     # Ensure that all afferents spike at least once in the pattern.
#     for i in range(0, pattern.shape[0]):
#         spike_sum = np.sum(pattern[i, :])
#         if spike_sum < 1:
#             rand_col = np.random.randint(0, pattern_len)
#             pattern[i, rand_col] = 1
#
#     # Calculate number of times that pattern will be repeated.
#     reps = math.floor((bg_len * REPETITION_RATIO) / pattern_len)
#
#     # Get the start positions for the pattern to be inserted.
#     start_positions = get_start_positions(pattern_len, bg_len, reps)
#     start_positions.sort()
#
#     # Insert the pattern at start positions.
#     for left in start_positions:
#         right = left + pattern_len
#         spikes[NUM_NEURONS / 2:, left: right] = pattern
#
#     rvalue = dict()
#     rvalue['spikes'] = spikes
#     rvalue['start_positions'] = start_positions
#
#     return rvalue

"""
def load_sample(filename):
    #TODO: erase this function 
    f = open(filename)

    spike_trains = np.array([])
    start_positions = map(int, (f.readline()).split())
    lines = f.read().split('\n')

    for line in lines:
        if line != [] and line != ['\n'] and line != '':
            if spike_trains.size == 0:
                spike_trains = map(int, line.split())
                spike_trains = np.reshape(spike_trains, (1, len(spike_trains)))
            else:
                spike_trains = np.vstack((spike_trains, map(int, line.split())))

    f.close()

    # Package everything nicely.
    rvalue = dict()
    rvalue['spike_trains'] = spike_trains
    rvalue['start_positions'] = start_positions

    return rvalue
"""

def load_sample(filename):
    """

    :param filename:
    :return:
    """

    rvalue = np.load(filename)

    return rvalue

"""
def save_sample(filename, sample):
    #TODO: Erase this function    
    #Old version
    start_positions = sample['start_positions']
    spike_trains = sample['spike_trains']
    f = open(filename, 'w')
    for start in range(len(start_positions)):
        f.write('%d ' % start_positions[start])
    f.write('\n')

    for row in range(spike_trains.shape[0]):
        for col in range(spike_trains.shape[1]):
            f.write('%0.1d ' % spike_trains[row, col])
        f.write('\n')
    f.write('\n\n')
    f.close()
"""

def save_sample(filename, sample):
    """
    :param filename:
    :param sample:
    :return:
    """
    start_positions = sample['start_positions']
    spike_trains = sample['spike_trains']
    np.savez(filename,start_positions=start_positions,spike_trains=spike_trains)


if __name__ == '__main__':
    sample = generate_sample(NUM_NEURONS, TOTAL_MS, PATTERN_MS)
    filename = "samples/{}_{}.txt".format(NUM_NEURONS, TOTAL_MS)
    save_sample(filename, sample)

    # spike_trains = sample['spike_trains']
    # mpl.imshow(spike_trains[0:2000, 0:2000],
    #            interpolation='nearest',
    #            cmap=mpl.cm.Greys)
    # mpl.title('Spike Trains')
    # mpl.ylabel('# Afferent')
    # mpl.xlabel('Time (ms)')
    # mpl.show()
