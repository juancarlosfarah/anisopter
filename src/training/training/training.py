__author__ = 'eg1114'


import shutil
import os

from animation.target_animation import *


class Training(object):
    """
    Main class to execute training of other modules.
    User interacts with only two functions:
     - set_stuff: TO DO !!!!!!!!!!!!!!!                   ########### TO DO
     - run_tests: which sets types and frequency of tests
    """

    def __init__(self):
        """
        Constructor.
        :return:
        """


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

    def run_tests(self, types=[1, 1, 1, 1], reps=1):
        """
        Function that runs selected tests on our modules.

        :param types: Corresponds to how many tests of each type should we run.
                      They correspond to:
                       [vertical, horizontal, diagonal, anty-diagonal]
        :param reps: How many times should we run each test case.
        :return:
        """

        self.types = types
        self.reps = reps


if __name__ == '__main__':
    t = Training()
    t.test_sequence_videos()