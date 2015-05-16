__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import numpy as np
import os
from subprocess import call

from bson.objectid import ObjectId
import pymongo
from estmd.estmd import ESTMD


class EstmdDao(object):

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
            'description': estmd.description,
            'animation_id': estmd.input_id,
            'h_filter': estmd.H_filter.tolist(),
            'b': estmd.b,
            'a': estmd.a,
            'cs_kernel': estmd.CSKernel.tolist(),
            'b1': estmd.b1,
            'a1': estmd.a1
        }

        _id = self.collection.insert(sim)

        # Save the frames.
        collection = self.db.frames
        for frame in estmd.frames:
            obj = {
                "simulation_id": _id,
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

    def get_simulation(self, _id, return_object=False):
        """
        Fetches an simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        simulation = self.collection.find_one({'_id': ObjectId(_id)})
        if "description" not in simulation:
            simulation['description'] = "Description"
        simulation['date'] = simulation['_id'].generation_time

        if return_object:
            print simulation.keys()

            sample_id = simulation.get('animation_id')
            description = simulation.get('description')
            H_filter = simulation.get('h_filter')
            b = simulation.get('b')
            a = simulation.get('a')
            CSKernel = simulation.get('cs_kernel')
            b1 = simulation.get('b1')
            a1 = simulation.get('a1')

            e = self.run_simulation(sample_id, description, H_filter,
                                          b, a, CSKernel, b1, a1, True)

            return e

        return simulation

    def run_simulation(self, sample_id, description, H_filter, b, a,
                       CSKernel, b1, a1, return_object=False):
        """
        Runs and saves the output simulation.
        :return: _id of simulation generated.
        """

        input_directory = "assets/animations/" + str(sample_id) + ".avi"

        H_filter = np.array(eval(H_filter))
        b = eval(b)
        a = eval(a)
        CSKernel = np.array(eval(CSKernel))
        b1 = eval(b1)
        a1 = eval(a1)

        e = ESTMD(sample_id, description, H_filter, b, a, CSKernel, b1, a1)

        if return_object:
            return e

        e.open_movie(input_directory)
        e.run(by_frame=True)
        e.create_list_of_arrays()
        _id = self.save(e)

        # Save video file.
        relative_path = "assets/estmd/"
        out_directory = os.path.abspath(relative_path + str(_id) + ".avi")

        e.open_movie(input_directory)
        e.run(out_dir=out_directory)

        dir = out_directory.strip(".avi")
        command = "avconv -i %s.avi -c:v libx264 -c:a copy %s.mp4" % (dir, dir)
        call(command.split())

        return _id


if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter
