# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 13:05:29 2013, Telluride, USA
@author: Zafeirios Fountas - Imperial College London (zfountas@imperial.ac.uk)
@date: July 2013, Telluride, USA
"""

# Creates the matlab script which includes the parameters for the morphology of
# the neurons. The script will generate 2 neurons right next to each other
import create_morphology as morph
morph.create_matlab_code(2, 0)

# Calls matlab toolbox 'trees' to create the swc/hoc files that include the 
# neurons
import os
os.system("octave py_tree_script.m")
os.system("mv ../trees/neuron0.hoc ../neuron0.hoc" )
os.system("mv ../trees/neuron0.swc ../neuron0.swc" )
os.system("mv ../trees/neuron1.hoc ../neuron1.hoc" )
os.system("mv ../trees/neuron1.swc ../neuron1.swc" )

# Simulate the outcome of the above with 'neuron simulator'
import simulate_in_neuron


