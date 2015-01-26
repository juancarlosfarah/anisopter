__author__ = 'Juan Carlos Farah,' \
             'Panagiotis Almpouras,' \
             'Erik Grabljevec'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk,' \
                  'panagiotis.almpouras12@imperial.ac.uk,' \
                  'erik.grabljevec14@imperial.ac.uk'

import numpy as np
import pylab
import math
import pattern_generator

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
K = 2.1                     # Multiplicative constant.
K1 = 2                      # Constant for positive pulse.
K2 = 4                      # Constant for negative spike after-potential.
T_WINDOW = int(TAU_M * 7)   # Maximum time that a spike can affect EPSP.
T_PLUS = 16.8               # LTP synaptic modification constant in ms.
T_MINUS = 33.7              # LTP synaptic modification constant in ms.
A_PLUS = 0.03125            # LTP learning rate.
A_MINUS = 0.85 * A_PLUS     # LTD learning rate.
LTP_WINDOW = 7 * T_PLUS     # LTP learning window.
LTD_WINDOW = 7 * T_MINUS    # LTD learning window.

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
def update_weights(spikes, weights, last_spike):
    """ Updates the weights according to STDP.

    :param weights: Current weight vector.
    :return: Updated weight vector.
    """

    # If post-synaptic neuron has just fired, calculate
    # LTP and adjust all weights within the time window.

    # Otherwise calculate LTD for all neurons that have fired,
    # if post-synaptic neuron has fired within the time window.

    return weights


def get_ltp(delta):
    """ Calculate weight change according to LTP.

    Note that the input delta to LTP has to be <= 0.
    :param delta: Time difference between post-synaptic and afferent spike.
    :return: Change in weight.
    """

    # Input delta to LTP has to be <= 0.
    if delta > 0:
        print "ERROR! Time delta input to LTP function needs to be less than" \
              "or equal to zero. Please double check your function calls."
        exit(1)

    # Only consider deltas within the learning window.
    if delta > LTP_WINDOW:
        return 0

    return A_PLUS * math.exp(delta / T_PLUS)


def get_ltd(delta):
    """ Calculate weight change according to LTD.

    Note that the input delta to LTP has to be > 0.
    :param delta: Time difference between post-synaptic and afferent spike.
    :return: Change in weight.
    """

    # Input delta to LTP has to be > 0.
    if delta <= 0:
        print "ERROR! Time delta input to LTD function needs to be greater" \
              "than zero. Please double check your function calls."
        exit(1)

    # Only consider deltas within the learning window.
    if delta > LTD_WINDOW:
        return 0

    return -1 * A_MINUS * math.exp(delta / T_MINUS)


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
    if width > T_WINDOW:
        window_start = width - T_WINDOW
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
    if delta > T_WINDOW:
        return 0
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


def plot_eta():
    """ Plots the values of the eta kernel for a given range.

    :return: Void.
    """
    # Calculate PSPs for given range.
    psps = []
    time = np.arange(T_MIN, T_WINDOW, 1, dtype=np.int32)
    last_spike = T_MIN
    for ms in range(T_MIN, T_WINDOW):
        psp = get_psp(ms, last_spike)
        psps.append(psp)

    # Plot values.
    pylab.plot(time[T_MIN:T_WINDOW], psps[T_MIN:T_WINDOW])
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Post-Synaptic Potential')
    pylab.title('Eta Kernel')
    pylab.show()


def plot_epsilon():
    """ Plots the values of the epsilon kernel.

    :return: Void.
    """
    epsilons = get_epsilons()
    pylab.plot(range(T_WINDOW, T_MIN, -1), epsilons)
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Epsilon')
    pylab.title('EPSP Epsilon Kernel')
    pylab.show()


def plot_ltp():
    """ Plots the values of LTP over the learning window.

    :return: Void.
    """
    # Set plot parameters.
    start = 0
    end = int(LTP_WINDOW)

    # Containers for y and x values, respectively.
    ltps = []
    time_delta = np.arange(start, end, 1, dtype=np.int32)

    # Get value for LTP.
    for ms in range(start, end, 1):
        # Input to LTP has to be negative.
        ms *= -1
        ltp = get_ltp(ms)
        ltps.append(ltp)

    # Plot values.
    pylab.plot(time_delta[start:end], ltps[start:end])
    pylab.xlabel('Time Delta (ms)')
    pylab.ylabel('Weight Change')
    pylab.title('Weight Change from LTP')
    pylab.show()


def plot_ltd():
    """ Plots the values of LTD over the learning window.

    :return: Void.
    """
    # Set plot parameters.
    start = 0
    end = int(LTD_WINDOW)

    # Containers for y and x values, respectively.
    ltds = []
    time_delta = np.arange(start, end, 1, dtype=np.int32)

    # Get value for LTD.
    for ms in range(start, end, 1):
        ltd = get_ltd(ms)
        ltds.append(ltd)

    # Plot values.
    pylab.plot(time_delta[start:end], ltds[start:end])
    pylab.xlabel('Time Delta (ms)')
    pylab.ylabel('Weight Change')
    pylab.title('Weight Change from LTD')
    pylab.show()


# Run Sample Test without STDP
# ============================
# Set parameters.
num_neurons = 200
test_length = 500
fixed_weight = 0.475
obj = pattern_generator.generate_pattern(num_neurons, test_length, 50, 1)
spike_trains = obj['spike_trains']
initial_weights = np.ndarray((num_neurons, 1))
initial_weights.fill(fixed_weight)
epsilons = get_epsilons()

# Purge afferent spike trains. This is necessary because sometimes the
# afferents fire too often making this model without STDP fire constantly.
purge_factor = 3
for i in range(0, test_length, purge_factor):
    for j in range(0, num_neurons):
        spike_trains[j, i] = 0

# Create container for results.
ps = [T_MIN for i in range(test_length + 1)]
time = np.arange(T_MIN, test_length, 1, dtype=np.int32)

# Assume last spike is irrelevant.
last_spike = 0 - T_WINDOW

# Get membrane potential at each given point.
for ms in range(0, test_length):
    spikes = spike_trains[:, ms]
    spikes = np.reshape(spikes, (num_neurons, 1))
    epsp_inputs = update_epsp_inputs(epsp_inputs, spikes, initial_weights)
    p = get_membrane_potential(epsp_inputs, epsilons, ms, last_spike)
    ps[ms] = p

    # If threshold has been met and more than 1 ms has elapsed since
    # the last post-synaptic spike, schedule a spike and flush EPSPs.
    if p > THETA and ms - last_spike > 1:
        last_spike = ms + 1
        epsp_inputs = np.array([])

# Plot membrane potential.
pylab.plot(time[T_MIN:test_length], ps[T_MIN:test_length])
pylab.xlabel('Time (ms)')
pylab.ylabel('Membrane Potential')
pylab.title('Spike Train without STDP')
pylab.show()