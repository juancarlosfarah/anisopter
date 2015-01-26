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
T_MIN = 0                   # Start time in ms.
T_STEP = 1                  # Time step in ms.
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
WEIGHT_MAX = 1              # Maximum weight value.
WEIGHT_MIN = 0              # Minimum weight value.

# Set Seed
np.random.seed(1)

# Sample Neuron
# =============
# TODO: Make this a class


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


def update_weights(spike_trains, weights, time_delta):
    """ Updates the weights according to STDP.

    :param weights: Current weight vector.
    :param time_delta: Time difference between post-synaptic and afferent spike.
    :return: Updated weight vector.
    """

    # Get number of neurons.
    num_neurons = spike_trains.shape[0]

    # If post-synaptic neuron has just fired, calculate time delta and
    # LTP for each afferent, then adjust all weights within the time window.
    if time_delta == 0:
        for i in range(0, num_neurons):
            time_delta = get_time_delta(spike_trains[i, :])
            weight_delta = get_ltp(time_delta)

            # Add weight delta and clip so that it's not > WEIGHT_MAX.
            weights[i] = min(WEIGHT_MAX, weights[i] + weight_delta)

    # Otherwise calculate LTD for all neurons that have fired,
    # if post-synaptic neuron has fired within the time window.
    elif time_delta > 0 and math.fabs(time_delta) < LTD_WINDOW:

        # Only consider last ms in spike trains.
        last_ms = spike_trains.shape[1] - 1
        spikes = spike_trains[:, last_ms]
        spikes = np.reshape(spikes, (num_neurons, 1))

        # Get LTD change for pre-synaptic neurons that just spiked.
        weight_delta = get_ltd(time_delta) * spikes

        # Add weight delta and clip weights so that they are not < WEIGHT_MIN.
        weights += weight_delta
        weights[weights < WEIGHT_MIN] = WEIGHT_MIN

    return weights


def get_time_delta(spike_train):
    """ Given an afferent, return its last spike time relative to now.

    :param spike_train: Array of spike values for afferent.
    :return: Time delta of spike time.
    """
    start = 0
    end = len(spike_train) - 1
    step = T_STEP * -1

    # Find the nearest spike in the spike train.
    for ms in range(end, start - 1, step):
        if spike_train[ms] == 1:
            return ms - end

    # If there are no spikes return a value outside the learning
    # window which means this neuron will be ignored for STDP.
    return (LTP_WINDOW + 1) * -1


def get_ltp(time_delta):
    """ Calculate weight change according to LTP.

    Note that the input delta to LTP has to be <= 0.
    :param time_delta: Time difference between post-synaptic and afferent spike.
    :return: Change in weight.
    """

    # Input delta to LTP has to be <= 0.
    if time_delta > 0:
        print "ERROR! Time delta input to LTP function needs to be less than " \
              "or equal to zero. Please double check your function calls."
        exit(1)

    # Only consider deltas within the learning window.
    if math.fabs(time_delta) > LTP_WINDOW:
        return 0

    return A_PLUS * math.exp(time_delta / T_PLUS)


def get_ltd(time_delta):
    """ Calculate weight change according to LTD.

    Note that the input delta to LTP has to be > 0.
    :param time_delta: Time difference between post-synaptic and afferent spike.
    :return: Change in weight.
    """

    # Input delta to LTP has to be > 0.
    if time_delta <= 0:
        print "ERROR! Time delta input to LTD function needs to be greater " \
              "than zero. Please double check your function calls."
        exit(1)

    # Only consider deltas within the learning window.
    if math.fabs(time_delta) > LTD_WINDOW:
        return 0

    return -1 * A_MINUS * math.exp(-time_delta / T_MINUS)


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
    end = int(LTP_WINDOW) * -1

    # Containers for y and x values, respectively.
    ltps = []
    time_delta = np.arange(end, start, 1, dtype=np.int32)

    # Get value for LTP.
    for ms in time_delta:
        # Input to LTP has to be negative.
        ltp = get_ltp(ms)
        ltps.append(ltp)

    # Plot values.
    pylab.plot(time_delta, ltps)
    pylab.xlabel('Time Delta (ms)')
    pylab.ylabel('Weight Change')
    pylab.title('Weight Change from LTP')
    pylab.show()


def plot_ltd():
    """ Plots the values of LTD over the learning window.

    :return: Void.
    """
    # Set plot parameters.
    start = 1
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
num_neurons = 2000
test_length = 1000
obj = pattern_generator.generate_pattern(num_neurons, test_length, 50, 1)
spike_trains = obj['spike_trains']
weights = np.random.ranf((num_neurons, 1))
epsilons = get_epsilons()

# Container for EPSP input contributions of each afferent.
epsp_inputs = np.array([])

# Create container for results.
ps = [T_MIN for i in range(test_length + 1)]
time = np.arange(T_MIN, test_length, 1, dtype=np.int32)

# Set last spike to an irrelevant value at first.
last_spike = 0 - max(LTD_WINDOW, LTP_WINDOW, T_WINDOW)

# Get membrane potential at each given point.
for ms in range(0, test_length):
    spikes = spike_trains[:, ms]
    spikes = np.reshape(spikes, (num_neurons, 1))
    epsp_inputs = update_epsp_inputs(epsp_inputs, spikes, weights)
    p = get_membrane_potential(epsp_inputs, epsilons, ms, last_spike)
    ps[ms] = p

    # Get relevant spikes for weight updating in LTP.
    ltp_window_start = max(0, ms - LTP_WINDOW)
    ltp_window_end = ms + 1
    spikes = spike_trains[:, ltp_window_start:ltp_window_end]

    # Update weights.
    time_delta = ms - math.fabs(last_spike)
    weights = update_weights(spikes, weights, time_delta)

    # If threshold has been met and more than 1 ms has elapsed since
    # the last post-synaptic spike, schedule a spike and flush EPSPs.
    if p > THETA and time_delta > 1:
        last_spike = ms + 1
        epsp_inputs = np.array([])

# Plot membrane potential.
pylab.plot(time[T_MIN:test_length], ps[T_MIN:test_length])
pylab.xlabel('Time (ms)')
pylab.ylabel('Membrane Potential')
pylab.title('Spike Train with STDP')
pylab.show()