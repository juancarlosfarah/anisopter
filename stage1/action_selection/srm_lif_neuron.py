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



K = 2.1222619               # Multiplicative constant.
K1 = 2                      # Constant for positive pulse.
K2 = 4                      # Constant for negative spike after-potential.


# Set Seed
# np.random.seed(1)

class Neuron:
    """
    Simulates a leaky integrate-and-fire (LIF) neuron following the
    Gerstner's Spike Response Model (SRM). As a basis we are using
    the parameters from Masquelier et al. (2008).
    """

    def __init__(self, num_afferents):
        self.num_afferents = num_afferents   # Number of afferents.
        self.tau_m = 10.0                    # Membrane time constant in ms.
        self.tau_s = 2.5                     # Synapse time constant in ms.
        self.t_plus = 16.8                   # LTP modification constant in ms.
        self.t_minus = 33.7                  # LTD modification constant in ms.
        self.ltp_window = 7 * self.t_plus    # LTP learning window.
        self.ltd_window = 7 * self.t_minus   # LTD learning window.
        self.t_window = int(self.tau_m * 7)  # Max time that spike affects EPSP.
        self.weight_max = 1                  # Maximum weight value.
        self.weight_min = 0                  # Minimum weight value.
        self.a_plus = 0.03125                # LTP learning rate.
        self.a_minus = 0.90 * self.a_plus    # LTD learning rate. NOTE: should be 0.85
        self.theta = 500                     # Threshold in arbitrary units.
        self.time_delta = None               # Time since last spike in ms.

        # Initialise weights.
        self.weights = np.random.normal(0.475, 0.1, (num_afferents, 1))
        self.weights[self.weights < self.weight_min] = self.weight_min
        self.weights[self.weights > self.weight_max] = self.weight_max

        # Initialise epsilons.
        self.epsilons = self.calculate_epsilons()

        # Initialise synapses eligible to undergo LTD.
        self.synapses_for_ltd = np.ones((self.num_afferents, 1), dtype=np.int32)

        # Initialise EPSP inputs container.
        self.epsps = np.zeros((self.num_afferents, 1))

    def calculate_epsilons(self):
        """
        Returns a vector with epsilon values relevant for EPSP.
        :return: Vector of epsilon values in time window.
        """
        epsilons = np.ndarray((self.t_window, 1), dtype=float)
        for i in range(0, self.t_window):
            delta = self.t_window - (i + 1)
            hss = self.calculate_heavyside_step(delta)
            left_exp = math.exp(-delta / self.tau_m)
            right_exp = math.exp(-delta / self.tau_s)
            epsilon = K * (left_exp - right_exp) * hss
            epsilons[i, 0] = epsilon

        return epsilons

    def update_weights(self, spike_trains):
        """
        Updates the weights according to STDP.
        :param time_delta: Delay between post-synaptic and afferent spike.
        :return: Updated weight vector.
        """

        # Get number of neurons.
        num_afferents = spike_trains.shape[0]

        global non_weighted_neurons, penultimate_spike, last_spike

        # If post-synaptic neuron has just fired, calculate time delta and
        # LTP for each afferent, then adjust all weights within the time window.
        if self.time_delta == 0:
            for i in range(0, self.num_afferents):
                spike_lag = self.calculate_time_delta(spike_trains[i, :])
                weight_delta = self.calculate_ltp(spike_lag)
                # Add weight delta and clip so that it's not > WEIGHT_MAX.
                self.weights[i] = min(self.weight_max,
                                      self.weights[i] + weight_delta)

            # Reset neurons to be weighed.
            penultimate_spike = last_spike
            non_weighted_neurons = np.ones((self.num_afferents, 1),
                                           dtype=np.float)

        # Otherwise calculate LTD for all neurons that have fired,
        # if post-synaptic neuron has fired within the time window.
        elif self.time_delta > 0 and self.time_delta < self.ltd_window:

            # Only consider last ms in spike trains.
            last_ms = spike_trains.shape[1] - 1
            spikes = deepcopy(spike_trains[:, last_ms])
            spikes = np.reshape(spikes, (num_afferents, 1))

            # Get LTD change for pre-synaptic neurons that
            # just spiked and have not been weighed yet.
            neurons_to_weigh = np.multiply(spikes, non_weighted_neurons)
            weight_delta = self.calculate_ltd(self.time_delta) * neurons_to_weigh

            # Add weight delta and clip so that they are not < WEIGHT_MIN.
            self.weights += weight_delta
            self.weights[self.weights < self.weight_min] = self.weight_min
            non_weighted_neurons = np.multiply(non_weighted_neurons,
                                               np.logical_not(spikes))

        return self.weights

    def calculate_time_delta(self, spike_train):
        """
        Given an afferent, return its last spike time relative to now.
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
        return (self.ltp_window + 1) * -1

    def calculate_ltp(self, time_delta):
        """
        Calculate weight change according to LTP.
        Note that the input delta to LTP has to be <= 0.
        :param time_delta: Delay between post-synaptic and afferent spike.
        :return: Change in weight.
        """

        # Input delta to LTP has to be <= 0.
        if time_delta > 0:
            print "ERROR! Input to LTP function needs to be less than " \
                  "or equal to zero. Please double check your function calls."
            # Use raise value error.
            exit(1)

        # Only consider deltas within the learning window.
        if math.fabs(time_delta) > self.ltp_window:
            return 0

        return self.a_plus * math.exp(time_delta / self.t_plus)

    def calculate_ltd(self, time_delta):
        """
        Calculate weight change according to LTD.
        Note that the input delta to LTP has to be > 0.
        :param time_delta: Delay between post-synaptic and afferent spike.
        :return: Change in weight.
        """

        # Input delta to LTP has to be > 0.
        if time_delta <= 0:
            print "ERROR! Input to LTD function needs to be greater " \
                  "than zero. Please double check your function calls."
            # Use raise value error.
            exit(1)

        # Only consider deltas within the learning window.
        if math.fabs(time_delta) > self.ltd_window:
            return 0

        return -self.a_minus * math.exp(-time_delta / self.t_minus)

    def calculate_heavyside_step(self, delta):
        """
        Calculate value of heavyside step for a given time delta.
        :param delta: Time difference.
        :return:
        """
        if delta >= 0:
            return 1
        else:
            return 0

    def update_epsp_inputs(self, spikes):
        """
        Given vectors of spikes and weights update the EPSP contributions.
        :param epsps: Matrix of current EPSP inputs.
        :param spikes: Vector of current spikes.
        :return:
        """

        weighted = np.multiply(spikes, self.weights)
        self.epsps = np.hstack((self.epsps, weighted))

        # Length of new EPSP window.
        width = self.epsps.shape[1]

        # Clamp neuron to learning window.
        if width > self.t_window:
            window_start = width - self.t_window
            self.epsps = self.epsps[:, window_start:width]

        return self.epsps

    def sum_epsps(self, epsps, epsilons):
        """
        Sum the EPSP contribution of all afferents.
        :param epsps: Matrix of current EPSP inputs.
        :param epsilons: Vector of epsilon values in time window.
        :return:
        """

        # Only consider as many epsilons as we have input.
        input_width = self.epsps.shape[1]
        epsilon_height = self.epsilons.shape[0]
        start = epsilon_height - input_width

        # Get weighted EPSP contributions.
        weighted = np.matrix(self.epsps) * np.matrix(self.epsilons[start:])

        # Return sum of weighted contributions.
        return np.sum(weighted)

    def calculate_psp(self):
        """
        Calculate the effect of a post-synaptic spike on the potential.
        :param time_delta: Time since last spike of post-synaptic neuron.
        :return: Value of the effect.
        """
        if self.time_delta > self.t_window:
            return 0
        hss = self.calculate_heavyside_step(self.time_delta)
        left_exp = math.exp(-self.time_delta / self.tau_m)
        right_exp = math.exp(-self.time_delta / self.tau_s)
        return self.theta * (K1 * left_exp - K2 * (left_exp - right_exp)) * hss

    def calculate_membrane_potential(self):
        """
        Return the membrane potential at any given time.
        :param epsps: Matrix of each afferent's EPSP input contribution.
        :param time: Current time in ms.
        :param last_spike: Time of last spike of post-synaptic neuron.
        :return: Membrane potential.
        """
        psp = self.calculate_psp()
        epsp_sum = self.sum_epsps(self.epsps, self.epsilons)
        return psp + epsp_sum

    def plot_eta(self):
        """
        Plots the values of the eta kernel for a given range.
        :return: Void.
        """
        # Calculate PSPs for given range.
        psps = []
        time = np.arange(T_MIN, self.t_window, 1, dtype=np.int32)
        last_spike = T_MIN
        for ms in range(T_MIN, self.t_window):
            psp = self.calculate_psp(ms, last_spike)
            psps.append(psp)

        # Plot values.
        pylab.plot(time[T_MIN:self.t_window], psps[T_MIN:self.t_window])
        pylab.xlabel('Time (ms)')
        pylab.ylabel('Post-Synaptic Potential')
        pylab.title('Eta Kernel')
        pylab.show()

    def plot_epsilon(self):
        """
        Plots the values of the epsilon kernel.
        :return: Void.
        """
        epsilons = self.calculate_epsilons()
        pylab.plot(range(self.t_window - 1, T_MIN - 1, -1), epsilons)
        pylab.xlabel('Time (ms)')
        pylab.ylabel('Epsilon')
        pylab.title('EPSP Epsilon Kernel')
        pylab.show()

    def plot_ltp(self, show=True):
        """
        Plots the values of LTP over the learning window.
        :return: Void.
        """
        # Set plot parameters.
        start = 0
        end = int(self.ltp_window) * -1

        # Containers for y and x values, respectively.
        ltps = []
        time_deltas = np.arange(end, start, 1, dtype=np.int32)

        # Get value for LTP.
        for ms in time_deltas:
            # Input to LTP has to be negative.
            ltp = self.calculate_ltp(ms)
            ltps.append(ltp)

        # Plot values.
        pylab.plot(time_deltas, ltps)
        if show:
            pylab.xlabel('Time Delta (ms)')
            pylab.ylabel('Weight Change')
            pylab.title('Weight Change from LTP')
            pylab.show()

    def plot_ltd(self, show=True):
        """
        Plots the values of LTD over the learning window.
        :return: Void.
        """
        # Set plot parameters.
        start = 1
        end = int(self.ltd_window)

        # Containers for y and x values, respectively.
        ltds = []
        time_deltas = np.arange(start, end, 1, dtype=np.int32)

        # Get value for LTD.
        for ms in range(start, end, 1):
            ltd = self.calculate_ltd(ms)
            ltds.append(ltd)

        # Plot values.
        pylab.plot(time_deltas[start:end], ltds[start:end])

        if show:
            pylab.xlabel('Time Delta (ms)')
            pylab.ylabel('Weight Change')
            pylab.title('Weight Change from LTD')
            pylab.show()

    def plot_weights(self, ms, rows=1, cols=1,
                     current_frame=1, bin_size=1):
        """
        Plots the distribution of the values of the weights.
        :param rows: Number of rows in the plot.
        :param cols: Number of columns in the plot.
        :param current_frame: Current frame for the plot.
        :param bin_size: Size of bins when generating the histogram.
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
        bins = len(self.weights) / bin_size
        pylab.ylabel(label)
        p.hist(self.weights, bins=bins)

        # Only show if plot is complete.
        if rows * cols == current_frame:
            pylab.xlabel("Weight Value")
            p.axes.get_xaxis().set_visible(True)
            pylab.show()

    # TODO: Put this function somewhere else.
    # def plot_lif_neuron(self):
    #     """
    #     Replicates the plot in Figure 3 of Masquelier et al. (2008).
    #     :return: Void.
    #     """
    #     # Set parameters.
    #     num_neurons = 1
    #     test_length = 80
    #     theta = 3
    #     spike_trains = pattern_generator.single_train()
    #     weights = np.empty(num_neurons)
    #     weights.fill(1)
    #     epsilons = calculate_epsilons()
    #
    #     # Container for EPSP input contributions of each afferent.
    #     epsp_inputs = np.array([])
    #
    #     # Create container for results.
    #     ps = [T_MIN] * test_length
    #     time = np.arange(T_MIN, test_length, 1, dtype=np.int32)
    #
    #     # Set last spike to an irrelevant value at first.
    #     last_spike = 0 - max(ltd_window, ltp_window, t_window)
    #
    #     # Get membrane potential at each given point.
    #     for ms in range(0, test_length - 1):
    #         spikes = spike_trains[:, ms]
    #         spikes = np.reshape(spikes, (num_neurons, 1))
    #         epsp_inputs = update_epsp_inputs(epsp_inputs, spikes, weights)
    #         p = calculate_membrane_potential(epsp_inputs, epsilons,
    #                                          ms, last_spike, theta)
    #
    #         # Here we're posting the potential to the next ms.
    #         # TODO: Confirm with Pedro if this makes sense.
    #         ps[ms + 1] = p
    #
    #         # Plot incoming spikes.
    #         if spikes[0] == 1:
    #             plt.axvline(ms, ls='dashed', c='grey')
    #
    #         # If threshold has been met and more than 1 ms has elapsed since
    #         # the last post-synaptic spike, schedule a spike and flush EPSPs.
    #         time_delta = ms - math.fabs(last_spike)
    #         if p > theta and math.fabs(time_delta) > 1:
    #             last_spike = ms + 1
    #             epsp_inputs = np.array([])
    #
    #     # Plot membrane potential.
    #     pylab.plot(time[T_MIN:test_length], ps[T_MIN:test_length])
    #     pylab.xlabel('Time (ms)')
    #     pylab.ylabel('Membrane Potential (Arbitrary Units)')
    #     pylab.title('Sample LIF Neuron')
    #     pylab.show()

    def plot_stdp(self):
        """
        Plot STDP from both LTD and LTP.
        :return: Void.
        """
        self.plot_ltd(False)
        self.plot_ltp(False)
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        pylab.xlabel('Time Delta (ms)')
        pylab.ylabel('Weight Change from STDP')
        pylab.xlim(-1 * self.ltp_window, self.ltd_window)
        pylab.title('Effect of STDP on Synaptic Weights')
        pylab.show()