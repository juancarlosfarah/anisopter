__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import mpld3
import pylab
import math
from matplotlib.patches import Rectangle


class SimulationDao:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.collection = self.db.simulations

    def save(self, simulation):
        """
        Saves the simulation to the database.
        :return: None.
        """

        if not simulation.savable:
            print "Cannot save this simulation in the database."
            return

        # Strip down neurons.
        neurons = []
        for n in simulation.neurons:
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
                "weight_distributions": n.weight_distributions
            }

            neurons.append(obj)

        simulation = {
            "start_positions": simulation.start_positions.tolist(),
            "num_afferents": simulation.num_afferents,
            "neurons": neurons,
            "pattern_duration": simulation.pattern_duration,
            "duration": simulation.duration
        }
        self.collection.insert(simulation)

    def get_simulations(self, num_simulations):
        """
        Fetches a given number of simulatons from the database.
        :param num_simulations: Number of simulations to fetch.
        :return: Array of simulations.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_simulations)
        sims = []

        for sim in cursor:
            sims.append(
                {
                    '_id': sim['_id'],
                    'date': sim['_id'].generation_time,
                    'body': sim['num_afferents'],
                    'duration': sim['duration'],
                    'num_neurons': len(sim['neurons'])
                })

        return sims

    def get_simulation(self, _id):
        """
        Fetches a simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        sim = self.collection.find_one({'_id': ObjectId(_id)})
        duration = sim['duration']
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
        sim['weight_distribution_plots'] = self.plot_weight_distributions(sim)

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
        pylab.title('Spike Train')

        plot = mpld3.fig_to_html(f)
        return plot