__author__ = 'Juan Carlos Farah,' \
             'Panagiotis Almpouras,' \
             'Erik Grabljevec'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk,' \
                  'panagiotis.almpouras12@imperial.ac.uk,' \
                  'erik.grabljevec14@imperial.ac.uk'

import numpy as np
import pylab
import math

"""
Simulate a leaky integrate-and-fire (LIF) neuron following the
Gerstner's Spike Response Model (SRM). As a basis we are using
the parameters from Masquelier et al. (2008).
"""

# Constants
T_MIN = 0                   # Start time.
TAU_M = 10.0                # Membrane time constant in ms.
TAU_S = 2.5                 # Synapse time constant in ms.
THETA = 500                 # Threshold in arbitrary units.
K = 1                       # Multiplicative constant.
K1 = 2                      # Constant for positive pulse.
K2 = 4                      # Constant for negative spike after-potential.
T_WINDOW = int(TAU_M * 7)   # Maximum time that a spike can affect EPSP.
T_PLUS = 16.8               # LTP synaptic modification constant in ms.
T_MINUS = 33.7              # LTP synaptic modification constant in ms.
A_PLUS = 0.03125            # LTP learning rate.
A_MINUS = 0.85 * A_PLUS     # LTD learning rate.
LTP_WINDOW = -7 * T_PLUS    # LTP learning window.
LTD_WINDOW = 7 * T_MIN      # LTD learning window.

# Set Seed
np.random.seed(1)

# Sample Neuron
# =============
# TODO: Make this a class
# Container for EPSP input contributions of each afferent.
epsp_inputs = np.array([])


def get_epsilons():
    """ Returns a vector with epsilon values relevant for EPSP.

    :return: Vector of epsilon values in time window.
    """
    epsilons = np.ndarray((T_WINDOW, 1), dtype=float)
    for i in range(0, T_WINDOW):
        delta = T_WINDOW - i
        hss = heavyside_step(delta)
        left_exp = math.exp(-delta / TAU_M)
        right_exp = math.exp(-delta / TAU_S)
        epsilon = K * (left_exp - right_exp) * hss
        epsilons[i, 0] = epsilon

    return epsilons


# TODO: Finish.
def update_weights(weights):
    """ Updates the weights according to STDP.

    :param weights: Current weight vector.
    :return: Updated weight vector.
    """

    # Get new weights.
    num_weights = weights.shape[1]
    new_weights = np.ndarray(shape=(5, 1), dtype=float)
    weights = np.hstack((weights, new_weights))
    return weights


# TODO: Implement.
def get_ltp():
    """ Calculate weight change according to LTP.

    :return:
    """
    return 1


def heavyside_step(delta):
    """ Calculate value of heavyside step for a given time delta.

    :param delta: Time difference.
    :return:
    """
    if delta >= 0:
        return 1
    else:
        return 0


def update_epsp_inputs(epsps, spikes, weights):
    """ Given vectors of spikes and weights update the EPSP contributions.

    :param epsps: Matrix of current EPSP inputs.
    :param spikes: Vector of current spikes.
    :param weights: Vector of current synaptic weights.
    :return:
    """
    weighted = np.multiply(spikes, weights)
    if epsps.size == 0:
        epsps = weighted
    else:
        epsps = np.hstack((epsps, weighted))

    width = epsps.shape[1]
    if width > 10:
        window_start = width - 10
        epsps = epsps[:, window_start:width]

    return epsps


def get_epsp_sum(epsps, epsilons):
    """ Sum the EPSP contribution of all afferents.

    :param epsps: Matrix of current EPSP inputs.
    :param epsilons: Vector of epsilon values in time window.
    :return:
    """

    # Only consider as many epsilons as we have input.
    input_width = epsps.shape[1]
    epsilon_height = epsilons.shape[0]
    start = epsilon_height - input_width

    # Get weighted EPSP contributions.
    weighted = np.matrix(epsps) * np.matrix(epsilons[start:])

    # Return sum of weighted contributions.
    return np.sum(weighted)


def get_psp(time, last_spike):
    """ Calculate the effect of a post-synaptic spike on the potential.

    :param time: Current time in ms.
    :param last_spike: Time of last spike of post-synaptic neuron.
    :return: Value of the effect.
    """
    delta = time - last_spike
    hss = heavyside_step(delta)
    left_exp = math.exp(-delta / TAU_M)
    right_exp = math.exp(-delta / TAU_S)
    return THETA * (K1 * left_exp - K2 * (left_exp - right_exp)) * hss


def get_membrane_potential(epsps, epsilons, time, last_spike):
    """ Return the membrane potential at any given time.

    :param epsps: Matrix of each afferent's EPSP input contribution.
    :param epsilons: Vector of epsilon values in time window.
    :param time: Current time in ms.
    :param last_spike: Time of last spike of post-synaptic neuron.
    :return: Membrane potential.
    """
    psp = get_psp(time, last_spike)
    epsp_sum = get_epsp_sum(epsps, epsilons)

    return psp + epsp_sum


# Test Case
# =========
# Test Num Neurons
num_neurons = 10
test_length = 10

# Epsilons
epsilons = get_epsilons()

# Initial Weights
init_weights = np.random.ranf((10, 1))

# Sample Spike Trains
# m = np.random.random_integers(0, 1, (5, 5))
# m = np.matrix('1 1 1 1 1; 0 0 0 0 0; 0 0 0 0 0; 0 0 0 0 0; 0 0 0 0 0')
m = np.matrix('1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0;\
               1 0 0 0 0 0 0 0 0 0')
print m

# Print change in EPSP sum over test range.
for test in range(0, test_length):
    spikes = m[:, test]
    spikes = np.reshape(spikes, (num_neurons, 1))
    epsp_inputs = update_epsp_inputs(epsp_inputs, spikes, init_weights)
    print get_epsp_sum(epsp_inputs, epsilons)

# Plot Epsilon Kernel
# ===================
# pylab.plot(range(T_WINDOW, T_MIN, -1), epsilons)
# pylab.xlabel('Time (ms)')
# pylab.ylabel('Epsilon')
# pylab.title('EPSP Epsilon Kernel')
# pylab.show()