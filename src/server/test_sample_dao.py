__author__ = 'juancarlosfarah'

import unittest
import sample_dao
import pymongo


class SampleDaoTests(unittest.TestCase):

    def setUp(self):
        """
        Creates a SimulationDao to test on.
        :return: None.
        """
        connection_string = "mongodb://localhost"
        connection = pymongo.MongoClient(connection_string)
        db = connection.test
        self.dao = sample_dao.SampleDao(db)
        self.dao.collection.drop()

    def test_dao(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """

        # Test saving.
        duration = 1000
        num_neurons = 100
        num_patterns = 1
        description = "Test_1"
        _id = self.dao.generate_sample(duration,
                                       num_neurons,
                                       num_patterns,
                                       description)

        # Test retrieving one.
        doc = self.dao.get_sample(_id)
        self.failUnless(doc['_id'] == _id)
        self.failUnless(doc['duration'] == 1000)
        self.failUnless(doc['num_efferents'] == 100)
        self.failUnless(len(doc['start_positions']) == 1)
        self.failUnless(doc['description'] == "Test_1")

        # Save another sample.
        d = 500
        num_neurons = 100
        num_patterns = 1
        desc = "Test_2"
        self.dao.generate_sample(d, num_neurons, num_patterns, desc)

        # Test retrieving many.
        samples = self.dao.get_samples(5)
        self.failUnless(len(samples) == 2)

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