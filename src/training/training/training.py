__author__ = 'eg1114'


import shutil
import os

import pymongo

from animation.target_animation import *
import estmd_dao


class Training(object):
    """
    Main class to execute training of other modules.
    User interacts with only two functions:
     - set_stuff: TO DO !!!!!!!!!!!!!!!                   ########### TO DO
     - run_tests: which sets types and frequency of tests
    """

    def __init__(self, input_id, types, n):
        """
        Constructor.
        :param types: Corresponds to how many tests of each type should we run.
                      They correspond to:
                       [vertical, horizontal, diagonal, anti-diagonal]
        :param reps: How many times should we run each test case.
        :return:
        """

        self.types = types
        self.n = n
        self.id = input_id

        host = "146.169.47.184"
        port = 27017
        db_name="anisopter"
        connection = pymongo.MongoClient(host=host, port=port)
        db = connection[db_name]

        estmd = estmd_dao.EstmdDao(db)
        output = estmd.get_simulation(self.id)
        print output

    @staticmethod
    def make_temp_directory(name):
        """
        Create empty directory with name "name".
        :param name: Name of empty directory we want to create.
        :return:
        """

        if os.path.exists(name):
            shutil.rmtree(name)

        os.makedirs(name)

    def single_test(self, start, vel, path, n):
        """

        :param start: Starting position.
        :param vel: Velocity vector.
        :param id: Id of video.
        :param n: how many times should you run this test.
        :return:
        """

        test = Animation()
        test.add_target(2, start=start, velocity=vel, size=5, v=8)

        test.run(path, 10, 20)

    def create_tests(self, type, dif, n):
        """

        :param type: Type of test 0-3:
                  [0, 1, 2, 3] = [vertical, horizontal, diagonal, anty-diagonal]
        :param dif: Number of different tests.
        :param n: Number of test repetitions
        :return:
        """

        for i in range(dif):
            # TO DO: adjust
            start = []
            # Run single test.

    def run(self):
        """
        Run stuff and save stuff.

        :return:
        """



if __name__ == '__main__':
    t = Training()