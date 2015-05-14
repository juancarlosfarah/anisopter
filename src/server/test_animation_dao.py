__author__ = 'eg1114'

import unittest
import animation_dao
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
        self.dao = animation_dao.AnimationDao(db)
        self.dao.collection.drop()

    def test_all(self):
        """
        Tests if a Sample can be saved and accessed.
        :return: None.
        """

        width = 640
        height = 480
        decription = "Test"
        targets = [{ 'color': 'rgb(20,97,107)',
                    'velocity': '5',
                    'velocity_vector': ['1', '2'],
                    'type': '1',
                    'start_pos': ['1', '2'],
                    'frames': '50',
                    'size': '1' }]
        frames = 20
        background = False
        background_speed = 0

        id = self.dao.generate_animation(width, height, decription, targets,
                                         frames, background, background_speed)

        self.dao.get_animation(id)
        self.dao.get_animations(1)
        self.dao.remove(id)

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
