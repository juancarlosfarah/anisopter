__author__ = 'juancarlosfarah'

import unittest
import simulation_dao
import pymongo


class SimulationDaoTests(unittest.TestCase):

    def setUp(self):
        """
        Creates a SimulationDao to test on.
        :return: None.
        """
        host = "146.169.47.184"
        port = 27017
        connection = pymongo.MongoClient(host=host, port=port)
        db = connection["anisopter"].test
        self.dao = simulation_dao.SimulationDao(db)
        self.dao.collection.drop()

    def test_dao(self):
        """
        Tests if a Simulation can be saved and accessed.
        :return: None.
        """

        # Test saving.
        duration = 1000
        num_neurons = 100
        num_patterns = 1
        description = "Test_1"
        _id = self.dao.run_simulation(duration,
                                      num_neurons,
                                      num_patterns,
                                      description)

        # Test retrieving one.
        doc = self.dao.get_simulation(_id)
        self.failUnless(doc['_id'] == _id)
        self.failUnless(doc['duration'] == 1000)
        self.failUnless(doc['num_efferents'] == 100)
        self.failUnless(len(doc['start_positions']) == 1)
        self.failUnless(doc['description'] == "Test_1")


        # Save another simulation.
        d = 500
        num_neurons = 100
        num_patterns = 1
        desc = "Test_2"
        self.dao.run_simulation(d, num_neurons, num_patterns, desc)

        # Test retrieving many.
        sims = self.dao.get_simulations(5)
        self.failUnless(len(sims) == 2)

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
