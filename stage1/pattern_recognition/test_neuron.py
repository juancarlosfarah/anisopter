__author__ = 'juancarlosfarah'

import math
import unittest

import neuron
import numpy as np
import matplotlib.pyplot as plt
import pylab


class NeuronTests(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        self.num_afferents = 10
        self.neuron = neuron.Neuron(self.num_afferents)
        self.tolerance = 0.000001
        return

    def test_time_delta(self):
        """
        Checks that neuron.calculate_time_delta 
        returns the correct output
        :return:
        """
        spike_train = np.array([1,0,1,1,0,1,0,0,0])
        time_delta = self.neuron.calculate_time_delta(spike_train)
        self.failUnless(time_delta==-3)
        return

    def test_ltp(self):
        """
        Checks that neuron.calculate_ltp returns the correct output
        :return:
        """
        ltp = self.neuron.calculate_ltp(-3)
        tolerance = math.fabs(ltp-0.0261395096029)
        self.failIf(tolerance>self.tolerance)
        return

    def test_ltd(self):
        """
        Checks that neuron.calculate_ltd returns the correct output
        :return:
        """
        ltd = self.neuron.calculate_ltd(3)
        tolerance = math.fabs(ltd+0.0263012639175)
        self.failIf(tolerance>self.tolerance)
        return

    def test_heavy_side(self):
        """
        Checks that neuron.calculate_heavy_side_step returns the correct output
        :return:
        """
        pos_val = 1
        neg_val = -1
        pos_result = self.neuron.calculate_heavyside_step(pos_val)
        self.failIf(pos_result != 1)
        neg_result = self.neuron.calculate_heavyside_step(neg_val)
        self.failIf(neg_result != 0)
        return

    def test_update_weights_time_delta_None(self):
        """
        Checks that neuron.update_weights returns the correct output
        """        
        spike_train = np.array([1,0,1,1,0,1,0,0,0])
        ms = 1
        test_failed = False
        
        self.neuron.time_delta = None
        
        self.neuron.current_weights = [[ 0.49599198],
                                        [ 0.46974692],
                                        [ 0.44050216],
                                        [ 0.59499429],
                                        [ 0.38400322],
                                        [ 0.59385204],
                                        [ 0.35422254],
                                        [ 0.60763721],
                                        [ 0.44616867],
                                        [ 0.47623609]]
                                        
        correct_updated_weights = [ [ 0.49599198],
                                    [ 0.46974692],
                                    [ 0.44050216],
                                    [ 0.59499429],
                                    [ 0.38400322],
                                    [ 0.59385204],
                                    [ 0.35422254],
                                    [ 0.60763721],
                                    [ 0.44616867],
                                    [ 0.47623609]]
        
        updated_weights = self.neuron.update_weights(spike_train, ms)
                            
        for i in range(len(correct_updated_weights)):
            if(updated_weights[i] != correct_updated_weights[i]):
                test_failed=True
                break

        self.failIf(test_failed)
        return
        
        
    def test_update_epsps(self):
        """
        Checks that neuron.update_epsps returns the correct result
        """
        test_failed = False
        
        spike_train = np.array([1,0,1,1,0,1,0,0,0])
        
        self.neuron.time_delta = 1
        
        self.neuron.current_weights = [[ 0.49599198],
                                        [ 0.46974692],
                                        [ 0.44050216],
                                        [ 0.59499429],
                                        [ 0.38400322],
                                        [ 0.59385204],
                                        [ 0.35422254],
                                        [ 0.60763721],
                                        [ 0.44616867],
                                        [ 0.47623609]]
        
        self.neuron.epsps =[[ 0],
                            [ 1],
                            [ 2],
                            [ 3],
                            [ 4],
                            [ 4],
                            [ 3],
                            [ 2],
                            [ 1],
                            [ 0]]
                            
        correct_updated_epsps_sums = [ 20.,           
                                        4.86335512,   
                                        0.,
                                        4.86335512,   
                                        4.86335512,   
                                        0.,
                                        4.86335512,   
                                        0.,           
                                        0.,           
                                        0.,]
                                       
        updated_epsps_sums = sum(self.neuron.update_epsps(spike_train))
        
        for i in range(len(updated_epsps_sums)):
            if abs(correct_updated_epsps_sums[i] - updated_epsps_sums[i]) > self.tolerance:
                test_failed = True
                break
                
        self.failIf(test_failed)
        return
        
        
    def test_sum_epsps(self):
        """
        Checks that neuron.sum_epsps returns the correct result
        """        
        correct_sum = 0
        
        calculated_sum = self.neuron.sum_epsps()
        
        self.failIf(abs(correct_sum-calculated_sum)>self.tolerance)
        return
    
    def test_sum_ipsps(self):
        """
        Checks that neuron.sum_ipsps returns the correct result
        """        
        ms = 10
        test_failed = False
        
        #ipsps size = 0
        if(self.neuron.sum_ipsps(ms) != 0):
            test_failed = True
            
        #ipsps size > 0
        self.neuron.ipsps = np.array([1,1])
        correct_sum = -201.214800862
        if(abs(self.neuron.sum_ipsps(ms) - correct_sum) > self.tolerance):
            test_failed = True

        self.failIf(test_failed)
        return
        
        
    def test_calculate_psp(self):
        """
        Checks that neuron.calculate_psp returns the correct result.
        """    
        correct_psp = 1000.0
        calculated_psp = self.neuron.calculate_psp(time_delta=0, debugging=True)
        self.failIf(abs(correct_psp - calculated_psp)>self.tolerance)
        return
        
        
    def test_calculate_membrane_potential(self):
        """
        Checks that neuron.calculate_membrane_potential 
        returns the correct result.
        """    
        ms = 10
        self.neuron.ipsps = np.array([1,1])
        correct_membrane_potential = -201.214800862
        calculated_membrane_potential = self.neuron.calculate_membrane_potential(ms)
        
        self.failIf(abs(correct_membrane_potential-calculated_membrane_potential)>self.tolerance)
        return
        
    def test_calculate_mu(self):
        """
        Checks that neuron.calculate_mu returns the correct result.
        """    
        test_failed = False
        
        # Case delta = 0
        delta = 0
        if(self.neuron.calculate_mu(delta) != 0):
            test_failed = True
        
        # Case delta != 0
        delta = 1
        correct_mu = -62.2134104356
        calculated_mu = self.neuron.calculate_mu(delta)
        if(abs(correct_mu - calculated_mu)>self.tolerance):
            test_failed = True
            
        self.failIf(test_failed)
        return
        
    def test_plot_ltp(self):
        fig =  self.neuron.plot_ltp(show=False, return_fig=True)
        self.failUnless(type(fig) is list)
        return
        
    def test_plot_ltd(self):      
        fig =  self.neuron.plot_ltd(show=False, return_fig=True)
        self.failUnless(type(fig) is list)
        return        
        
    def tearDown(self):
        """

        :return:
        """
        return


def main():
    unittest.main()

if __name__ == '__main__':
    main()
