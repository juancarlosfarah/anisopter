__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import pymongo
from cstmd.cstmd import Cstmd


class CstmdDao:

    def __init__(self, database):
        self.db = database
        self.collection = self.db.cstmd

    def save(self, cstmd):
        """
        Saves the CSTMD1 simulation to the database.
        :return: _id of simulation inserted.
        """

        # Targets.
        targets = []

        # General simulation data.
        sim = {
            'description': cstmd.description,
            'num_neurons': cstmd.num_neurons,
            'num_synapses': cstmd.num_synapses,
            'num_electrodes': cstmd.num_electrodes,
            'max_current': cstmd.max_current,
            'min_current': cstmd.min_current,
            'min_weight': cstmd.min_weight,
            'max_weight': cstmd.max_weight,
            'num_pixels': cstmd.num_pixels,
            'duration': cstmd.duration,
            'potassium': cstmd.potassium,
            'sodium': cstmd.sodium,
            'synaptic_distance': cstmd.synaptic_distance
        }

        _id = self.collection.insert_one(sim)

        return _id

    def get_simulations(self, num_simulations):
        """
        Fetches a given number of simulations from the database.
        :param num_simulations: Number of simulations to fetch.
        :return: Array of simulations.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_simulations)
        simulations = []

        for simulation in cursor:
            if "description" not in simulation:
                simulation['description'] = "Description"
            simulations.append(
                {
                    '_id': simulation['_id'],
                    'date': simulation['_id'].generation_time,
                    'description': simulation['description'],
                    'num_neurons': simulation['num_neurons'],
                    'num_synapses': simulation['num_synapses'],
                    'num_electrodes': simulation['num_electrodes'],
                    'max_current': simulation['max_current'],
                    'min_current': simulation['min_current'],
                    'min_weight': simulation['min_weight'],
                    'max_weight': simulation['max_weight'],
                    'num_pixels': simulation['num_pixels'],
                    'duration': simulation['duration'],
                    'potassium': simulation['potassium'],
                    'sodium': simulation['sodium'],
                    'synaptic_distance': simulation['synaptic_distance']
                })

        return simulations

    def get_simulation(self, _id):
        """
        Fetches an simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        simulation = self.collection.find_one({'_id': ObjectId(_id)})

        return simulation

    def run_simulation(self,
                       sample,
                       frames,
                       num_neurons,
                       num_electrodes,
                       duration,
                       description):
        """
        Generates and saves a simulation.
        :param sample: Dictionary with information about input sample.
        :param frames: Cursor containing frames.
        :param num_neurons: Number of neurons.
        :param num_electrodes: Number of electrodes.
        :param duration: Duration of simulation.
        :param description: Optional description field.
        :return: _id of simulation generated.
        """

        cstmd = Cstmd(num_neurons=num_neurons,
                      num_synapses=500,
                      synaptic_distance=30,
                      num_electrodes,
                      duration=duration,
                      description=description)

        spike_trains = []
        for frame_object in frames:
            frame = np.array(frame_object['frame'])
            times, ids, spike_train = cstmd.run(rates=frame)
            spike_trains.append(spike_train)

        _id = self.save(cstmd)
        return _id

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter
