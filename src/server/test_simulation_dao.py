__author__ = 'eg1114'

import unittest
import animation_dao
import estmd_dao
import cstmd_dao
import simulation_dao
import sample_dao
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
        self.dao_simul = simulation_dao.SimulationDao(db)
        self.samples = sample_dao.SampleDao(db)
        self.dao_simul.collection.drop()
        self.samples.collection.drop()

    def test_all(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """


        sample = self.samples.generate_sample(100, 2, 2, "Random")

        id4 = self.dao_simul.run_simulation(sample, 1, 5, description, 1, 1, 1, 1, False)

        self.dao_simul.get_simulation(id4)
        self.dao_simul.get_simulations(1)

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