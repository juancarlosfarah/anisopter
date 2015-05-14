__author__ = 'eg1114'

import unittest
import animation_dao
import estmd_dao
import cstmd_dao
import pymongo


class SampleDaoTests(unittest.TestCase):

    def setUp(self):
        """
        Creates a SimulationDao to test on.
        :return: None.
        """
        
        host = "146.169.47.184"
        port = 27017
        connection = pymongo.MongoClient(host=host, port=port)
        db = connection["anisopter"].test
        self.dao_animi = animation_dao.AnimationDao(db)
        self.dao_estmd = estmd_dao.EstmdDao(db)
        self.dao_cstmd = cstmd_dao.CstmdDao(db)
        self.dao_animi.collection.drop()
        self.dao_estmd.collection.drop()
        self.dao_cstmd.collection.drop()
        

    def test_all(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """

        width = 640
        height = 480
        description = "Test"
        targets = [{ 'color': 'rgb(20,97,107)',
                     'velocity': '5',
                     'velocity_vector': ['1', '2'],
                     'type': '1',
                     'start_pos': ['1', '2'],
                     'frames': '50',
                     'size': '1' }]
        frames = 20
        background = ""
        background_speed = 0

        H_filter = "[[-1, -1, -1, -1, -1],[-1,  0,  0,  0, -1],[-1,  0,  2,  0, -1],[-1,  0,  0,  0, -1],[-1, -1, -1, -1, -1]]"

        b = "[0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]"
        a = "[1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]"

        CSKernel = "[[-1.0 / 9.0, -1.0 / 9.0, -1.0 / 9.0],[-1.0 / 9.0,  8.0 / 9.0, -1.0 / 9.0],[-1.0 / 9.0, -1.0 / 9.0, -1.0 / 9.0]]"

        b1 = "[1.0, 1.0]"
        a1 = "[51.0, -49.0]"


        id = self.dao_animi.generate_animation(width, height, description,
                                               targets,frames, background,
                                               background_speed)

        id2 = self.dao_estmd.run_simulation(id, "test", H_filter, b, a,
                                            CSKernel, b1, a1)

        self.dao_estmd.get_simulation(id2)
        self.dao_estmd.get_simulations(1)
        
        frames = []
        for i in range(10) :
            frames.append({'frame': [0 for i in range(32*32)]})

        sample = {'_id':id, 'animation_id':id2}
        num_neurons = 1
<<<<<<< HEAD
        num_electrodes = 5
        num_synapses = 5
        synaptic_distance = 5
        duration_per_frame = 1
=======
        num_electrodes = 1
        num_synapses = 1
        synaptic_distance = 1
        duration_per_frame = 1

        frames = []
        for i in range(10) :
            frames.append({'frame': [0 for i in range(32*32)]})
>>>>>>> ec4d0807b51422664be8a289373930151db554fc

        id3 = self.dao_cstmd.run_simulation(sample,
                           frames,
                           num_neurons,
                           num_electrodes,
                           num_synapses,
                           synaptic_distance,
                           duration_per_frame,
                           description)

        self.dao_cstmd.get_simulation(id3)
        self.dao_cstmd.get_simulations(1)

    def tearDown(self):
        """
        Resets the sample for the tests.
        :return:
        """
        self.dao = None


def main():
    unittest.main()

if __name__ == '__main__':
    main()
