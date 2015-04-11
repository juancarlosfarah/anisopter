# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:18:31 2013, Telluride, USA
@author: Zafeirios Fountas - Imperial College London (zfountas@imperial.ac.uk)

Notes:
 -   So the number of synapses helps the neuron with the weaker input 
     which however comes first.
"""

import neuron
from neuron import h
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
import math
import random
#import spike_trains

# -- PARAMETERS ---------------------------------------------------------------

neurons_no = 2
SYNAPSES_NO = 500   #1005        # Syn: 0 - 1100, K: 0.015 - 0.08
electrodes = 4 # How many points of the neuron should been recorded (when SINGLE_TEST==1) - The electrodes are equally distributed accross the compartments of a neuron
SINGLE_TEST = 1 # Run the simulation only one time with the parameters that are defined in this section
EXPERIMENT = 3 # SOS: Mode 2 is still under development..

#SEEDS
stim_seed = 400
synapses_seed = 20

t_stop = 500
v_init = -60

dt = 0.25       # default 0.025
h.celsius = 20  # Temperature of the cells

# Stimulation
IC = 0
NetStim = 1   # 1: T1, 2: T2, 3: T1&T2, 0: No stimulation
SpTrain = 0

delay_of_T1 = 13 # [ms]
delay_of_T2 = 50 # [ms]
stim_start = 50 # [ms]
stim_duration = 1500 # [ms]
stim_amp = 1.6 # [nA] amplitude
stim_numb = 20
stim_noise = 0
spike_train_pick = 100

# HH parameters - (Na is Sodium, K is Potassium)
# SOS: For Na = 0.48, K below 0.0125 is not bistable, above something as well
K = 0.06 #My limit: 0.0125 # Klauss used: 0.072
Na = 0.48
                # SOS: We should leave Sodium constant and vary the Potassium
                # The thick dendrites should be arround 5 microMeters
                # the thin ones arround 1.5...

# Synapses
D = 30# Maximum distance between compartments that are connected with a synapse
max_synapses = 10000# maximum limit of synapses in case where we are very close
weights = 0.01
thresholds = 0.0
delays = 1.0

# -----------------------------------------------------------------------------

# -- THINGS THAT RUN ONLY ONCE ------------------------------------------------
# Calculate the number of compartments of each neuron
NSize = []
for n in range(neurons_no) :
    h.load_file(1, "../neuron"+str(n)+".hoc")
    # count the number of sections:
    NSize.append(0)
    for sec in h.allsec():
        NSize[n] = NSize[n] + 1
    print "This neuron has ", NSize[n], " compartments!"
    h('forall delete_section()')

# Load all neurons!
for n in range(neurons_no) :
    h.load_file(1, "../neuron"+str(n)+".hoc")
# This is calculated only to confirm the previous
nAll = 0
for sec in h.allsec():
    nAll = nAll + 1
print "All neurons have ", nAll, " compartments!"

# Take the coordinates of the middle of all the compartments:
cell_list = []
Coordinates = []
for n in range(neurons_no) :
    cell = []
    print "Neuron ", n
    for i in range(NSize[n]):
        exec "cell.append(h.neuron"+str(n)+"_tree["+str(i)+"])";
        cell[i].push()
        middle = int(h.n3d()/2)# It has to be integer!!
        Coordinates.append((h.x3d(middle),h.y3d(middle),h.z3d(middle)))
        #print "Yo(", i, ") Middle is ", middle, Coordinates[i]
        h.pop_section()
    cell_list.append(cell)
    
# Generate the spike trains!
#if SpTrain :
#    input_spikes = spike_trains.make_input(angle=50,pick=spike_train_pick,duration=stim_duration)
#    fInput = open("spInput.txt", "w")
#    for input_spike in input_spikes :
#        fInput.write(str(str(input_spike) + "\n"))

# -----------------------------------------------------------------------------

def run_experiment(synapses_no = 1000, Potassium = K, PLOTS = 0, EXP2 = 0) :
    # Find all the compartments of neuron B that are closer than D to to each
    # compartment of neuron A
    ss = []
    ssSize = 0
    nc = []
    ncSize = 0
    for n in range(neurons_no-1): # So we need at least two neurons for it to work!
        if SINGLE_TEST :
            print "Searching for synapses for neurons ", n, " and ", n+1
        synapses = 0
        syn = []
        for a in range(NSize[n]) :
            minimum = sys.float_info.max
            (x1,y1,z1) = Coordinates[a]
            for b in range(NSize[n],NSize[n]+NSize[n+1]) :
                (x2,y2,z2) = Coordinates[b]
                dist = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
                if synapses < max_synapses :
                    if D > dist :
                        synapses = synapses + 1
                        syn.append((a,b-NSize[n]))
                else :
                    print "WORNING: We reached the maximum number of synapses"
        if SINGLE_TEST :
            print "Synapses found: ", synapses
        if synapses < synapses_no or len(syn) < synapses_no :
            sys.exit("ERROR: There are not enough intersections to create synapses. Change parameter D and run again!!")
        random.seed(synapses_seed)
        # Reduce the amount of synapses
        while len(syn) > synapses_no :
            random_synapse = int(random.uniform(0,len(syn)-1))
            syn.pop(random_synapse)
        print "Synapses used: ", len(syn)
            
        # ------------------------------------------------------------------- #
        if SINGLE_TEST : # In a single test we want to see more output..
            print "Generating synapses..."
        for pre, post in syn :
            if random.random() < 0.5 :
                #print "0 -> 1" # to prove that synapses are generated in both directions
                ssSize = ssSize + 1
                exec "ss.append(h.Exp2Syn(h.neuron"+str(n+1)+"_tree[post](0.5)))"
                #ss.tau1 --- ms rise time
                #ss.tau2 --- ms decay time
                #ss.e -- mV reversal potential
                #ss.i -- nA synaptic current
                ss[ssSize-1].e = -75; # [mV]
                ncSize = ncSize + 1
                exec "nc.append(h.NetCon(h.neuron"+str(n)+"_tree[pre](0.5)._ref_v, ss[ssSize-1], thresholds, delays, weights, sec=h.neuron"+str(n)+"_tree[pre]))"
            else :
                #print "1 -> 0" # to prove that synapses are generated in both directions
                ssSize = ssSize + 1
                exec "ss.append(h.Exp2Syn(h.neuron"+str(n)+"_tree[pre](0.5)))"
                ss[ssSize-1].e = -75; # [mV]
                ncSize = ncSize + 1
                exec "nc.append(h.NetCon(h.neuron"+str(n+1)+"_tree[post](0.5)._ref_v, ss[ssSize-1], thresholds, delays, weights, sec=h.neuron"+str(n+1)+"_tree[post]))"
        if SINGLE_TEST :
            print "OK!"
    
    if SINGLE_TEST :
        print "Generating parameters..."
    h('forall {uninsert pas}')
    h('forall {insert hh}')
    for sec in h.allsec() :
        sec.gnabar_hh =  Na
        sec.gkbar_hh =  Potassium
    
    #Stimulation
    if IC :
        stimIC = h.IClamp(h.neuron0_tree[720](0.5))
        stimIC.delay = stim_start   # [ms]
        stimIC.dur = stim_duration  # [ms]
        stimIC.amp = stim_amp       # [nA] amplitude
        syn0ic = h.Exp2Syn(h.neuron0_tree[3](0.5)) # 720
        nc0ic = h.NetCon(stimIC,syn0ic,0,0.025+delay_of_T1,0.05) # threshold, delay, weight
        syn1ic = h.Exp2Syn(h.neuron1_tree[3](0.5)) # 720
        nc1ic = h.NetCon(stimIC,syn1ic,0,0.025,0.01) # threshold, delay, weight
    elif NetStim:
        # Experiment 2
        if NetStim == 1:
            w1_n0 = 0.05
            w1_n1 = 0.01
            w2_n0 = 0.0
            w2_n1 = 0.0
        elif NetStim == 2: 
            w1_n0 = 0.0
            w1_n1 = 0.0
            w2_n0 = 0.01
            w2_n1 = 0.05
        elif  NetStim == 3 :
            w1_n0 = 0.05
            w1_n1 = 0.01
            w2_n0 = 0.01
            w2_n1 = 0.05

        # First stimulus
        stimNet1 = h.NetStim()
        stimNet1.start = stim_start  # like delay
        stimNet1.number = stim_numb  # Number of spikes
        stimNet1.noise = stim_noise  # 0
        stimNet1.seed(stim_seed)
        syn0net1 = h.Exp2Syn(h.neuron0_tree[3](0.5))
        nc0net1  = h.NetCon(stimNet1,syn0net1,0,0.025+delay_of_T1,w1_n0) # threshold, delay, weight
        syn1net1 = h.Exp2Syn(h.neuron1_tree[3](0.5))
        nc1net1  = h.NetCon(stimNet1,syn1net1,0,0.025,w1_n1) # threshold, delay, weight
        # Second stimulus
        stimNet2 = h.NetStim()
        stimNet2.start = stim_start  # like delay
        stimNet2.number = stim_numb  # Number of spikes
        stimNet2.noise = stim_noise  # 0
        stimNet2.seed(stim_seed+10)
        syn0net2 = h.Exp2Syn(h.neuron0_tree[3](0.5))
        nc0net2  = h.NetCon(stimNet2,syn0net2,0,0.025,w2_n0)
        syn1net2 = h.Exp2Syn(h.neuron1_tree[3](0.5))
        nc1net2  = h.NetCon(stimNet2,syn1net2,0,0.025+delay_of_T2,w2_n1)
    elif SpTrain:
        stimNet = h.NetStim()
        stimNet.start = 0
        stimNet.number = 0
        stimNet.noise = 0
        syn0net = h.Exp2Syn(h.neuron0_tree[2](0.5))
        nc0net  = h.NetCon(stimNet,syn0net,0,0.025,0.0045)
        syn1net = h.Exp2Syn(h.neuron1_tree[2](0.5))
        nc1net  = h.NetCon(stimNet,syn1net,0,0.025,0.0015)
        
        
    # Spiking recording
    tvec0 = h.Vector() #time
    idvec0 = h.Vector() #cell number
    raster0 = h.NetCon(h.neuron0_tree[1](.5)._ref_v, None, sec=h.neuron0_tree[1]) #(.5)
    raster0.threshold = 0 #-10 #set threshold to a value of your choice
    raster0.record(tvec0, idvec0, 0)
    
    tvec1 = h.Vector() #time
    idvec1 = h.Vector() #cell number
    raster1 = h.NetCon(h.neuron1_tree[1](.5)._ref_v, None, sec=h.neuron1_tree[1])
    raster1.threshold = 0
    raster1.record(tvec1, idvec1, 1)
    
    if SINGLE_TEST :
        print "OK!"

    # RUN THE SIMULATION:
    #def run_experiment():
    #define the compartments whose activity will be recorded
    rec0_size = int(NSize[0] / electrodes)
    rec1_size = int(NSize[1] / electrodes)
    rec0 = []
    rec1 = []
    for i in range(electrodes) :
        rec0.append(rec0_size*i)
        rec1.append(rec1_size*i)

    # Initialize the electrodes
    if PLOTS: 
        for e in range(electrodes) :
            exec "vrec0"+str(e)+" = h.Vector()"
            exec "trec0"+str(e)+" = h.Vector()"
            exec "vrec1"+str(e)+" = h.Vector()"
            exec "trec1"+str(e)+" = h.Vector()"
            exec "vrec0"+str(e)+".record(h.neuron0_tree["+str(rec0[e])+"](0.5)._ref_v)"
            exec "trec0"+str(e)+".record(h._ref_t)"
            exec "vrec1"+str(e)+".record(h.neuron1_tree["+str(rec1[e])+"](0.5)._ref_v)"
            exec "trec1"+str(e)+".record(h._ref_t)"

    # Finalize initialization
    h.finitialize(-60)
    h.dt = dt

    # Set the spike trains
    if SpTrain :
        for input_spike in input_spikes :
            nc0net.event(input_spike + delay_of_T1)
            nc1net.event(input_spike)

    # Run the simulation
    neuron.run(t_stop)
    
    print "Result: (neuron0, neuron1) =      ", len(tvec0), ",   ", len(tvec1)

    # Plot the recordings    
    if PLOTS :
        plt.figure(1)
        for e in range(electrodes) :
            exec "t0"+str(e)+" = np.array(trec0"+str(e)+")"
            exec "v0"+str(e)+" = np.array(vrec0"+str(e)+")"
            exec "t1"+str(e)+" = np.array(trec1"+str(e)+")"
            exec "v1"+str(e)+" = np.array(vrec1"+str(e)+")"
        for e in range(electrodes) :
            exec "plt.subplot(2,"+str(electrodes+1)+","+str(e+1)+")"
            exec "plt.plot(t0"+str(e)+",v0"+str(e)+",label='Section "+str(rec0[e])+"', c='b')"
            exec "plt.legend(loc=0)"
            exec "plt.subplot(2,"+str(electrodes+1)+","+str(electrodes+e+2)+")"
            exec "plt.plot(t1"+str(e)+",v1"+str(e)+",label='Section "+str(rec1[e])+"', c='r')"
            exec "plt.legend(loc=0)"
        exec "plt.subplot(2,"+str(electrodes+1)+","+str(electrodes+1)+")"
        # to change the size of the plot use: mp.figure(1, figsize=(20,20))
        # You can change the color and marker according to the pylab documentation
        a = plt.gca()
        a.set_xlim([0,t_stop])
        idvec1temp = [x*(-1.0) for x in idvec1]
        plt.scatter(tvec0, idvec0, c='b', marker='+')
        plt.scatter(tvec1, idvec1temp, c='r', marker='+')
        if SpTrain :
            tt = []
            for i in range(len(input_spikes)):
                tt.append(1.0)
            plt.scatter(input_spikes, tt, c='g')

        # FIRING RATE
        exec "plt.subplot(2,"+str(electrodes+1)+","+str(2*electrodes+2)+")"
        a = plt.gca()
        a.set_xlim([0,t_stop])
    # The following part is also used in experiment 2 where we need to calculate
    # and then compare the firing rate of the first neuron
    if PLOTS or EXP2:
        for neu in range(2) :
            spikes = [0.0]
            my_length = 0
            exec "my_length = len(tvec"+str(neu)+")"
            for s in range(my_length) :
                exec "spikes.append(tvec"+str(neu)+"[s])"
            
            fr = []
            s = 0
            for i in range(len(spikes)-1) :
                t0 = spikes[i]
                t1 = spikes[i+1]
                s = t1 - t0
                if s == 0 :
                    sys.exit("ERROR: Division by zero!")
                else :
                    fr.append(1000.0/s)
            if s == 0 :
                fr.append(0.0)
            else :
                fr.append(1000.0/s)
            if EXP2 :
                print fr
                return fr, []
            if neu == 0:
                plt.plot(spikes, fr, c='b')
            elif neu == 1:
                plt.plot(spikes, fr, c='r')
        """ # Firing rate of input stimulus (SOS: doesn't work very well)
        if SpTrain and len(input_spikes) > 0:
            spikes = [0.0]
            for sp in input_spikes :
                spikes.append(sp)
            
            fr = []
            s = 0
            for i in range(len(spikes)-1) :
                t0 = spikes[i]
                t1 = spikes[i+1]
                s = t1 - t0
                if s == 0 :
                    #sys.exit("ERROR: Division by zero!"+str(t0)+"-"+str(t1))
                    print "ERROR: Division by zero!"+str(t0)+"-"+str(t1)
                    fr.append(0.0)
                else :
                    fr.append(1000.0/s)
            if s == 0 :
                fr.append(0.0)
            else :
                fr.append(1000.0/s)
            plt.plot(spikes, fr, c='g')
        """
        #plt.savefig('screenshots/raster_plot.png') #this will save the plot - comment out if this is not needed
        #plt.draw() 
        plt.show() #this allows you to view the plot - comment out if this not needed

    if EXP2 == 0 :
        return len(tvec0), len(tvec1)
    else :
        sys.exit("ERROR: It shouldn't reach this point!")

if SINGLE_TEST:
    run_experiment(synapses_no = SYNAPSES_NO, PLOTS = 1)
elif EXPERIMENT == 1:
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
            a, b = run_experiment(synapses_no = current_synapses, Potassium=k, PLOTS = 0)
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

elif EXPERIMENT == 2: # SOS: Still under development!!
    # Run it for T1, then for T2 then for T3, record all the spikes of A,
    # and then check the difference |At1 - At1t2| and |At2 - At1t2|
    
    # Run for T1
    NetStim = 1
    T1_fr, temp = run_experiment(synapses_no = SYNAPSES_NO, Potassium = K, PLOTS = 0)

    # Run for T2
    NetStim = 2
    T2_fr, temp = run_experiment(synapses_no = SYNAPSES_NO, Potassium = K, PLOTS = 0)

    # Run for T1&T2
    NetStim = 3
    T12_fr, temp = run_experiment(synapses_no = SYNAPSES_NO, Potassium = K, PLOTS = 0)
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
    a, b = run_experiment(synapses_no = current_synapses, Potassium=k, PLOTS = 0)
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



