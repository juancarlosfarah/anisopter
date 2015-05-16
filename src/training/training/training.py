__author__ = 'eg1114'


import shutil
import os

import pymongo

from animation.target_animation import *


class Training(object):
    """
    Main class to execute training of other modules.
    User interacts with only two functions:
     - set_stuff: TO DO !!!!!!!!!!!!!!!                   ########### TO DO
     - run_tests: which sets types and frequency of tests
    """

    def __init__(self, types, n, ani, estmd, cstmd, sim):
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
        self.ani = ani
        self.estmd = estmd
        self.cstmd = cstmd
        self.sim = sim


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


        self.ani.add_target(2, start=start, velocity=vel, size=5, v=8)
        self.ani.run(path, 15, 25)


    def create_tests(self, type, dif, n):
        """

        :param type: Type of test 0-3:
                  [0, 1, 2, 3] = [vertical, horizontal, diagonal, anty-diagonal]
        :param dif: Number of different tests.
        :param n: Number of test repetitions
        :return:
        """

        pass

    def run(self):
        """
        Run stuff and save stuff.

        :return:
        """
        out_dir = "out_directories"
        name = "test1"
        out_path = out_dir + "/" + name

        self.make_temp_directory(out_dir)
        self.ani.run(out_path)
        self.estmd.open_movie(out_path)
        self.estmd.run(by_frame=True)

        frame_array = e.run(by_frame=True)

        print frame_array[10]


if __name__ == '__main__':
    t = Training()
