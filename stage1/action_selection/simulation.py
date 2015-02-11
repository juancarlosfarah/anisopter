__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import poisson_pattern_generator
import srm_lif_neuron


class Simulation:
    """
    Simulation of a given number of afferents firing into a pattern recognition
    neuron over a given number of time steps.
    """
    def __init__(self):
        self.t_min = 0                   # Start time in ms.
        self.t_step = 1                  # Time step in ms.
        self.spike_trains = None
        self.start_positions = None
        self.num_afferents = None
        self.neurons = []
        self.pattern_len = None
        self.test_length = None

    def load(self, filename, folder="samples/", extension=".npz"):
        path = folder + filename + extension
        sample = poisson_pattern_generator.load_sample(path)
        self.spike_trains = sample['spike_trains']
        self.start_positions = sample['start_positions']
        params = map(float, filename.split("_"))
        self.num_afferents = int(params[1])
        self.test_length = int(params[2])
        self.pattern_len = int(params[3])

    def run(self, num_neurons):
        # Instantiate neuron with given number of afferents.
        for i in range(num_neurons):
            self.neurons.append(srm_lif_neuron.Neuron(self.num_afferents))



# Run Sample Test
# ===============
# sample = poisson_pattern_generator.generate_sample(num_neurons,
#                                                    test_length,
#                                                    pattern_len)


# Create container for results.
ps = [T_MIN for i in range(test_length + 1)]
time = np.arange(T_MIN, test_length, 1, dtype=np.int32)

# Set last spike to an irrelevant value at first.
last_spike = 0 - max(neuron.ltd_window, neuron.ltp_window, neuron.t_window)
penultimate_spike = last_spike

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
    neuron_numbers.append(np.random.randint(0, neuron.num_afferents))
    container = [0] * test_length
    neuron_weights.append(container)

# Get membrane potential at each given point.
for ms in range(0, test_length - 1):
    spikes = deepcopy(spike_trains[:, ms])
    spikes = np.reshape(spikes, (neuron.num_afferents, 1))
    p = neuron.calculate_membrane_potential(ms, last_spike)
    neuron.update_epsp_inputs(spikes)

    # Post the potential to the next ms.
    ps[ms + 1] = p

    # Record sample neurons' weight at this point.
    for i in range(0, neuron_sample_size):
        neuron_weights[i][ms] = neuron.weights[neuron_numbers[i]][0]

    # Get relevant spikes for weight updating in LTP.
    ltp_window_start = max(0, ms - neuron.ltp_window, penultimate_spike + 1)
    ltp_window_end = ms + 1
    spikes = deepcopy(spike_trains[:, ltp_window_start:ltp_window_end])

    # Update weights.
    time_delta = ms - math.fabs(last_spike)
    neuron.update_weights(spikes, time_delta)

    # Plot weight distribution at given intervals.
    if ms % frame_step == 0:
        neuron.plot_weights(ms, rows, current_frame=frame, bin_size=bin_size)
        frame += 1

    # If threshold has been met and more than 1 ms has elapsed
    # since the last post-synaptic spike, schedule a spike.
    if p >= neuron.theta and math.fabs(time_delta) > 1:
        penultimate_spike = last_spike
        last_spike = ms + 1
        epsp_inputs = np.zeros((neuron.num_afferents, 1))

    # Progress bar.
    progress = (ms / float(test_length - 1)) * 100
    sys.stdout.write("Processing spikes: %d%% \r" % progress)
    sys.stdout.flush()

# Plot final weight distribution.
neuron.plot_weights(test_length, rows, current_frame=frame, bin_size=bin_size)

# Plot sample neurons' weight over time.
for i in range(0, neuron_sample_size):
    pylab.plot(time[T_MIN:test_length], neuron_weights[i][T_MIN:test_length])
    pylab.xlabel('Time (ms)')
    pylab.ylabel('Weight')
    pylab.title('Synaptic Weight')
pylab.show()

# Prepare the pattern plot.
color = '#E6E6E6'
min_y = neuron.theta * -0.5
max_y = neuron.theta * 2.25
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