__author__ = 'eg1114'

import unittest
import training_dao
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
        self.dao = training_dao.TrainingDao(db)
        self.dao.collection.drop()

    def test_all(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """

        input_id = str("kvenkakvenka")
        types = [1, 1, 1, 1]
        n = 1

        self.dao.generate_training_simulation(input_id, types, n)

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