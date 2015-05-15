__author__ = 'eg1114'

import unittest
import sample_dao
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
        self.samples = sample_dao.SampleDao(db)
        self.samples.collection.drop()

    def test_all(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """


        id = self.samples.generate_sample(100, 5, 5, "Random")
        sample = self.samples.get_sample(id)
        c = self.samples.db.spikes
        cursor = c.find({'sample_id' : sample['_id']}).sort('_id', direction=1)
        
        self.samples.get_samples(1)
        self.samples.get_sample(id)
        self.get_spikes(id)

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