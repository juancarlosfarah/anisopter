__author__ = 'Juan Carlos Farah,' \
             'Panagiotis Almpouras,' \
             'Erik Grabljevec'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk,' \
                  'panagiotis.almpouras12@imperial.ac.uk,' \
                  'erik.grabljevec14@imperial.ac.uk'

import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
import pattern_generator
import sys
import poisson_pattern_generator
from copy import deepcopy

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
K = 2.1222619               # Multiplicative constant.
K1 = 2                      # Constant for positive pulse.
K2 = 4                      # Constant for negative spike after-potential.
T_WINDOW = int(TAU_M * 7)   # Maximum time that a spike can affect EPSP.
T_PLUS = 16.8               # LTP synaptic modification constant in ms.
T_MINUS = 33.7              # LTD synaptic modification constant in ms.
A_PLUS = 0.03125            # LTP learning rate.
A_MINUS = 0.85 * A_PLUS     # LTD learning rate.
LTP_WINDOW = 7 * T_PLUS     # LTP learning window.
LTD_WINDOW = 7 * T_MINUS    # LTD learning window.
WEIGHT_MAX = 1              # Maximum weight value.
WEIGHT_MIN = 0              # Minimum weight value.
PATTERN_LEN = 50            # Length of pattern.

# Set Seed
# np.random.seed(1)

# Sample Neuron
# =============
# TODO: Make this a class


def calculate_epsilons():
    """ Returns a vector with epsilon values relevant for EPSP.

    :return: Vector of epsilon values in time window.
    """
    epsilons = np.ndarray((T_WINDOW, 1), dtype=float)
    for i in range(0, T_WINDOW):
        delta = T_WINDOW - (i + 1)
        hss = calculate_heavyside_step(delta)
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

    global non_weighted_neurons

    # If post-synaptic neuron has just fired, calculate time delta and
    # LTP for each afferent, then adjust all weights within the time window.
    if time_delta == 0:
        for i in range(0, num_neurons):
            spike_lag = calculate_time_delta(spike_trains[i, :])
            weight_delta = calculate_ltp(spike_lag)
            # Add weight delta and clip so that it's not > WEIGHT_MAX.
            weights[i] = min(WEIGHT_MAX, weights[i] + weight_delta)

        # Reset neurons to be weighed.
        non_weighted_neurons = np.ones((num_neurons, 1), dtype=np.float)

    # Otherwise calculate LTD for all neurons that have fired,
    # if post-synaptic neuron has fired within the time window.
    elif time_delta > 0 and math.fabs(time_delta) < LTD_WINDOW:

        # Only consider last ms in spike trains.
        last_ms = spike_trains.shape[1] - 1
        spikes = deepcopy(spike_trains[:, last_ms])
        spikes = np.reshape(spikes, (num_neurons, 1))

        # Get LTD change for pre-synaptic neurons that
        # just spiked and have not been weighed yet.
        neurons_to_weigh = np.multiply(spikes, non_weighted_neurons)
        weight_delta = calculate_ltd(time_delta) * neurons_to_weigh

        # Add weight delta and clip weights so that they are not < WEIGHT_MIN.
        weights += weight_delta
        weights[weights < WEIGHT_MIN] = WEIGHT_MIN
        non_weighted_neurons = np.multiply(non_weighted_neurons,
                                           np.logical_not(spikes))

    return weights


def calculate_time_delta(spike_train):
    """ Given an afferent, return its last spike time relative to now.

    :param spike_train: Array of spike values for afferent.
    :return: Time delta of spike time.
    """
    start = 0
    end = len(spike_train) - 1

    # Find the nearest spike in the spike train.
    for ms in range(end, start - 1, -T_STEP):
        if spike_train[ms] == 1:
            return ms - end

    # If there are no spikes return a value outside the learning
    # window which means this neuron will be ignored for STDP.
    return (LTP_WINDOW + 1) * -1


def calculate_ltp(time_delta):
    """ Calculate weight change according to LTP.

    Note that the input delta to LTP has to be <= 0.
    :param time_delta: Time difference between post-synaptic and afferent spike.
    :return: Change in weight.
    """

    # Input delta to LTP has to be <= 0.
    if time_delta > 0:
        print "ERROR! Time delta input to LTP function needs to be less than " \
              "or equal to zero. Please double check your function calls."
        # Use raise value error.
        exit(1)

    # Only consider deltas within the learning window.
    if math.fabs(time_delta) > LTP_WINDOW:
        return 0

    return A_PLUS * math.exp(time_delta / T_PLUS)


def calculate_ltd(time_delta):
    """ Calculate weight change according to LTD.

    Note that the input delta to LTP has to be > 0.
    :param time_delta: Time difference between post-synaptic and afferent spike.
    :return: Change in weight.
    """

    # Input delta to LTP has to be > 0.
    if time_delta <= 0:
        print "ERROR! Time delta input to LTD function needs to be greater " \
              "than zero. Please double check your function calls."
        # Use raise value error.
        exit(1)

    # Only consider deltas within the learning window.
    if math.fabs(time_delta) > LTD_WINDOW:
        return 0

    return -A_MINUS * math.exp(-time_delta / T_MINUS)


def calculate_heavyside_step(delta):
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

    # Number of neurons.
    num_neurons = epsps.shape[0]

    # Flush EPSP for neurons that fired.
    # for i in range(0, num_neurons):
    #     if spikes[i] == 1:
    #         epsps[i, :] = 0

    weighted = np.multiply(spikes, weights)
    epsps = np.hstack((epsps, weighted))

    # Length of new EPSP window.
    width = epsps.shape[1]

    # Clamp neuron to learning window.
    if width > T_WINDOW:
        window_start = width - T_WINDOW
        epsps = epsps[:, window_start:width]

    return epsps


def sum_epsps(epsps, epsilons):
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


def calculate_psp(time, last_spike, theta=THETA):
    """ Calculate the effect of a post-synaptic spike on the potential.

    :param time: Current time in ms.
    :param last_spike: Time of last spike of post-synaptic neuron.
    :return: Value of the effect.
    """
    delta = math.fabs(time - last_spike)
    if delta > T_WINDOW:
        return 0
    hss = calculate_heavyside_step(delta)
    left_exp = math.exp(-delta / TAU_M)
    right_exp = math.exp(-delta / TAU_S)
    return theta * (K1 * left_exp - K2 * (left_exp - right_exp)) * hss


def calculate_membrane_potential(epsps, epsilons, time,
                                 last_spike, theta=THETA):
    """ Return the membrane potential at any given time.

    :param epsps: Matrix of each afferent's EPSP input contribution.
    :param epsilons: Vector of epsilon values in time window.
    :param time: Current time in ms.
    :param last_spike: Time of last spike of post-synaptic neuron.
    :return: Membrane potential.
    """
    psp = calculate_psp(time, last_spike, theta)
    epsp_sum = sum_epsps(epsps, epsilons)
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
        psp = calculate_psp(ms, last_spike)
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
    epsilons = calculate_epsilons()
    pylab.plot(range(T_WINDOW - 1, T_MIN - 1, -1), epsilons)
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Epsilon')
    pylab.title('EPSP Epsilon Kernel')
    pylab.show()


def plot_ltp(show=True):
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
        ltp = calculate_ltp(ms)
        ltps.append(ltp)

    # Plot values.
    pylab.plot(time_delta, ltps)
    if show:
        pylab.xlabel('Time Delta (ms)')
        pylab.ylabel('Weight Change')
        pylab.title('Weight Change from LTP')
        pylab.show()


def plot_ltd(show=True):
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
        ltd = calculate_ltd(ms)
        ltds.append(ltd)

    # Plot values.
    pylab.plot(time_delta[start:end], ltds[start:end])

    if show:
        pylab.xlabel('Time Delta (ms)')
        pylab.ylabel('Weight Change')
        pylab.title('Weight Change from LTD')
        pylab.show()


def plot_weights(weights, ms, rows=1, cols=1, current_frame=1, bin_size=1):
    """ Plots the distribution of the values of the weights.

    :param weights: Array of weights.
    :param rows: Number of rows in the plot.
    :param cols: Number of columns in the plot.
    :param current_frame: Current frame for the plot.
    :param bins: Size of bins when generating the histogram.
    :return: Void.
    """

    # Plot a histogram of the values.
    p = pylab.subplot(rows, cols, current_frame)

    # Only add title to first plot.
    if current_frame == 1:
        pylab.title('Weight Distribution Over Time')

    p.axes.get_xaxis().set_visible(False)
    p.axes.get_yaxis().set_ticks([])
    label = str(ms / 1000) + 's'
    bins = len(weights) / bin_size
    pylab.ylabel(label)
    p.hist(weights, bins=bins)

    # Only show if plot is complete.
    if rows * cols == current_frame:
        pylab.xlabel("Weight Value")
        p.axes.get_xaxis().set_visible(True)
        pylab.show()


def plot_lif_neuron():
    """ Replicates the plot in Figure 3 of Masquelier et al. (2008).

    :return: Void.
    """
    # Set parameters.
    num_neurons = 1
    test_length = 80
    theta = 3
    spike_trains = pattern_generator.single_train()
    weights = np.empty(num_neurons)
    weights.fill(1)
    epsilons = calculate_epsilons()

    # Container for EPSP input contributions of each afferent.
    epsp_inputs = np.array([])

    # Create container for results.
    ps = [T_MIN] * test_length
    time = np.arange(T_MIN, test_length, 1, dtype=np.int32)

    # Set last spike to an irrelevant value at first.
    last_spike = 0 - max(LTD_WINDOW, LTP_WINDOW, T_WINDOW)

    # Get membrane potential at each given point.
    for ms in range(0, test_length - 1):
        spikes = spike_trains[:, ms]
        spikes = np.reshape(spikes, (num_neurons, 1))
        epsp_inputs = update_epsp_inputs(epsp_inputs, spikes, weights)
        p = calculate_membrane_potential(epsp_inputs, epsilons,
                                         ms, last_spike, theta)

        # Here we're posting the potential to the next ms.
        # TODO: Confirm with Pedro if this makes sense.
        ps[ms + 1] = p

        # Plot incoming spikes.
        if spikes[0] == 1:
            plt.axvline(ms, ls='dashed', c='grey')

        # If threshold has been met and more than 1 ms has elapsed since
        # the last post-synaptic spike, schedule a spike and flush EPSPs.
        time_delta = ms - math.fabs(last_spike)
        if p > theta and math.fabs(time_delta) > 1:
            last_spike = ms + 1
            epsp_inputs = np.array([])

    # Plot membrane potential.
    pylab.plot(time[T_MIN:test_length], ps[T_MIN:test_length])
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Membrane Potential (Arbitrary Units)')
    pylab.title('Sample LIF Neuron')
    pylab.show()


def plot_stdp():
    """ Plot STDP from both LTD and LTP.
    :return: Void.
    """
    plot_ltd(False)
    plot_ltp(False)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    pylab.xlabel('Time Delta (ms)')
    pylab.ylabel('Weight Change from STDP')
    pylab.xlim(-1 * LTP_WINDOW, LTD_WINDOW)
    pylab.title('Weight Change')
    pylab.show()


# Run Sample Test without STDP
# ============================
# sample = poisson_pattern_generator.generate_sample(num_neurons,
#                                                    test_length,
#                                                    pattern_len)
folder = "samples/"
filename = "1_2000_5000_50_0.25_0.5_10.0"
extension = ".npz"
path = folder + filename + extension
sample = poisson_pattern_generator.load_sample(path)
spike_trains = sample['spike_trains']
start_positions = sample['start_positions']

# Get parameters.
params = map(float, filename.split("_"))
num_neurons = int(params[1])
test_length = int(params[2])
pattern_len = int(params[3])

# Initialise weights.
weights = np.random.normal(0.475, 0.1, (num_neurons, 1))
weights[weights < WEIGHT_MIN] = WEIGHT_MIN
weights[weights > WEIGHT_MAX] = WEIGHT_MAX

# TODO: Integrate this global variable.
non_weighted_neurons = np.ones((num_neurons, 1), dtype=int)

epsilons = calculate_epsilons()

# Container for EPSP input contributions of each afferent.
epsp_inputs = np.zeros((num_neurons, 1))

# Create container for results.
ps = [T_MIN for i in range(test_length + 1)]
time = np.arange(T_MIN, test_length, 1, dtype=np.int32)

# Set last spike to an irrelevant value at first.
last_spike = 0 - max(LTD_WINDOW, LTP_WINDOW, T_WINDOW)

# Values for plotting weights.
frame = 1
frames = 5
bin_size = 50
frame_step = test_length / frames
rows = frames + 1

# Containers for weights of random neurons over time.
neuron_sample_size = 10
neuron_numbers = []
neuron_weights = []
for i in range(0, neuron_sample_size):
    neuron_numbers.append(np.random.randint(0, num_neurons))
    container = [0] * test_length
    neuron_weights.append(container)

# Get membrane potential at each given point.
for ms in range(0, test_length - 1):
    spikes = deepcopy(spike_trains[:, ms])
    spikes = np.reshape(spikes, (num_neurons, 1))
    p = calculate_membrane_potential(epsp_inputs, epsilons,
                                     ms, last_spike, THETA)
    epsp_inputs = update_epsp_inputs(epsp_inputs, spikes, weights)

    # Here we're posting the potential to the next ms.
    # TODO: Confirm with Pedro if this makes sense.
    ps[ms + 1] = p

    # Get relevant spikes for weight updating in LTP.
    ltp_window_start = max(0, ms - LTP_WINDOW)
    ltp_window_end = ms + 1
    spikes = deepcopy(spike_trains[:, ltp_window_start:ltp_window_end])

    # Record sample neurons' weight at this point.
    for i in range(0, neuron_sample_size):
        neuron_weights[i][ms] = weights[neuron_numbers[i]][0]

    # Update weights.
    time_delta = ms - math.fabs(last_spike)
    weights = update_weights(spikes, weights, time_delta)

    # Plot weight distribution at given intervals.
    if ms % frame_step == 0:
        plot_weights(weights, ms, rows, current_frame=frame, bin_size=bin_size)
        frame += 1

    # If threshold has been met and more than 1 ms has elapsed
    # since the last post-synaptic spike, schedule a spike.
    if p >= THETA and math.fabs(time_delta) > 1:
        last_spike = ms + 1
        epsp_inputs = np.zeros((num_neurons, 1))

    # Progress bar.
    progress = (ms / float(test_length - 1)) * 100
    sys.stdout.write("Processing spikes: %d%% \r" % progress)
    sys.stdout.flush()

# Plot final weight distribution.
plot_weights(weights, test_length, rows, current_frame=frame, bin_size=bin_size)

# Plot sample neurons' weight over time.
for i in range(0, neuron_sample_size):
    pylab.plot(time[T_MIN:test_length], neuron_weights[i][T_MIN:test_length])
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Weight')
    pylab.title('Synaptic Weight')
pylab.show()

# Prepare the pattern plot.
color = '#E6E6E6'
min_y = THETA * -0.5
max_y = THETA * 2.25
for i in start_positions:
    plt.gca().add_patch(Rectangle((i, min_y),
                                  PATTERN_LEN,
                                  max_y + math.fabs(min_y),
                                  facecolor=color,
                                  edgecolor=color))

# Plot membrane potential.
pylab.plot(time[T_MIN:test_length], ps[T_MIN:test_length])
pylab.ylim(min_y, max_y)
pylab.xlabel('Time (ms)')
pylab.ylabel('Membrane Potential')
pylab.title('Spike Train with STDP')
pylab.show()
