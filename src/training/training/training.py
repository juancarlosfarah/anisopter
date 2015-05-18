__author__ = 'eg1114'


import math
import os
import shutil
from subprocess import call

from animation.target_animation import Animation
from action_selection.action_selection import ActionSelection
from cstmd.cstmd import Cstmd
from estmd.estmd import ESTMD
from pattern_recognition.simulation import Simulation


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
        name = "test1.avi"
        out_path = os.path.abspath(os.path.join(out_dir, name))

        self.make_temp_directory(out_dir)

        self.ani.run(out_path, 10, 10)

        self.estmd.open_movie(out_path)
        self.estmd.run(by_frame=True)
        self.estmd.run(by_frame=True)
        frame_array = self.estmd.create_list_of_arrays()
        n = len(frame_array)
        for i in range(n):
            frame_array[i] = {'frame': frame_array[i].flatten()}

        self.cstmd.input = frame_array
        self.cstmd.spike_trains = cstmd.run()[1]

        # Adding simulation

        sim = Simulation("Test", True)

        sim.spike_trains = self.cstmd.spike_trains
        sim.start_positions = 0
        sim.pattern_duration = self.cstmd.duration
        sim.num_afferents = self.cstmd.spike_trains.shape[0]
        sim.duration = self.cstmd.spike_trains.shape[1]
        sim.sampling_interval = math.ceil(self.cstmd.duration / 5)

        n1 = sim.add_neuron(0.03125, .95, 300)
        n2 = sim.add_neuron(0.03125, 0.91, 125)
        n3 = sim.add_neuron(0.03125, 0.91, 125)
        n1.connect(n2)
        n1.connect(n3)
        n2.connect(n3)

        sim.run()

        # Adding ActionSelection

        pattern_input = []
        for neuron in sim.neurons:
            pattern_input.append(neuron.spike_times)

        a_s = ActionSelection(pattern_input=input,
                              pattern_duration=self.ani.total_frames,
                              animation=self.ani)
        a_s.run(show_plots=False)


if __name__ == '__main__':

    ani = Animation()
    ani.add_target(2, start=[300, 300])
    estmd = ESTMD()
    cstmd = Cstmd(2, 10, 30, 10, None)

    t = Training([1, 1, 1, 1], 1, ani, estmd, cstmd, False)
    t.run()
