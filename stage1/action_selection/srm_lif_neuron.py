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
T_MIN = 0           # Start time.
TAU_M = 10.0        # Membrane time constant in ms.
TAU_S = 2.5         # Synapse time constant in ms.
THETA = 500         # Threshold in arbitrary units.
K = 1               # Multiplicative constant.
K1 = 2              # Multiplicative constant for PSP.
K2 = 4              # Multiplicative constant for PSP.
T_RES = TAU_M * 7   # Maximum time that a spike can affect EPSP.


def heavyside_step(delta):
    """ Calculate value of heavyside step for a given time delta.

    :param delta: Time difference.
    :return:
    """
    if delta >= 0:
        return 1
    else:
        return 0


def get_epsp(spike_train, time, last_spike):
    """ Given a spike train calculate the EPSP contribution of an afferent.

    :param spike_train: A given neuron's spike train.
    :param time: Current time in ms.
    :return: Array of the EPSP contributions of an afferent.
    """

    # Array to store EPSP contributions.
    epsilons = []

    # Only consider up to T_RES contributions into the past
    # or up to the time the post-synaptic neuron fired last.
    start = max(T_MIN, time - T_RES, last_spike)

    # For each potential spike in the observation
    # window, calculate EPSP contribution.
    for i in range(start, time + 1):

        # Only calculate the EPSP contribution of spikes.
        if spike_train[i] != 0:
            delta = time - i
            hss = heavyside_step(delta)
            left_exp = math.exp(-delta / TAU_M)
            right_exp = math.exp(-delta / TAU_S)
            epsilon = K * (left_exp - right_exp) * hss
            epsilons.append(epsilon)
        else:
            epsilons.append(0)

    return epsilons


def get_epsp_sum(spike_trains, weights, time, last_spike):
    """ Sum the EPSP contribution of all afferents.

    :param spike_trains: Matrix with each afferent's spike train.
    :param weights: Synaptic weights between afferents and post-synaptic neuron.
    :param time: Current time in ms.
    :param last_spike: Time of last spike of post-synaptic neuron.
    :return:
    """

    # Create container to collect EPSP contributions.
    num_neurons = spike_trains.shape[0]
    epsps = np.array([])

    # Get the EPSP contribution of each neuron.
    for i in range(0, num_neurons):
        new_epsp = get_epsp(spike_trains[i], time, last_spike)
        if epsps.size == 0:
            epsps = np.hstack((epsps, new_epsp))
        else:
            epsps = np.vstack((epsps, new_epsp))

    # Only consider weights for the relevant observation period.
    num_cols = epsps.shape[1]
    first_relevant_weights = weights.shape[1] - num_cols
    relevant_weights = weights[:, first_relevant_weights:]

    # Get weighted EPSP contributions.
    weighted = np.multiply(epsps, relevant_weights)

    # Return sum of weighted contributions.
    return sum(sum(weighted))


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


def get_membrane_potential(spike_trains, weights, time, last_spike):
    """ Return the membrane potential at any given time.

    :param spike_trains: Matrix with each afferent's spike train.
    :param weights: Synaptic weights between afferents and post-synaptic neuron.
    :param time: Current time in ms.
    :param last_spike: Time of last spike of post-synaptic neuron.
    :return: Membrane potential.
    """
    psp = get_psp(time, last_spike)
    epsp_sum = get_epsp_sum(spike_trains, weights, time, last_spike)

    return psp + epsp_sum


# Test Case
# =========

# Set Seed
np.random.seed(1)
# Sample Weights
w = np.random.ranf((5, 5))
# Sample Spike Trains
m = np.identity(5, dtype=np.int32)
print m
print get_membrane_potential(m, w, 4, 0)