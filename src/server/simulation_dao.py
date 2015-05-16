__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import matplotlib
matplotlib.use('Agg')   # Do not load the GTK. (Doesn't support show()).
import numpy as np
import mpld3
import pylab
import os
import sys
import math
from matplotlib.patches import Rectangle

from pattern_recognition.simulation import Simulation


class SimulationDao:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.collection = self.db.simulations

    def save(self, sim, animation_id, estmd_id, cstmd_id):
        """
        Saves the simulation to the database.
        :return: None.
        """

        if not sim.savable:
            print "Cannot save this simulation in the database."
            return

        # Strip down neurons.
        neurons = []
        for n in sim.neurons:
            obj = {
                "tau_m": n.tau_m,
                "tau_s": n.tau_s,
                "spike_times": n.spike_times,
                "potential": n.potential,
                "t_plus": n.t_plus,
                "t_minus": n.t_minus,
                "ltp_window": n.ltp_window,
                "ltd_window": n.ltd_window,
                "t_window": n.t_window,
                "alpha": n.alpha,
                "theta": n.theta,
                "k": n.k,
                "k1": n.k1,
                "k2": n.k2,
                "weight_max": n.weight_max,
                "weight_min": n.weight_min,
                "a_plus": n.a_plus,
                "a_minus": n.a_minus,
                "weights": n.current_weights.flatten().tolist(),
                "weight_distributions": n.weight_distributions,
            }

            neurons.append(obj)

        sim = {
            "start_positions": sim.start_positions,
            "num_afferents": sim.num_afferents,
            "neurons": neurons,
            "pattern_duration": sim.pattern_duration,
            "duration": sim.duration,
            "description": sim.description,
            "animation_id": animation_id,
            "cstmd_id": cstmd_id,
            "estmd_id": estmd_id
        }
        _id = self.collection.insert(sim)
        return _id

    def get_simulations(self, num_simulations, from_animation=False): 
        """
        Fetches a given number of simulatons from the database.
        :param num_simulations: Number of simulations to fetch.
        :return: Array of simulations.
        """
        c = self.collection
        if not from_animation:
            cursor = c.find()
        else:
            cursor = c.find({"animation_id": {"$ne": None}})

        cursor.sort('_id', direction=-1).limit(num_simulations)
        sims = []
        for sim in cursor:
            if "description" not in sim:
                sim['description'] = "Description"
            sims.append(
                {
                    '_id': sim['_id'],
                    'date': sim['_id'].generation_time,
                    'description': sim['description'],
                    'num_afferents': sim['num_afferents'],
                    'duration': sim['duration'],
                    'num_neurons': len(sim['neurons'])
                })

        return sims

    def get_simulation(self, _id, return_object=False):
        """
        Fetches a simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        sim = self.collection.find_one({'_id': ObjectId(_id)})
        duration = sim['duration']
        patterns = sim["start_positions"]
        p_plots = []

        # Plot first second if available.
        if duration >= 1000:
            p_plots.append(self.plot_membrane_potential(sim, 0, 1000))

        # Plot last second if over two seconds long.
        if duration >= 2000:
            p_plots.append(self.plot_membrane_potential(sim,
                                                        (duration - 1000),
                                                        duration))

        sim['potential_plots'] = p_plots
        wd_plots = self.plot_weight_distributions(sim)
        for i in range(len(sim['neurons'])):
            sim['neurons'][i]['weight_distribution_plot'] = wd_plots[i]

        if len(patterns) > 0:
            spike_info = self.get_neuron_info(sim)

            # Currently we only get spike-timing info
            # for the first neuron for one pattern.
            # TODO: Expand to all neurons.
            sim['neurons'][0]['spike_info'] = spike_info

        if return_object:
            description = sim['description']
            training = True

            s = Simulation(description, training)

            return s

        return sim

    def plot_weight_distributions(self, simulation):

        # Plot weight distribution at given intervals.
        plots = []
        for n in simulation['neurons']:
            frame = 1
            frames = 5
            rows = frames + 1
            cols = 1
            f = pylab.figure()
            for dist in n['weight_distributions']:
                # Plot a histogram of the values.
                p = pylab.subplot(rows, cols, frame)

                # Only add title to first plot.
                if frame == 1:
                    pylab.title('Weight Distribution Over Time')

                p.axes.get_xaxis().set_visible(False)
                p.axes.get_yaxis().set_ticks([])
                p.bar(np.arange(0, 1, 0.1), dist, 0.1)

                # Only show if plot is complete.
                if rows * cols == frame:
                    pylab.xlabel("Weight Value")
                    p.axes.get_xaxis().set_visible(True)
                frame += 1
            plots.append(mpld3.fig_to_html(f))
            pylab.close(f)
        return plots

    def plot_membrane_potential(self, simulation, start, end):

        f = pylab.figure()
        pattern_duration = simulation["pattern_duration"]

        # Container for time.
        time = np.arange(start, end, 1, dtype=np.int32)
        # Up to five colors supported.
        colors = ["#E6E6E6", "#CCFFCC", "#FFCC99", "#CCFFFF", "#FFFFCC"]

        # Prepare the pattern plot.
        min_y = simulation['neurons'][0]['theta'] * -0.75
        max_y = simulation['neurons'][0]['theta'] * 2.25
        for i in range(len(simulation['start_positions'])):
            start_pos = simulation['start_positions'][i]
            color = colors[i % len(colors)]
            for j in start_pos:
                if start <= j <= (end - pattern_duration):
                    pylab.gca().add_patch(Rectangle((j, min_y),
                                                    pattern_duration,
                                                    max_y + math.fabs(min_y),
                                                    facecolor=color,
                                                    edgecolor=color))

        # Plot membrane potential for each neuron.
        for n in simulation['neurons']:
            pylab.plot(time, n['potential'][start:end])
            pylab.ylim(min_y, max_y)

        # Prepare and display plot.
        pylab.xlabel('Time (ms)')
        pylab.ylabel('Membrane Potential')

        plot = mpld3.fig_to_html(f)
        pylab.close(f)
        return plot 

    def get_neuron_info(self, simulation):
        """
        Get spike-timing information for each neuron.
        :param simulation:
        :return:
        """
        # Container for return value.
        rvalue = []

        # Currently we only get spike-timing info
        # for the first neuron for one pattern.
        # TODO: Expand to all neurons.
        pattern_duration = simulation["pattern_duration"]
        duration = simulation["duration"]
        neurons = simulation["neurons"]
        patterns = simulation["start_positions"]
        n = neurons[0]

        # Split start positions and spikes into 4 arrays.
        split = duration / 4
        pattern = np.array(patterns[0])
        spikes = np.array(n["spike_times"])
        for i in range(1, 5):
            p = pattern[split * (i - 1) <= pattern]
            p = p[p < split * i]
            s = spikes[split * (i - 1) <= spikes]
            s = s[s < split * i]

            f_positives = 0.0
            t_positives = 0.0
            num_spikes = s.size
            num_patterns = p.size
            to_delete = []
            for spike in s:
                matched = False
                for j in range(p.size):
                    start_pos = p[j]
                    if 0 <= spike - start_pos <= pattern_duration:
                        t_positives += 1
                        to_delete.append(j)
                        matched = True
                if not matched:
                    f_positives += 1

            # Remove patterns that contain a spike
            # and calculate false negatives.
            p_left = np.delete(p, to_delete)
            f_negatives = float(p_left.size)

            # Package results and append to return value.
            rate_t_positives = 0
            rate_f_positives = 0
            rate_f_negatives = 0
            if num_spikes != 0:
                rate_t_positives = t_positives / num_spikes * 100
                rate_f_positives = f_positives / num_spikes * 100
            if num_patterns != 0:
                rate_f_negatives = f_negatives / num_patterns * 100
            results = [rate_t_positives,
                       rate_f_positives,
                       rate_f_negatives]
            rvalue.append(results)

        return rvalue

    def run_simulation(self,
                       sample,
                       cursor,
                       num_neurons,
                       description,
                       a_plus,
                       a_ratio,
                       theta,
                       weights,
                       training,
                       return_object = False):

        sim = Simulation(description, training)

        sim.load_sample(sample, cursor)

        # Add the post-synaptic neurons and connect them.
        neurons = []
        for i in range(num_neurons):
            if weights is not None:
                weight = weights[i]
            else:
                weight = None
            n = sim.add_neuron(a_plus, a_ratio, theta, weight)
            for neuron in neurons:
                n.connect(neuron)

        sim.run()

        # Allow for simulations run on generated samples.
        if 'animation_id' not in sample:
            sample['animation_id'] = None

        if 'estmd_id' not in sample:
            sample['estmd_id'] = None

        _id = self.save(sim,
                        sample['animation_id'],
                        sample['estmd_id'],
                        sample['_id'])
        return _id


if __name__ == "__main__" and __package__ is None:
    print "Running!"
    # s = SimulationDao()
    # s.run_simulation()
