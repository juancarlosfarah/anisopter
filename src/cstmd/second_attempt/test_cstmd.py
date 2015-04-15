"""
Unit tests for module CSTMD.
"""
from subprocess import call
import unittest
import pickle

from src.cstmd.second_attempt import CSTMD
import numpy as np
import os
import matplotlib


class TestCSTMD(unittest.TestCase):
    """
    This class represents sequence of tests for class CSTMD.
    """
    # Set up initial value for the CSTMD object    
    neurons_no = 2
    electrds=2
    SYNAPSES_NO=500
    D=30
    time_bet_frames=10

    # Initiate the CSTMD object
    dr = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D,electrds=electrds,PRINT =True)

    # Create an array of zeros
    frame_list = []
    for i in range(10) :
        frame_list.append(np.zeros([32,32]))

    # Run simulation for the empty arrray
    for frame in frame_list :
        frame = frame.ravel()
        times, ids = dr.run(time = time_bet_frames, rates = frame)


    def setUp(self):
        """
        Method that runs at start of each test.
        """
        self.perc_change_acceptable=50.0       
        self.Na = 0.48
        self.K = 0.05
        self.runtime=2000


    def real_firing_rates(self,data) :
        """
        Method that calculates the firing rate of the CSTMD neurons.
        """
        fr = []
        for i in range(len(data)-4) :
            fr.append(4000.0 / (data[i+4] - data[i]))
        return fr

    def test_compFireRate(self):
        """
        Method which compares the firing rate of the CSTMD with and without
        input.
        """
        
        # Runs the simulation with no input
        call(["python", "example.py", "-file", "64x64_no_input_200.pkl", "-K", str(self.K), "-Na", str(self.Na)])
        with open("data.pkl", 'rb') as my_file :
            data_no_input = pickle.load(my_file)

        # Runs the simulation with some input
        call(["python", "example.py", "-file", "64x64_strong_200.pkl", "-K", str(self.K), "-Na", str(self.Na)])
        with open("data.pkl", 'rb') as my_file :
            data_input = pickle.load(my_file)

        # Gets the firing rate for each of the 2 simulations
        real_fr_no_input = self.real_firing_rates(data_no_input)
        real_fr_input = self.real_firing_rates(data_input)
        

        # Gets the percentage change of the firing rate range while having an input
        without_input_rng=max(real_fr_no_input)-min(real_fr_no_input)        
        with_input_rng=max(real_fr_input)-min(real_fr_input)
        perc_change=100*(with_input_rng-without_input_rng)/without_input_rng

        # If the percentage change of the firing rate is greater than the 
        # predicted rate then the test succeeds
        self.failUnless(perc_change>=self.perc_change_acceptable)
 
    def test_save(self):
        """
        Method which checks whether the resulted spike trains are saved
        after a CSTMD simulation is run.
        """        
        # Save file
        self.dr.sp_trains_save()

        extension = ".npz"
        filename = "spike_trains/{}_{}_{}_{}_{}_{}".format(self.neurons_no,"neur",
                                                         self.electrds,"elecs",
                                                         self.time_bet_frames*len(self.frame_list),"runtime")

        # Checks whether a file of spike trains is created
        self.failUnless(os.path.exists(filename + extension))
    
    def test_plot(self):
        """
        Method which checks whether the expected plots are produced.
        """ 
        # Retrieve scatter plot
        fig = self.dr.plot(return_fig=True)

        # If the correct type of plot is return, then the test succeeds
        self.failUnless(type(fig) is matplotlib.collections.PathCollection)


if __name__ == '__main__':
    unittest.main()
