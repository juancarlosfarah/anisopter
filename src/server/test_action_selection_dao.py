__author__ = 'eg1114'

import unittest
import action_selection_dao
import pymongo
import numpy as np


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
        self.dao = action_selection_dao.ActionSelectionDao(db)
        self.dao.collection.drop()

    def test_all(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """


        id = self.dao.run_simulation_preprocessor()
        self.dao.get_simulation(id)
        self.dao.get_simulations(1)

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
