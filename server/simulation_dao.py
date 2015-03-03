__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId


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

        return sim