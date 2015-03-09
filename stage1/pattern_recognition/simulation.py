__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import math
from copy import deepcopy
import sys

from stage1.pattern_recognition import neuron
import pylab
from matplotlib.patches import Rectangle
import numpy as np



# Import simulation_dao for saving.
#TODO: Uncomment
# server = os.path.abspath(os.path.join("..", "..", "..", "server"))
# sys.path.append(server)
# import simulation_dao


class Simulation:
    """
    Simulation of a given number of afferents firing into a pattern
    recognition neuron over a given number of time steps.
    """
    # Defaults
    A_PLUS = neuron.Neuron.A_PLUS
    A_RATIO = neuron.Neuron.A_RATIO
    THETA = neuron.Neuron.THETA

    def __init__(self, description=None):
        self.t_min = 0                   # Start time in ms.
        self.t_step = 1                  # Time step in ms.
        self.spike_trains = None
        self.start_positions = None
        self.num_afferents = None
        self.neurons = []
        self.pattern_duration = None
        self.duration = None
        self.savable = True
        self.sampling_interval = None
        self.description = description

    def load_file(self, filename, folder="samples/", extension=".npz"):
        """
        Loads a file containing sample spike trains.
        :param filename: Name of file with spike trains.
        :param folder: Folder containing sample files.
        :param extension: Filename extension.
        :return: None.
        """
        path = folder + filename + extension
        sample = np.load(path)
        self.spike_trains = sample['spike_trains']
        self.start_positions = sample['start_positions']
        self.pattern_duration = sample['pattern_duration']
        self.num_afferents = self.spike_trains.shape[0]
        self.duration = self.spike_trains.shape[1]
        self.sampling_interval = math.ceil(self.duration / 5)

    def load(self, sample):
        """
        Loads a sample.
        :param sample: Sample
        :return: None.
        """
        self.spike_trains = sample.spike_trains
        self.start_positions = sample.start_positions
        self.pattern_duration = sample.pattern_duration
        self.num_afferents = self.spike_trains.shape[0]
        self.duration = self.spike_trains.shape[1]
        self.sampling_interval = math.ceil(self.duration / 5)

    def add_neuron(self, a_plus=A_PLUS, a_ratio=A_RATIO, theta=THETA):
        """
        Adds neuron to simulation.
        :return: Neuron.
        """
        n = neuron.Neuron(self.num_afferents, a_plus, a_ratio, theta)
        self.neurons.append(n)
        return n

    def plot_weight_distributions(self):
        # Values for plotting weights.
        frame = 1
        frames = 5
        bin_size = 50
        frame_step = self.duration / frames
        rows = frames + 1

        # Plot weight distribution at given intervals.
        for ms in range(self.duration):
            if ms % frame_step == 0:
                self.neurons[0].plot_weight_distribution(ms, rows,
                                                         current_frame=frame,
                                                         bin_size=bin_size)
                frame += 1

        # Plot final weight distribution.
        self.neurons[0].plot_weight_distribution(self.duration, rows,
                                                 current_frame=frame,
                                                 bin_size=bin_size)

    def run(self, save_weights=False):
        """
        Runs a simulation.
        :param save_weights: Saves all historic weights. Only for debugging.
        :return: None.
        """

        # If weights are being saved, simulation is not savable.
        self.savable = not save_weights

        # Reset neurons.
        for i in range(len(self.neurons)):

            # Clear spike times container.
            self.neurons[i].spike_times = []

            # Create container for results.
            self.neurons[i].potential = [j for j in range(self.duration + 1)]

        # Get membrane potential at each given point.
        for ms in range(0, self.duration - 1):

            for n in self.neurons:

                # Update time delta.
                if len(n.spike_times) > 0:
                    n.time_delta = ms - n.spike_times[-1]

                # Shape spikes.
                spikes = deepcopy(self.spike_trains[:, ms])
                spikes = np.reshape(spikes, (n.num_afferents, 1))

                # Update EPSP inputs.
                n.update_epsps(spikes)

                # Send inhibitory signal to sibling neurons.
                if n.time_delta == 0:
                    n.ipsps = np.array([])
                    for s in n.siblings:
                        s.update_ipsps(ms)

                # Calculate membrane potential.
                p = n.calculate_membrane_potential(ms)

                # Update LTP window width.
                n.update_ltp_window_width(ms)

                # Post the potential to the next ms.
                n.potential[ms + 1] = p

                # Record weights at this point only if running with flag.
                if save_weights:
                    if n.historic_weights.size == 0:
                        n.historic_weights = self.neurons[0].current_weights
                    else:
                        n.historic_weights = np.hstack((n.historic_weights,
                                                        n.current_weights))

                # Save weight distribution if at interval.
                if ms % self.sampling_interval == 0:
                    n.save_weight_distributions()

                # Update weights.
                n.update_weights(self.spike_trains, ms)

                # If threshold has been met and more than 1 ms has elapsed
                # since the last post-synaptic spike, schedule a spike.
                if p >= n.theta and (n.time_delta > 1 or n.time_delta is None):
                    n.spike_times.append(ms + 1)

            # Progress bar.
            progress = (ms / float(self.duration - 1)) * 100
            sys.stdout.write("Processing spikes: %d%% \r" % progress)
            sys.stdout.flush()

    def plot_weights(self):
        start = self.t_min
        end = self.duration - 1

        # Container for time.
        time = np.arange(start, end, 1, dtype=np.int32)

        # Sample 1% of available afferents.
        neuron_sample_size = int(self.neurons[0].num_afferents * 0.01)

        # Plot sample neurons' weight over time.
        for i in range(0, neuron_sample_size):
            pylab.plot(time[start:end],
                       self.neurons[0].historic_weights[i, start:end])
            pylab.xlabel('Time (ms)')
            pylab.ylabel('Weight')
            pylab.title('Synaptic Weight')
        pylab.show()

    def plot_membrane_potential(self):
        start = self.t_min
        end = self.duration

        # Container for time.
        time = np.arange(start, end, 1, dtype=np.int32)

        # Up to five colors supported.
        colors = ["#E6E6E6", "#CCFFCC", "#FFCC99", "#CCFFFF", "#FFFFCC"]

        # Prepare the pattern plot.
        for i in range(len(self.start_positions)):
            color = colors[i % len(colors)]
            min_y = self.neurons[0].theta * -0.5
            max_y = self.neurons[0].theta * 2.25
            for j in self.start_positions[i]:
                pylab.gca().add_patch(Rectangle((j, min_y),
                                                self.pattern_duration,
                                                max_y + math.fabs(min_y),
                                                facecolor=color,
                                                edgecolor=color))

        # Plot membrane potential for each neuron.
        for n in self.neurons:
            pylab.plot(time[start:end], n.potential[start:end])
            pylab.ylim(min_y, max_y)

        # Prepare and display plot.
        pylab.xlabel('Time (ms)')
        pylab.ylabel('Membrane Potential')
        pylab.title('Spike Train with STDP')
        pylab.show()


# Run Sample Test
# ===============
# sample = poisson_pattern_generator.generate_sample(num_neurons,
#                                                    test_length,
#                                                    pattern_len)
if __name__ == '__main__':
    sim = Simulation()
    # sim.load("3_500_50000_50_0.1_0.5_10.0")
    sim.load_file("combined_50k")
    n1 = sim.add_neuron(0.03125, .95, 125)
    # n2 = sim.add_neuron(0.03125, 0.91, 125)
    # n3 = sim.add_neuron(0.03125, 0.91, 125)
    # n1.connect(n2)
    # n1.connect(n3)
    # n2.connect(n3)
    sim.run()
    # sim.plot_weights()
    sim.plot_membrane_potential()


    # Save simulation to database.
    # connection_string = "mongodb://localhost"
    # connection = pymongo.MongoClient(connection_string)
    # db = connection.anisopter
    # simulations = simulation_dao.SimulationDao(db)
    # simulations.save(sim)