# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:18:31 2013, Telluride, USA
@author: Zafeirios Fountas - Imperial College London (zfountas@imperial.ac.uk)

Notes:
 -   So the number of synapses helps the neuron with the weaker input 
     which however comes first.
"""

from scipy import stats
#import spike_trains
from Dragonfly import *

# "single_test" Run the simulation only one time with the parameters that are 
#               defined in this section
# "1"           
# "2"           SOS: Mode 2 is still under development..
EXPERIMENT = "single_test"

# -- PARAMETERS ---------------------------------------------------------------
neurons_no = 2
SYNAPSES_NO = 500   #1005        # Syn: 0 - 1100, K: 0.015 - 0.08

# Synapses
D = 30 # Maximum distance between compartments that are connected with a synapse
# -----------------------------------------------------------------------------

dr = Dragonfly(2)


# -----------------------------------------------------------------------------

if EXPERIMENT == "single_test":
    dr.run_experiment(synapses_no = SYNAPSES_NO, D=D, PLOTS = True)

elif EXPERIMENT == "1":
    spA = []
    spB = []
    spDiff = []
    axisSyn = []
    axisK = []
    
    fA = open("spA.txt", "w")
    fB = open("spB.txt", "w")
    fDiff = open("spDiff.txt", "w")
    
    #for current_synapses in range(0, 3000, 50):
    for current_synapses in range(0, 1000, 10):
        for k in np.arange(0.03,0.5,0.05) : # My limit: 0.0125 #He used: 0.072
            k=K
            axisK.append(k)
            axisSyn.append(current_synapses)
            a, b = run_experiment(synapses_no = current_synapses, Potassium=k, PLOTS = False, PRINTS=False)
            diff = abs(a-b)
            spA.append(a)
            spB.append(b)
            spDiff.append(diff)
        
            fA.write(str(str(k) + "," + str(current_synapses) + "," + str(a) + "\n"))
            fB.write(str(str(k) + "," + str(current_synapses) + "," + str(b) + "\n"))
            fDiff.write(str(str(k) + "," + str(current_synapses) + "," + str(diff) + "\n"))
      
    plt.figure(1)
    plt.plot(axisSyn, spA, c='b')
    plt.plot(axisSyn, spB, c='r')
    plt.plot(axisSyn, spDiff, c='g')
    plt.show()    

elif EXPERIMENT == "2": # SOS: Still under development!!
    # Run it for T1, then for T2 then for T3, record all the spikes of A,
    # and then check the difference |At1 - At1t2| and |At2 - At1t2|
    
    # Run for T1
    NetStim = 1
    T1_fr, temp = run_experiment(synapses_no = SYNAPSES_NO, Potassium = K, PLOTS = False, PRINTS=False)

    # Run for T2
    NetStim = 2
    T2_fr, temp = run_experiment(synapses_no = SYNAPSES_NO, Potassium = K, PLOTS = False, PRINTS=False)

    # Run for T1&T2
    NetStim = 3
    T12_fr, temp = run_experiment(synapses_no = SYNAPSES_NO, Potassium = K, PLOTS = False, PRINTS=False)
    """
    if len(T1_fr) != len(T2_fr) or len(T1_fr) != len(T12_fr) :
        sys.exit("ERROR: The sizes of the firing rates don't match!")
    if len(T1_fr) == 0 :
        sys.exit("ERROR: Size of firing rates is zero!")
    
    diff1 = 0.0
    for fr1, fr12 in zip(T1_fr, T12_fr) :
        diff1 = diff1 + float(abs(fr1-fr12))
    diff1 = diff1 / len(T1_fr)

    diff2 = 0.0
    for fr2, fr12 in zip(T2_fr, T12_fr) :
        diff2 = diff2 + float(abs(fr2-fr12))
    diff1 = diff1 / len(T2_fr)
        
    print "Results:   diff1:", diff1, "diff2:", diff2

    # I can also record the difference 1 and 2 accross time and plot it!
    
    
    spA = []
    spB = []
    spDiff = []
    axisSyn = []
    axisK = []
    
    
    axisK.append(k)
    axisSyn.append(current_synapses)
    a, b = run_experiment(synapses_no = current_synapses, Potassium=k, PLOTS = False, PRINTS=False)
    diff = abs(a-b)
    spA.append(a)
    spB.append(b)
    spDiff.append(diff)


    fA = open("spA.txt", "w")
    fB = open("spB.txt", "w")
    fDiff = open("spDiff.txt", "w")


    fA.write(str(str(k) + "," + str(current_synapses) + "," + str(a) + "\n"))
    fB.write(str(str(k) + "," + str(current_synapses) + "," + str(b) + "\n"))
    fDiff.write(str(str(k) + "," + str(current_synapses) + "," + str(diff) + "\n"))
      
    plt.figure(1)
    plt.plot(axisSyn, spA, c='b')
    plt.plot(axisSyn, spB, c='r')
    plt.plot(axisSyn, spDiff, c='g')
    plt.show()    
    """
    
#from neuron import gui # To start nrngui!



