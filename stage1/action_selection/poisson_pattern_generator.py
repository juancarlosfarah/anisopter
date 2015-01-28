__author__ = 'Juan Carlos Farah,' \
             'Panagiotis Almpouras'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk,' \
                  'panagiotis.almpouras12@imperial.ac.uk'

import math
import matplotlib.pylab as mpl
import numpy as np
from copy import deepcopy


"""
Constants
=========
"""
TIME_STEP = 0.001               # seconds
SPIKES_PER_S = 50               # spikes per second, on average
F_PROB = SPIKES_PER_S*TIME_STEP # probability of a neuron firing in a timestep
TOTAL_MS = 150000               # length of spike trains
SEED = 1                        # seed for the random
NUM_NEURONS = 2000              # number of afferents
PATTERN_MS = 50                 # length of the spike pattern
REPETITION_RATIO = 0.25         # % of the pattern in the overall spike train


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
        start_pos = np.random.randint(0, upper_limit, 1)

        # Check that it is a valid start position given
        # the existing start positions in the list.
        for pos in start_positions:
            if math.fabs(pos - start_pos) < pattern_len:
                is_valid_start = False

        # Only insert pos if it is a valid start position.
        if is_valid_start:
            start_positions.append(start_pos[0])
            reps -= 1

    return start_positions


def generate_pattern(num_neurons, bg_len, pattern_len=50, seed=SEED):
    """ Create the spike trains using a Poisson distribution.

    :param num_neurons: Number of neurons.
    :param bg_len: Length in ms of observation period.
    :param pattern_len: Length in ms of repeating pattern.
    :param seed: Seed to use for random generation.
    :return: Pseudo-random-generated observation matrix.
    """

    # Set seed.
    np.random.seed(seed)

    # Create a num_neurons * bg_len matrix that contains
    # values uniformly distributed between 0 and 1.
    vt = np.random.uniform(0, 1, (num_neurons, bg_len))

    spikes = deepcopy(vt)

    # When probability is lower afferent does not spike.
    spikes[vt > F_PROB] = 0

    # When probability is lower afferent spikes.
    spikes[vt < F_PROB] = 1

    # Identify a pattern of length = pattern_len.
    pat_start = np.random.randint(0, bg_len - pattern_len)
    pattern = deepcopy(spikes[:, pat_start: pat_start + pattern_len])

    # Ensure that all afferents spike at least once in the pattern.
    for i in range(0, num_neurons):
        temp_sum = np.sum(pattern[i, :])
        if temp_sum < 1:
            rand_col = np.random.randint(0, pattern_len)
            pattern[i, rand_col] = 1

    # Calculate number of times that pattern will be repeated.
    reps = math.floor((bg_len * REPETITION_RATIO) / pattern_len)

    # Get the start positions for the pattern to be inserted.
    start_positions = get_start_positions(pattern_len, bg_len, reps)

    # Insert the pattern at start positions.
    for left in start_positions:
        right = left + pattern_len
        spikes[:, left: right] = pattern

    return spikes

# Create plots, label axes and show.

if __name__ == '__main__':
    spikes = generate_pattern(NUM_NEURONS, TOTAL_MS)
    mpl.imshow(spikes[0:200, 0:1000],
               interpolation='nearest',
               cmap=mpl.cm.Greys)
    mpl.title('Spike Trains')
    mpl.ylabel('# Afferent')
    mpl.xlabel('Time (ms)')
    mpl.show()