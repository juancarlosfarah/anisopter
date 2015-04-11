# -*- coding: utf-8 -*-
# http://www.neuron.yale.edu/neuron/static/new_doc/programming/neuronpython.html

import neuron
from neuron import h
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import math
import sys

class Dragonfly(object) :

    # -- PARAMETERS ------------------------------------------------------------
    electrodes = 4      # How many points of the neuron should been recorded 
                        # (when SINGLE_TEST==True) - The electrodes are equally 
                        # distributed accross the compartments of a neuron

    t_stop = 500
    v_init = -60

    dt = 0.25       # default 0.025
    h.celsius = 20  # Temperature of the cells

    # SEEDS
    stim_seed = 400 
    synapses_seed = 20

    # Synapses
    weights = 0.01
    thresholds = 0.0
    delays = 1.0
    max_synapses = 10000 # maximum limit of synapses in case where we are very close

    # Stimulation
    IC = 1
    NetStim = 0   # 1: T1, 2: T2, 3: T1&T2, 0: No stimulation
    SpTrain = False
    
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
    # --------------------------------------------------------------------------

	# IK: constructor
    def __init__(self, neurons_no, PRINT = True) :
        if PRINT == True :
            print "------------------------------------------------------ "
            print "     *    Dragonfly CSTMD1 neuron simulation    *      "
            print "     *                                          *      "
            print "     *      author: Zafeirios Fountas           *      "
            print "------------------------------------------------------ "
        
        self.global_time = time.time()
        self.PRINTS = PRINT
        self.neurons_no = neurons_no

        # THINGS THAT RUN ONLY ONCE 
    
        # Calculate the number of compartments of each neuron
        self.calc_compartments()
        
        # Load all neurons!
        self.load_neurons()
        
        # Take the coordinates of the middle of all the compartments:
        self.find_middle_coordinates()
            
        # Generate the spike trains!
        #if SpTrain :
        #    input_spikes = spike_trains.make_input(angle=50,pick=spike_train_pick,duration=stim_duration)
        #    fInput = open("spInput.txt", "w")
        #    for input_spike in input_spikes :
        #        fInput.write(str(str(input_spike) + "\n"))



    # Calculate the number of compartments of each neuron
    def calc_compartments(self) :
        self.NSize = []
        for n in range(self.neurons_no) :
            h.load_file(1, "../RESULTED_NEURONS/neuron"+str(n)+".hoc")
            # count the number of sections:
            self.NSize.append(0)
            for sec in h.allsec():
                self.NSize[n] = self.NSize[n] + 1
            print "This neuron has ", self.NSize[n], " compartments!"
            h('forall delete_section()')
    
    # Load all neurons!
    def load_neurons(self) :
        for n in range(self.neurons_no) :
            h.load_file(1, "../RESULTED_NEURONS/neuron"+str(n)+".hoc")
        # This is calculated only to confirm the previous
        nAll = 0
        for sec in h.allsec():
            nAll = nAll + 1
        print "All neurons have ", nAll, " compartments!"
    
    
    # Take the coordinates of the middle of all the compartments:
    def find_middle_coordinates(self) :
        cell_list = []
        self.m_coordinates = []
        for n in range(self.neurons_no) :
            cell = []
            print "Neuron ", n
            for i in range(self.NSize[n]):
                exec "cell.append(h.neuron"+str(n)+"_tree["+str(i)+"])";
                cell[i].push()
                middle = int(h.n3d()/2)# It has to be integer!!
                self.m_coordinates.append((h.x3d(middle),h.y3d(middle),h.z3d(middle)))
                #print "Yo(", i, ") Middle is ", middle, Coordinates[i]
                h.pop_section()
            cell_list.append(cell)
        self.m_coordinates
    



    def run_experiment(self, synapses_no, D, Potassium=-1, PLOTS = False, EXP2 = 0) :
        if Potassium == -1 :
            Potassium = self.K

        # Find all the compartments of neuron n+1 that are closer than D to to each
        # compartment of neuron n (intersection points) and could accomodate 
        # possible synapses and then  create 'synapses_no' synapses..!
        ss = []
        ssSize = 0
        nc = []
        ncSize = 0
        for n in range(self.neurons_no-1): # Note: So we need at least two neurons for it to work!
    
            # -- Find intersection points ------------------------------------------
            if self.PRINTS :
                print "Searching for synapses for neurons ", n, " and ", n+1
            synapses = 0
            syn = []
            for a in range(self.NSize[n]) :
                minimum = sys.float_info.max
                (x1,y1,z1) = self.m_coordinates[a]
                for b in range(self.NSize[n],self.NSize[n]+self.NSize[n+1]) :
                    (x2,y2,z2) = self.m_coordinates[b]
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
                    if synapses < self.max_synapses :
                        if D > dist :
                            synapses = synapses + 1
                            syn.append((a,b-self.NSize[n]))
                    else :
                        print "WORNING: We reached the maximum number of synapses"
            if self.PRINTS :
                print "Synapses found: ", synapses
    
            # -- Reduce intersection points to number of synapses ------------------
            if synapses < synapses_no or len(syn) < synapses_no :
                sys.exit("ERROR: There are not enough intersections to create "+\
                         "synapses. Change parameter D and run again!!")
            random.seed(self.synapses_seed)
            # Reduce the amount of synapses
            while len(syn) > synapses_no :
                random_synapse = int(random.uniform(0,len(syn)-1))
                syn.pop(random_synapse)
            print "Synapses used: ", len(syn)
                
            # ------------------------------------------------------------------- #
            if self.PRINTS :
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
                    exec "nc.append(h.NetCon(h.neuron"+str(n)+"_tree[pre](0.5)._ref_v, ss[ssSize-1], self.thresholds, self.delays, self.weights, sec=h.neuron"+str(n)+"_tree[pre]))"
                else :
                    #print "1 -> 0" # to prove that synapses are generated in both directions
                    ssSize = ssSize + 1
                    exec "ss.append(h.Exp2Syn(h.neuron"+str(n)+"_tree[pre](0.5)))"
                    ss[ssSize-1].e = -75; # [mV]
                    ncSize = ncSize + 1
                    exec "nc.append(h.NetCon(h.neuron"+str(n+1)+"_tree[post](0.5)._ref_v, ss[ssSize-1], self.thresholds, self.delays, self.weights, sec=h.neuron"+str(n+1)+"_tree[post]))"
            if self.PRINTS :
                print "OK!"
        
        if self.PRINTS :
            print "Generating parameters..."
        h('forall {uninsert pas}')
        h('forall {insert hh}')
        for sec in h.allsec() :
            sec.gnabar_hh =  self.Na
            sec.gkbar_hh =  Potassium
        
        #Stimulation

        if self.IC :
            stimIC = h.IClamp(h.neuron0_tree[720](0.5))
            stimIC.delay = self.stim_start   # [ms]
            stimIC.dur = self.stim_duration  # [ms]
            stimIC.amp = self.stim_amp       # [nA] amplitude
            syn0ic = h.Exp2Syn(h.neuron0_tree[3](0.5)) # 720
            nc0ic = h.NetCon(stimIC,syn0ic,0,0.025+self.delay_of_T1,0.05) # threshold, delay, weight
            syn1ic = h.Exp2Syn(h.neuron1_tree[3](0.5)) # 720
            nc1ic = h.NetCon(stimIC,syn1ic,0,0.025,0.01) # threshold, delay, weight
        elif self.NetStim:
            # Experiment 2
            if self.NetStim == 1:
                w1_n0 = 0.05
                w1_n1 = 0.01
                w2_n0 = 0.0
                w2_n1 = 0.0
            elif self.NetStim == 2: 
                w1_n0 = 0.0
                w1_n1 = 0.0
                w2_n0 = 0.01
                w2_n1 = 0.05
            elif  self.NetStim == 3 :
                w1_n0 = 0.05
                w1_n1 = 0.01
                w2_n0 = 0.01
                w2_n1 = 0.05
    
            # First stimulus
            stimNet1 = h.NetStim()
            stimNet1.start = self.stim_start  # like delay
            stimNet1.number = self.stim_numb  # Number of spikes
            stimNet1.noise = self.stim_noise  # 0
            stimNet1.seed(self.stim_seed)
            syn0net1 = h.Exp2Syn(h.neuron0_tree[3](0.5))
            nc0net1  = h.NetCon(stimNet1,syn0net1,0,0.025+self.delay_of_T1,w1_n0) # threshold, delay, weight
            syn1net1 = h.Exp2Syn(h.neuron1_tree[3](0.5))
            nc1net1  = h.NetCon(stimNet1,syn1net1,0,0.025,w1_n1) # threshold, delay, weight
            # Second stimulus
            stimNet2 = h.NetStim()
            stimNet2.start = self.stim_start  # like delay
            stimNet2.number = self.stim_numb  # Number of spikes
            stimNet2.noise = self.stim_noise  # 0
            stimNet2.seed(self.stim_seed+10)
            syn0net2 = h.Exp2Syn(h.neuron0_tree[3](0.5))
            nc0net2  = h.NetCon(stimNet2,syn0net2,0,0.025,w2_n0)
            syn1net2 = h.Exp2Syn(h.neuron1_tree[3](0.5))
            nc1net2  = h.NetCon(stimNet2,syn1net2,0,0.025+self.delay_of_T2,w2_n1)
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
        
        if self.PRINTS :
            print "OK!"
    
        # RUN THE SIMULATION:
        #def run_experiment():
        #define the compartments whose activity will be recorded
        rec0_size = int(self.NSize[0] / self.electrodes)
        rec1_size = int(self.NSize[1] / self.electrodes)
        rec0 = []
        rec1 = []
        for i in range(self.electrodes) :
            rec0.append(rec0_size*i)
            rec1.append(rec1_size*i)
    
        # Initialize the electrodes
        if PLOTS: 
            for e in range(self.electrodes) :
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
        h.dt = self.dt
    
        # Set the spike trains
        if self.SpTrain :
            for input_spike in input_spikes :
                nc0net.event(input_spike + self.delay_of_T1)
                nc1net.event(input_spike)

        step = self.t_stop/2
        print "sim starting running!"
        start_time = time.time()
        # Run the simulation
        neuron.run(step)
        print "Time:", time.time() - start_time

        start_time = time.time()
        # Run the simulation
        neuron.run(step+step)
        print "Time:", time.time() - start_time
        
        print "Result: (neuron0, neuron1) =      ", len(tvec0),",   ",len(tvec1)
    
        # Plot the recordings    
        if PLOTS :
            plt.figure(1)
            for e in range(self.electrodes) :
                exec "t0"+str(e)+" = np.array(trec0"+str(e)+")"
                exec "v0"+str(e)+" = np.array(vrec0"+str(e)+")"
                exec "t1"+str(e)+" = np.array(trec1"+str(e)+")"
                exec "v1"+str(e)+" = np.array(vrec1"+str(e)+")"
            for e in range(self.electrodes) :
                exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(e+1)+")"
                exec "plt.plot(t0"+str(e)+",v0"+str(e)+",label='Section "+str(rec0[e])+"', c='b')"
                exec "plt.legend(loc=0)"
                exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(self.electrodes+e+2)+")"
                exec "plt.plot(t1"+str(e)+",v1"+str(e)+",label='Section "+str(rec1[e])+"', c='r')"
                exec "plt.legend(loc=0)"
            exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(self.electrodes+1)+")"
            # to change the size of the plot use: mp.figure(1, figsize=(20,20))
            # You can change the color and marker according to the pylab documentation
            a = plt.gca()
            a.set_xlim([0,self.t_stop])
            idvec1temp = [x*(-1.0) for x in idvec1]
            plt.scatter(tvec0, idvec0, c='b', marker='+')
            plt.scatter(tvec1, idvec1temp, c='r', marker='+')
            if self.SpTrain :
                tt = []
                for i in range(len(input_spikes)):
                    tt.append(1.0)
                plt.scatter(input_spikes, tt, c='g')
    
            # FIRING RATE
            exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(2*self.electrodes+2)+")"
            a = plt.gca()
            a.set_xlim([0,self.t_stop])

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