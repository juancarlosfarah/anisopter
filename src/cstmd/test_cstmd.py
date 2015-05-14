"""
Unit tests for module CSTMD.
"""
from subprocess import call
import unittest
import pickle
import pymongo

from cstmd.cstmd import Cstmd
import cstmd_dao
import numpy as np
import os
import matplotlib


class TestCSTMD(unittest.TestCase):
    """
    This class represents sequence of tests for class CSTMD.
    """
    # Create an array of zeros
    frames = []
    for i in range(10) :
        frames.append({'frame': [0 for i in range(32*32)]})

    # Set up initial value for the CSTMD object
    num_neurons = 2
    num_electrodes=2
    num_synapses=500
    synaptic_distance=30
    duration_per_frame=10
    description="Test"


    # Initiate the CSTMD object
    cstmd = Cstmd(num_neurons=num_neurons,
              num_synapses=num_synapses,
              synaptic_distance=synaptic_distance,
              num_electrodes=num_electrodes,
              duration=duration_per_frame,
              description=description,
              input=frames)


    # Run simulation for the empty arrray
    times, cstmd.spike_trains = cstmd.run()


    def setUp(self):
        """
        Method that runs at start of each test.
        """
        self.perc_change_acceptable=50.0


    def test_plotting(self):
        """
        Test how plotting works.
        """

        db_name="anisopter"
        host = "146.169.47.184"
        port = 27017
        connection = pymongo.MongoClient(host=host, port=port)
        db = connection[db_name]

        dao = cstmd_dao.CstmdDao(db)
        id = dao.get_simulations(1)[0]['_id']

        self.cstmd.plot_fir_rate(id)
        self.plot_compart_act(id)



if __name__ == '__main__':
    unittest.main()


