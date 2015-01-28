__author__ = 'Juan Carlos Farah, Panagiotis Almpouras'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk, panagiotis.almpouras12@imperial.ac.uk'

import math
import matplotlib.pylab as mpl
import numpy as np
from copy import deepcopy

"""
Constants
=========
These constants are based on Masquelier et al. (2008). Based on the
this paper, each column in the pattern matrix represents 1ms with its
corresponding vector denoting which neurons fired or not by a 1 or 0,
respectively. Each row represents the firing pattern of a neuron over
150s. The repetition ratio means what percentage of the total matrix
is covered by the pattern. We use 25% as recommended by the authors.
"""
SEED = 1
SEED_MODIFIER = 25
NUM_NEURONS = 2000
TOTAL_MS = 150000
PATTERN_MS = 50
REPETITION_RATIO = 0.25
PLOT_TIME_START = 0
PLOT_TIME_END = 2000
NOISE_FACTOR = 0.1


def generate_random_matrix(rows, cols, seed):
    """ Generates a random matrix given a seed.

    :param rows: Number of rows.
    :param cols: Number of columns.
    :param seed: Seed to use for random generation.
    :return: Pseudo-random-generated matrix.
    """

    np.random.seed(seed)
    return np.random.random_integers(0, 1, (rows, cols))


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


def generate_pattern(neurons, bg_len, pattern_len, seed):
    """ Generate an observation matrix with an embedded repeating pattern.

    :param neurons: Number of neurons.
    :param bg_len: Length in ms of observation period.
    :param pattern_len: Length in ms of repeating pattern.
    :param seed: Seed to use for random generation.
    :return: Pseudo-random-generated observation matrix.
    """

    # Create dictionary for return value.
    rvalue = {}

    # Generate a noise matrix as a background.
    noise = generate_random_matrix(neurons, bg_len, seed)

    # Modify seed and generate a pattern matrix.
    pattern_seed = seed * SEED_MODIFIER
    pattern = generate_random_matrix(neurons, pattern_len, pattern_seed)
    rvalue['pattern'] = pattern

    # Calculate number of times that pattern will be repeated.
    reps = math.floor((bg_len * REPETITION_RATIO) / pattern_len)
    rvalue['reps'] = reps

    # Get pseudo-random start positions for the pattern.
    start_positions = get_start_positions(pattern_len, bg_len, reps)
    rvalue['start_positions'] = start_positions

    # Insert the pattern at start positions.
    for left in start_positions:
        right = left + pattern_len
        noise[:, left: right] = pattern

    rvalue['spike_trains'] = noise

    return rvalue


def plot_pattern(pattern, start=PLOT_TIME_START, end=PLOT_TIME_END):
    """ Plots a given time span of a given pattern.

    :param pattern: Pattern to plot.
    :param start: Start time in ms.
    :param end: End time in ms.
    :return:
    """

    # Get subset of pattern.
    sp = pattern[:, start:end]

    # Create figure, label axes and show.
    f = mpl.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.set_aspect('equal')
    mpl.imshow(sp, interpolation='nearest', cmap=mpl.cm.Greys)
    mpl.ylabel('# Afferent')
    mpl.xlabel('Time (ms)')
    mpl.show()


def add_noise_to_pattern(pattern, probability):
    """ Adds noise to a given pattern.

    :param pattern: Matrix representation of pattern.
    :param probability: Probability of a given neuron to not fire when it should.
    :return: Matrix representation of pattern with noise.
    """

    # Reshape copy of pattern to one-dimensional array.
    num_rows = pattern.shape[0]
    num_cols = pattern.shape[1]
    num_elem = num_rows * num_cols
    copy = pattern.copy()
    flat = np.reshape(copy, num_elem)

    # Get indices with spikes.
    indices = np.where(flat == 1)[0]

    # Remove indices randomly with given probability.
    removed_indices = indices[np.random.rand(*indices.shape) < probability]
    flat[removed_indices] = 0

    # Reshape pattern into matrix and return.
    noisy_pattern = np.reshape(flat, (num_rows, num_cols))
    return noisy_pattern


def add_noise(obj, probability):
    """ Adds noise to given spike trains.

    :param obj: Object with the spike trains and metadata.
    :param probability: Probability of a given neuron to not fire when it should.
    :return: Matrix representation of spike trains with noise.
    """

    # Extract information from object.
    noisy_spike_trains = obj['spike_trains']
    pattern = obj['pattern']
    pattern_len = pattern.shape[1]
    start_positions = obj['start_positions']

    # Add version of noisy pattern to each start point.
    for left in start_positions:
        noisy_pattern = add_noise_to_pattern(pattern, probability)
        right = left + pattern_len
        noisy_spike_trains[:, left: right] = noisy_pattern

    return noisy_spike_trains


def plot_patterns(pattern1, pattern2, start=PLOT_TIME_START, end=PLOT_TIME_END):
    """ Plots a given time span of two given patterns.

    :param pattern1: Left pattern to plot.
    :param pattern1: Right pattern to plot.
    :param start: Start time in ms.
    :param end: End time in ms.
    :return:
    """

    # Get subset of patterns.
    sp1 = pattern1[:, start:end]
    sp2 = pattern2[:, start:end]

    # Create plots, label axes and show.
    mpl.subplot(1, 2, 1)
    mpl.imshow(sp1, interpolation='nearest', cmap=mpl.cm.Greys)
    mpl.title('Spike Trains')
    mpl.ylabel('# Afferent')
    mpl.xlabel('Time (ms)')
    mpl.subplot(1, 2, 2)
    mpl.imshow(sp2, interpolation='nearest', cmap=mpl.cm.Greys)
    mpl.title('Spike Trains with Noise')
    mpl.show()


def single_train():
    """ Creates a spike train of 6 spikes in 80ms
        Goal is to replicate Figure 3 from Masquieller et al. 2008
    """
    #create array of length 80 filled with zeros
    single_spike_train = [0]*80

    #create array of timesteps for which there will be a spike
    spike_times = [2, 24, 46, 47, 49, 61]

    #make the neuron fire at each time step
    for i in spike_times:
        single_spike_train[i] = 1

    return single_spike_train



if __name__ == '__main__':

    spike_train=single_train()
    for i in spike_train:
        print spike_train[i]
# Plot sample spike trains pattern with and without noise.
# o = generate_pattern(NUM_NEURONS, TOTAL_MS, PATTERN_MS, SEED)
# p1 = o['spike_trains']
# copy = deepcopy(o)
# p2 = add_noise(copy, NOISE_FACTOR)
# plot_patterns(p1, p2)
