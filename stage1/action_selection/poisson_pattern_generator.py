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

# Set seed.
np.random.seed(SEED)

# STEP 1:
# =======
# Create the spike trains using Poisson distribution:

# create a (NUM_NEURONS x TOTAL_MS) matrix that contains values
# uniformly distributed between 0 and 1:
vt = np.random.uniform(0, 1, (NUM_NEURONS, TOTAL_MS))

spikes = deepcopy(vt)

# when probability is lower afferent does not spike
spikes[vt > F_PROB] = 0

# when probability is lower afferent spikes
spikes[vt < F_PROB] = 1

# STEP 2:
# =======
# Identify a pattern of length = PATTERN_MS
pat_start = np.random.randint(0, TOTAL_MS-PATTERN_MS)
pattern = deepcopy(spikes[:, pat_start:pat_start+PATTERN_MS])

# Ensure that all afferents spike at least once in the pattern
for i in range(0,NUM_NEURONS):
    temp_sum=np.sum(pattern[i, :])
    if temp_sum<1:
        rand_col=np.random.randint(0, PATTERN_MS)
        pattern[i, rand_col] = 1

# Calculate number of times that pattern will be repeated.
reps = math.floor((TOTAL_MS * REPETITION_RATIO) / PATTERN_MS)

# Get the start positions for the pattern to be inserted.
start_positions = get_start_positions(PATTERN_MS, TOTAL_MS, reps)

# Insert the pattern at start positions.
for left in start_positions:
    right = left + PATTERN_MS
    spikes[:, left: right] = pattern

# Create plots, label axes and show.
mpl.imshow(spikes[0:200,0:1000], interpolation='nearest', cmap=mpl.cm.Greys)
mpl.title('Spike Trains')
mpl.ylabel('# Afferent')
mpl.xlabel('Time (ms)')
mpl.show()