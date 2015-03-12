"""
Unit tests for module CSTMD.
"""
from CSTMD import CSTMD
from subprocess import call
import unittest
import numpy as np
import pickle

class TestCSTMD(unittest.TestCase):
    """
    This class represents sequence of tests for class CSTMD.
    """
    perc_change_acceptable=50.0

    def setUp(self):
        """
        Method that runs at start of each test.
        """
        neurons_no = 2
        SYNAPSES_NO = 500
        D = 30
        electrds = 50
        self.cstmd = CSTMD(neurons_no=neurons_no, synapses_no=SYNAPSES_NO, D=D,electrds=electrds)

    def real_firing_rates(self,data) :
        """
        Method that calculates the firing rate of the CSTMD neurons.
        """
        fr = []
        for i in range(len(data)-4) :
            fr.append(4000.0 / (data[i+4] - data[i]))
        return fr

    def compFireRate(self):
        """
        Method which compares the firing rate of the CSTMD with and without
        input.
        """
        Na = 0.48
        K = 0.05
        
        # Runs the simulation with no input
        call(["python", "example.py", "-file", "64x64_no_input_200.pkl", "-K", str(K), "-Na", str(Na)])
        with open("data.pkl", 'rb') as my_file :
            data_no_input = pickle.load(my_file)

        # Runs the simulation with some input
        call(["python", "example.py", "-file", "64x64_strong_200.pkl", "-K", str(K), "-Na", str(Na)])
        with open("data.pkl", 'rb') as my_file :
            data_input = pickle.load(my_file)

        # Gets the firing rate for each of the 2 simulations
        real_fr_no_input = self.real_firing_rates(data_no_input)
        real_fr_input = self.real_firing_rates(data_input)
        

        # Gets the percentage change of the firing rate range while having an input
        without_input_rng=max(real_fr_no_input)-min(real_fr_no_input)        
        with_input_rng=max(real_fr_input)-min(real_fr_input)
        perc_change=100*(with_input_rng-without_input_rng)/without_input_rng

        return perc_change

    def test_run(self):
        # If the percentage change of the firing rate is greater than the 
        # predicted rate then the test succeeds
        self.assertTrue(self.compFireRate()>=self.perc_change_acceptable)

if __name__ == '__main__':
    unittest.main()
