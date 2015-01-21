__author__ = 'Juan Carlos Farah, Panagiotis Almpouras'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk, panagiotis.almpouras12@imperial.ac.uk'

import math
import numpy as np

"""
Constants
=========
These constants are based on (Masquelier et al. 2008). Based on the
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
PATTEN_MS = 50
REPETITION_RATIO = 0.25


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
            reps = reps - 1

    return start_positions


def generate_pattern(neurons, bg_len, pattern_len, seed):
    """ Generate a observation matrix with an embedded repeating pattern.

    :param neurons: Number of neurons.
    :param bg_len: Length in ms of observation period.
    :param pattern_len: Length in ms of repeating pattern.
    :param seed: Seed to use for random generation.
    :return: Pseudo-random-generated observation matrix.
    """

    # Generate a noise matrix as a background.
    noise = generate_random_matrix(neurons, bg_len, seed)

    # Modify seed and generate a pattern matrix.
    pattern_seed = seed * SEED_MODIFIER
    pattern = generate_random_matrix(neurons, pattern_len, pattern_seed)

    # Calculate number of times that pattern will be repeated.
    reps = math.floor((bg_len * REPETITION_RATIO) / pattern_len)

    # Get pseudo-random start positions for the pattern.
    start_positions = get_start_positions(pattern_len, bg_len, reps)

    # Insert the pattern at start positions.
    for left in start_positions:
        right = left + pattern_len
        noise[:, left: right] = pattern

    return noise

# Sample print the matrix to the console.
print generate_pattern(NUM_NEURONS, TOTAL_MS, PATTEN_MS, SEED)