__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import pymongo
from action_selection.action_selection import ActionSelection


class ActionSelectionDao:

    def __init__(self, database):
        self.db = database
        self.collection = self.db.action_selections

    def save(self, a_s):
        """
        Saves the action selection simulation to the database.
        :return: _id of simulation inserted.
        """

        # General action data.
        a_s = {
            'description': a_s.description,
            'tau_m': a_s.taum,
            'tau_pre':  a_s.taum
        }

        # Save general data.
        _id = self.collection.insert(a_s)

        return _id

    def get_simulations(self, num_simulations):
        """
        Fetches a given number of simulations from the database.
        :param num_simulations: Number of simulations to fetch.
        :return: Array of simulations.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_simulations)
        simulations = cursor.toArray()

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
                       num_synapses,
                       synaptic_distance,
                       duration_per_frame,
                       description):
        """
        Generates and saves a simulation.
        """

        # Get the input.

        # Instatiate an ActionSelection object.
        a_s = ActionSelection()

        # Save video to filesystem.

        # Save action selection simulation.
        _id = self.save(a_s)

        return _id

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter
