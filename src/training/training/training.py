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

    def create_video(self, start, vel, id):
        """

        :param start: Starting position.
        :param vel: Velocity vector.
        :param id: Id of video.
        :return:
        """

        test = Animation()
        test.add_target(2)
        test.add_target(2, start=start, velocity=vel, size=5, v=8)

        local_dir = "out_directories"
        name = "test" + str(id) + ".avi"
        path = local_dir + "/" + name
        Training.make_temp_directory(local_dir)

        print "---------------------------------------------"
        print path
        test.run(path, 10, 20)

    def test_sequence_videos(self):

        starts = [[200, 10], [400, 10], [400, 300]]
        dirs = [[0, 1], [-1, 1], [-1, 0]]

        for s, d, i in zip(starts, dirs, range(len(starts))):
            self.create_video(s, d, i)


if __name__ == '__main__':
    t = Training()
    t.test_sequence_videos()