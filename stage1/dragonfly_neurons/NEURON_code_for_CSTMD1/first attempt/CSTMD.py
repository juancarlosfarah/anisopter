# -*- coding: utf-8 -*-
# http://www.neuron.yale.edu/neuron/static/new_doc/programming/neuronpython.html

import neuron
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math
import time
import sys

class CSTMD(object) :
    PLOTS = True
    # -- PARAMETERS ------------------------------------------------------------
    electrodes = 4      # How many points of the neuron should been recorded 
                        # (when PLOT_ACTIVITY==True) -The electrodes are equally 
                        # distributed accross the compartments of a neuron

    t_stop = 500

    dt = 0.25       # default 0.025
    h.celsius = 20  # Temperature of the cells

    # SEEDS
    stim_seed = int(time.time())#400 
    synapses_seed = int(time.time())#20

    # Synapses
    weights = 0.01
    thresholds = 0.0
    delays = 1.0
    max_synapses = 10000 # maximum limit of synapses in case where we are very close

    # Stimulation
    IC = 0
    NetStim = 0   # 1: T1, 2: T2, 3: T1&T2, -1: Visual input
    SpTrain = False
    IntFire = True
    
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
    output_indx = 323
    
    # Plot an array of electrodes for neurons 0 and 1
    PLOT_ACTIVITY = True


    PIXEL_NO = 4096
    MAX_CURRENT = 10.0
    MIN_CURRENT = 2.0
    # --------------------------------------------------------------------------


    # -- Helper functions ------------------------------------------------------
    def calc_rand_weight(self, x, MIN, MAX) :
        return MIN + np.random.rand()*((MAX-MIN)*np.exp(-x)**2.0)/800.0

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
        
        
        # Take the coordinates of the middle of all the compartments:
        self.find_middle_coordinates()
            

        self.generate_synapses(synapses_no, D, Potassium=-1)
        self.set_input_output()


    # Calculate the number of compartments of each neuron and Load all neurons!
    def calc_compartments(self) :
        self.NSize = []
        for n in range(self.neurons_no) :
            h.load_file(1, "../RESULTED_NEURONS/neuron"+str(n)+".hoc")
            # count the number of sections:
            self.NSize.append(0)
            # Find the total number of compartments in neurons
            for sec in h.allsec():
                self.NSize[n] = self.NSize[n] + 1
            # Remove compartments of prev. neurons so we get the no of current
            i = n-1
            while i >= 0 :
                self.NSize[n] -= self.NSize[i]
                i -= 1
                
            print "This neuron has ", self.NSize[n], " compartments!"

        # This is calculated only to confirm the previous
        nAll = 0
        for sec in h.allsec(): # All neuron's compartments together
            nAll = nAll + 1
        print "All neurons have ", nAll, " compartments!"
    
    
    # Take the coordinates of the middle of all the compartments:
    def find_middle_coordinates(self) :
        cell_list = []
        self.m_coordinates = []
        for n in range(self.neurons_no) :
            cell = []
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
            print "Generating parameters..."
        h('forall {uninsert pas}')
        h('forall {insert hh}')
        for sec in h.allsec() :
            sec.gnabar_hh =  self.Na
            sec.gkbar_hh =  Potassium
        

    def set_input_output(self) :
        if self.IntFire:

            """
            self.w1_n0 = 0.05
                # First stimulus
            self.stimNet = h.IntFire2()
            self.stimNet.taum = 100
            self.stimNet.taus = 1
            self.stimNet.ib = 2.0
            # To see the current state of variable m or input current i, check
            # self.stimNet.M
            # self.stimNet.I
            self.syn0net = h.Exp2Syn(h.neuron0_tree[self.input_indx](0.5))
            self.nc0net  = h.NetCon(self.stimNet,self.syn0net,0,0.025+self.delay_of_T1,self.w1_n0) # threshold, delay, weight
            """


            self.stimNet = []
            self.syn0net = []
            self.nc0net = []
            for p in range(self.PIXEL_NO) :
                self.stimNet.append(h.IntFire2())
                self.stimNet[p].taum = 100
                self.stimNet[p].taus = 1
                self.stimNet[p].ib = self.MIN_CURRENT
                # To see the current state of variable m or input current i, check
                # self.stimNet.M
                # self.stimNet.I

                # Connect every neuron to this input that represents a pixel
                for n in range(self.neurons_no) :
                    # This means that the maximum weight of the whole input
                    # stimulus will be from MIN to MAX
                    MIN = 0.01
                    MAX = 0.1 # SOS ZAF: The correct value is 0.01
                    
                    Centre = np.sqrt(self.PIXEL_NO)/2.0
                    x = p % np.sqrt(self.PIXEL_NO)
                    y = p / np.sqrt(self.PIXEL_NO)
                    Dist = np.sqrt( (x-Centre)**2 + (y-Centre)**2 )

                    weight = self.calc_rand_weight(Dist, MIN, MAX)/float(self.PIXEL_NO)
                    exec "self.syn0net.append(h.Exp2Syn(h.neuron"+str(n)+"_tree[self.input_indx](0.5)))"
                    self.nc0net.append(h.NetCon(self.stimNet[p],
                                                self.syn0net[-1],
                                                0,0.025+self.delay_of_T1,
                                                weight)) # threshold, delay, weight


        elif self.IC :
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
            if self.NetStim == -1:

                self.stimNet = []
                self.syn0net = []
                self.nc0net = []
                for p in range(self.PIXEL_NO) :
                    self.stimNet.append(h.NetStim())
                    self.stimNet[p].start = 0  # like delay
                    self.stimNet[p].number = 2  # Number of spikes
                    self.stimNet[p].interval = 5
                    self.stimNet[p].noise = self.stim_noise  # 0
                    self.stimNet[p].seed(self.stim_seed)

                    # Connect every neuron to this input that represents a pixel
                    for n in range(self.neurons_no) :
                        # This means that the maximum weight of the whole input
                        # stimulus will be from MIN to MAX
                        MIN = 0.00001
                        MAX = 0.0001 # SOS ZAF: The correct value is 0.01
                        weight = (MIN + np.random.rand()*(MAX-MIN))/float(self.PIXEL_NO)
                        exec "self.syn0net.append(h.Exp2Syn(h.neuron"+str(n)+"_tree[self.input_indx](0.5)))"
                        self.nc0net.append(h.NetCon(self.stimNet[p],
                                                    self.syn0net[-1],
                                                    0,0.025+self.delay_of_T1,
                                                    weight)) # threshold, delay, weight


            else :
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
            

        print "Setting output.."

        # -- Spiking recording -------------------------------------------------
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
        # ----------------------------------------------------------------------


        # -- Electrodes for observations ---------------------------------------
        if self.PLOT_ACTIVITY == True :
            #define the compartments whose activity will be recorded
            self.rec0_size = int(self.NSize[0] / self.electrodes)
            self.rec1_size = int(self.NSize[1] / self.electrodes)
            print self.rec0_size
            print self.rec1_size
            self.rec0 = []
            self.rec1 = []
            for i in range(self.electrodes) :
                self.rec0.append(self.rec0_size*i)
                self.rec1.append(self.rec1_size*i)

            # Initialize electrodes
            if self.PLOTS:
                for e in range(self.electrodes) :
                    exec "self.vrec0"+str(e)+" = h.Vector()"
                    exec "self.trec0"+str(e)+" = h.Vector()"
                    exec "self.vrec1"+str(e)+" = h.Vector()"
                    exec "self.trec1"+str(e)+" = h.Vector()"
                    exec "self.vrec0"+str(e)+".record(h.neuron0_tree["+str(self.rec0[e])+"](0.5)._ref_v)"
                    exec "self.trec0"+str(e)+".record(h._ref_t)"
                    exec "self.vrec1"+str(e)+".record(h.neuron1_tree["+str(self.rec1[e])+"](0.5)._ref_v)"
                    exec "self.trec1"+str(e)+".record(h._ref_t)"



                    self.id_input = h.Vector()
                    self.t_input = h.Vector()
                    self.raster_input = h.NetCon(self.stimNet[0], None)
                    self.raster_input.threshold = 0 #-10 #set threshold to a value of your choice
                    self.raster_input.record(self.id_input,self.t_input)

        # ----------------------------------------------------------------------

        # Finalize initialization
        h.finitialize(-60)
        h.dt = self.dt


    def run(self, time, rates,ib=0) :
        print "len ",len(rates)
        #if self.IntFire:
        #    self.stimNet.ib = ib

        if self.IntFire:
            if len(rates) > self.PIXEL_NO :
                print "Error: Not enough stimuli!\nReturning.."
                return [], []
            
            for i in range(len(rates)) :
                self.stimNet[i].ib = self.MIN_CURRENT + rates[i]*(self.MAX_CURRENT-self.MIN_CURRENT)

        self.curr_time += time

        if not self.PLOT_ACTIVITY :
            # Delete previously recorded spikes from the vectors
            for i in range(len(self.t_vec)) :
                self.t_vec[i].clear()


         # Run the simulation
        neuron.run(self.curr_time)
        if self.PLOT_ACTIVITY :
            print "Raster stuff:"
            for i in range(len(self.t_vec)) :
                print "Spikes of neuron",str(i)+":", len(self.t_vec[i])

        #if self.IntFire:
        #    print self.stimNet[0].M()
        #    print self.stimNet[0].I()


        #for i in range(len(self.t_vec)) :
        #    print i
        #    for j in range(len(self.t_vec[i])) :
        #        print "\b ", j, ":", self.t_vec[i][j], self.id_vec[i][j]



        #print "Result: (neuron0, neuron1) =      ", len(self.tvec0),",   ",len(self.tvec1)
        
        T = list(self.t_vec)
        ID = self.id_vec

        return T, ID

    def plot(self) :
        # -- Plot the recordings -----------------------------------------------    
        if self.PLOT_ACTIVITY == True :
            plt.figure(1)
            for e in range(self.electrodes) :
                exec "t0"+str(e)+" = np.array(self.trec0"+str(e)+")"
                exec "v0"+str(e)+" = np.array(self.vrec0"+str(e)+")"
                exec "t1"+str(e)+" = np.array(self.trec1"+str(e)+")"
                exec "v1"+str(e)+" = np.array(self.vrec1"+str(e)+")"
            for e in range(self.electrodes) :
                plt.subplot(2,self.electrodes+1,e+1)
                exec "plt.plot(t0"+str(e)+",v0"+str(e)+",label='Section "+str(self.rec0[e])+"', c='b')"
                plt.legend(loc=0)
                plt.subplot(2,self.electrodes+1,self.electrodes+e+2)
                exec "plt.plot(t1"+str(e)+",v1"+str(e)+",label='Section "+str(self.rec1[e])+"', c='r')"
                plt.legend(loc=0)

            plt.subplot(2,self.electrodes+1,self.electrodes+1)
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
            plt.subplot(2,self.electrodes+1, 2*self.electrodes+2)
            a = plt.gca()
            a.set_xlim([0,self.t_stop])

        
            # The following part is also used in experiment 2 where we need to calculate
            # and then compare the firing rate of the first neuron
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


            plt.figure()
            plt.scatter(self.id_input, self.t_input, c='b', marker='+')
            plt.xlim(0, self.curr_time)
            plt.show()








