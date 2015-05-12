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
    def make_temp_directory(name):
        """
        Create empty directory with name "name".
        :param name: Name of empty directory we want to create.
        :return:
        """

        if os.path.exists(name):
            shutil.rmtree(name)

        os.makedirs(name)

    def test_create_video(self):
        """

        :return:
        """

        test = Animation()
        test.add_target(2)

        local_dir = "out_directories"
        name = "test.avi"
        path = local_dir + "/" + name
        Training.make_temp_directory(local_dir)

        test.run(path, 10, 10)


if __name__ == '__main__':
    t = Training()
    t.test_create_video()