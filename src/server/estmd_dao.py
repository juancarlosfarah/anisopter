__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import os
import sys
import pymongo

from estmd.estmd import ESTMD


class EstmdDao:

    def __init__(self, database):
        self.db = database
        self.collection = self.db.estmd
        self.frames = self.db.frames

    def save(self, estmd):
        """
        Saves the ESTMD simulation to the database.
        :return: _id of simulation inserted.
        """

        # General simulation data.
        sim = {
            'description': estmd.description
        }

        _id = self.collection.insert(sim)

        # Save the frames.
        collection = self.db.frames
        for frame in estmd.frames:
            obj = {
                "sample_id": _id,
                "frame": frame.ravel().tolist()
            }
            collection.insert(obj)

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
                    'description': simulation['description']
                })

        return simulations

    def get_frames(self, _id):
        """
        Fetches the frames of a given simulation.
        :param _id: Simulation ID.
        :return: Cursor containing frames.
        """
        cursor = self.frames.find({'simulation_id': ObjectId(_id)})\
                            .sort([('_id', pymongo.ASCENDING)])

        return cursor

    def get_simulation(self, _id):
        """
        Fetches an simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        simulation = self.collection.find_one({'_id': ObjectId(_id)})
        if "description" not in simulation:
            simulation['description'] = "Description"
        simulation['date'] = simulation['_id'].generation_time
        return simulation

    def run_simulation(self, sample_id):
        """
        Runs and saves the output simulation.
        :return: _id of simulation generated.
        """

        input_directory = "assets/animations/" + sample_id + ".avi"

        e = ESTMD()
        e.open_movie(input_directory)
        e.run(by_frame=True)
        e.create_list_of_arrays()

        _id = self.save(e)

        return _id

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter