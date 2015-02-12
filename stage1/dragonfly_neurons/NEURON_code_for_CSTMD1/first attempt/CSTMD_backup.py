# -*- coding: utf-8 -*-
# http://www.neuron.yale.edu/neuron/static/new_doc/programming/neuronpython.html

import neuron
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math
import sys

class CSTMD(object) :
    PLOTS = True
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
    IC = 0
    NetStim = 1   # 1: T1, 2: T2, 3: T1&T2, 0: No stimulation
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
    
    # -- NEW VARIABLES ---------------------------------------------------------
    # in miliseconds    
    curr_time=0

    # Index of electrode for input
    input_indx = 0

    # Index of electrode for output
    output_indx = 1
    # --------------------------------------------------------------------------

	# IK: constructor
    def __init__(self, neurons_no, synapses_no, D, PRINT = True) :
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

        self.generate_synapses(synapses_no, D, Potassium=-1)
        self.set_input_output()


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
    



    def generate_synapses(self, synapses_no, D, Potassium=-1) :
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
        

    def set_input_output(self) :
        if self.IC :
            self.stimIC = h.IClamp(h.neuron0_tree[720](0.5))
            self.stimIC.delay = self.stim_start   # [ms]
            self.stimIC.dur = self.stim_duration  # [ms]
            self.stimIC.amp = self.stim_amp       # [nA] amplitude
            self.syn0ic = h.Exp2Syn(h.neuron0_tree[3](0.5)) # 720
            self.nc0ic = h.NetCon(stimIC,syn0ic,0,0.025+delay_of_T1,0.05) # threshold, delay, weight
            self.syn1ic = h.Exp2Syn(h.neuron1_tree[3](0.5)) # 720
            self.nc1ic = h.NetCon(stimIC,syn1ic,0,0.025,0.01) # threshold, delay, weight
        elif self.NetStim:
            # Experiment 2
            if self.NetStim == 1:
                self.w1_n0 = 0.05
                self.w1_n1 = 0.01
                self.w2_n0 = 0.0
                self.w2_n1 = 0.0
            elif self.NetStim == 2: 
                self.w1_n0 = 0.0
                self.w1_n1 = 0.0
                self.w2_n0 = 0.01
                self.w2_n1 = 0.05
            elif  self.NetStim == 3 :
                self.w1_n0 = 0.05
                self.w1_n1 = 0.01
                self.w2_n0 = 0.01
                self.w2_n1 = 0.05
    
            # First stimulus
            self.stimNet1 = h.NetStim()
            self.stimNet1.start = self.stim_start  # like delay
            self.stimNet1.number = self.stim_numb  # Number of spikes
            self.stimNet1.noise = self.stim_noise  # 0
            self.stimNet1.seed(self.stim_seed)
            self.syn0net1 = h.Exp2Syn(h.neuron0_tree[3](0.5))
            self.nc0net1  = h.NetCon(self.stimNet1,self.syn0net1,0,0.025+self.delay_of_T1,self.w1_n0) # threshold, delay, weight
            self.syn1net1 = h.Exp2Syn(h.neuron1_tree[3](0.5))
            self.nc1net1  = h.NetCon(self.stimNet1,self.syn1net1,0,0.025,self.w1_n1) # threshold, delay, weight
            # Second stimulus
            self.stimNet2 = h.NetStim()
            self.stimNet2.start = self.stim_start  # like delay
            self.stimNet2.number = self.stim_numb  # Number of spikes
            self.stimNet2.noise = self.stim_noise  # 0
            self.stimNet2.seed(self.stim_seed+10)
            self.syn0net2 = h.Exp2Syn(h.neuron0_tree[3](0.5))
            self.nc0net2  = h.NetCon(self.stimNet2,self.syn0net2,0,0.025,self.w2_n0)
            self.syn1net2 = h.Exp2Syn(h.neuron1_tree[3](0.5))
            self.nc1net2  = h.NetCon(self.stimNet2,self.syn1net2,0,0.025+self.delay_of_T2,self.w2_n1)
        elif self.SpTrain:
            stimNet = h.NetStim()
            stimNet.start = 0
            stimNet.number = 0
            stimNet.noise = 0
            syn0net = h.Exp2Syn(h.neuron0_tree[2](0.5))
            nc0net  = h.NetCon(stimNet,syn0net,0,0.025,0.0045)
            syn1net = h.Exp2Syn(h.neuron1_tree[2](0.5))
            nc1net  = h.NetCon(stimNet,syn1net,0,0.025,0.0015)
            

        if self.PRINTS : print "Setting output.."

        # Spiking recording
        # Define the compartments whose activity will be recorded
        self.rec_output = [self.output_indx]*self.neurons_no
        
        self.t_vec = [] #time
        self.id_vec = [] #cell number
        self.raster = []

        # Initialize the electrodes
        for n in range(self.neurons_no) :
            self.t_vec.append(h.Vector())
            self.id_vec.append(h.Vector())
            exec "self.raster.append(h.NetCon(h.neuron"+str(n)+"_tree[self.rec_output[n]](.5)._ref_v, None, sec=h.neuron"+str(n)+"_tree[self.rec_output[n]]))" #(.5)
            self.raster[-1].threshold = 0 #-10 #set threshold to a value of your choice
            self.raster[-1].record(self.t_vec[-1], self.id_vec[-1], n)
   






        # ------------------------
        if self.PRINTS :
            print "OK!"

        # RUN THE SIMULATION:
        #def run_experiment():
        #define the compartments whose activity will be recorded
        self.rec0_size = int(self.NSize[0] / self.electrodes)
        self.rec1_size = int(self.NSize[1] / self.electrodes)
        self.rec0 = []
        self.rec1 = []
        for i in range(self.electrodes) :
            self.rec0.append(self.rec0_size*i)
            self.rec1.append(self.rec1_size*i)

        # Initialize the electrodes
        if self.PLOTS:
            for e in range(self.electrodes) :
                print "!AAAA"
                exec "self.vrec0"+str(e)+" = h.Vector()"
                exec "self.trec0"+str(e)+" = h.Vector()"
                exec "self.vrec1"+str(e)+" = h.Vector()"
                exec "self.trec1"+str(e)+" = h.Vector()"
                exec "self.vrec0"+str(e)+".record(h.neuron0_tree["+str(self.rec0[e])+"](0.5)._ref_v)"
                exec "self.trec0"+str(e)+".record(h._ref_t)"
                exec "self.vrec1"+str(e)+".record(h.neuron1_tree["+str(self.rec1[e])+"](0.5)._ref_v)"
                exec "self.trec1"+str(e)+".record(h._ref_t)"
        # ------------------------







        # Finalize initialization
        h.finitialize(-60)
        h.dt = self.dt


    #Stimulation
    def run(self, time) :
        self.curr_time += time


        # Set the spike trains
        if self.SpTrain :
            for input_spike in input_spikes :
                nc0net.event(input_spike + self.delay_of_T1)
                nc1net.event(input_spike)

        print "Running for", time, "ms"
        #start_time = time.time()
        # Run the simulation

        neuron.run(self.curr_time)
        print "Raster stuff:"
        for i in range(len(self.t_vec)) :
            print i
            for j in range(len(self.t_vec)) :
                print "\b ", j, ":", self.t_vec[i][j], self.id_vec[i][j]

        #return []
        #print "Time:", time.time() - start_time

        #print "Result: (neuron0, neuron1) =      ", len(self.tvec0),",   ",len(self.tvec1)
        #return []

        # Plot the recordings    
        if self.PLOTS :
            plt.figure(1)
            for e in range(self.electrodes) :
                exec "t0"+str(e)+" = np.array(self.trec0"+str(e)+")"
                exec "v0"+str(e)+" = np.array(self.vrec0"+str(e)+")"
                exec "t1"+str(e)+" = np.array(self.trec1"+str(e)+")"
                exec "v1"+str(e)+" = np.array(self.vrec1"+str(e)+")"
            for e in range(self.electrodes) :
                exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(e+1)+")"
                exec "plt.plot(t0"+str(e)+",v0"+str(e)+",label='Section "+str(self.rec0[e])+"', c='b')"
                exec "plt.legend(loc=0)"
                exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(self.electrodes+e+2)+")"
                exec "plt.plot(t1"+str(e)+",v1"+str(e)+",label='Section "+str(self.rec1[e])+"', c='r')"
                exec "plt.legend(loc=0)"
            exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(self.electrodes+1)+")"
            # to change the size of the plot use: mp.figure(1, figsize=(20,20))
            # You can change the color and marker according to the pylab documentation
            a = plt.gca()
            a.set_xlim([0,self.t_stop])
            self.idvec1temp = [x*(-1.0) for x in self.id_vec[1]]
            plt.scatter(self.t_vec[0], self.id_vec[0], c='b', marker='+')
            plt.scatter(self.t_vec[1], self.idvec1temp, c='r', marker='+')
            if self.SpTrain :
                tt = []
                for i in range(len(self.input_spikes)):
                    tt.append(1.0)
                plt.scatter(self.input_spikes, tt, c='g')
    
            # FIRING RATE
            exec "plt.subplot(2,"+str(self.electrodes+1)+","+str(2*self.electrodes+2)+")"
            a = plt.gca()
            a.set_xlim([0,self.t_stop])

        # The following part is also used in experiment 2 where we need to calculate
        # and then compare the firing rate of the first neuron
        if self.PLOTS or False:
            for neu in range(2) :
                spikes = [0.0]
                my_length = 0
                my_length = len(self.t_vec[neu])
                for s in range(my_length) :
                    spikes.append(self.t_vec[neu][s])
                
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
                if False :
                    print fr
                    return fr, []
                if neu == 0:
                    plt.plot(spikes, fr, c='b')
                elif neu == 1:
                    plt.plot(spikes, fr, c='r')
        plt.show()



