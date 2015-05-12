__author__ = 'eg1114'


import shutil
import os

from animation.target_animation import *


class Training(object):
    """
    Main class to execute training of other modules.
    """

    def __init__(self):
        """
        Constructor.
        :return:
        """

        pass

    @staticmethod
    def make_temp_directory(self, name):
        """
        Create empty directory with name "name".
        :param name: Name of empty directory we want to create.
        :return:
        """

        if os.path.exists(name):
            shutil.rmtree(name)

        os.makedirs(name)


if __name__ == '__main__':
    test = Training()
    test.only_function()