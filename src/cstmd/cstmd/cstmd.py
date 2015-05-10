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
import os
class Cstmd(object) :

    # -- PARAMETERS ------------------------------------------------------------
    t_stop = 500


    dt = 0.25       # default 0.025
    h.celsius = 20  # Temperature of the cells

    # SEEDS
    stim_seed = 400 
    synapses_seed = 20

    # Synapses
    weights = 0.01
    thresholds = 0.0
    delays = 1.0
    max_synapses = 10000                # maximum limit of synapses
    curr_time = 0                       # ms
    input_index = 0                     # Index of electrode for input
    output_index = 323                  # Index of electrode for output

    # Start index of compartments for pattern recognition output
    start_patt_rec_index = 10

    # Compartment number step for pattern recognition output
    step_patt_rec_index = 5

    def __init__(self,
                 num_neurons,
                 num_synapses,
                 synaptic_distance,
                 num_electrodes,
                 input,
                 verbose=True,
                 potassium=0.06,
                 sodium=0.48,
                 num_pixels=4096,
                 max_current=30,
                 min_current=2.0,
                 min_weight=0.000005,
                 max_weight=0.00005,
                 plot_activity=True,
                 duration=10,
                 description=""):

        #### Compartment activity recordings' vars
        self.rec=[]
        self.vrec=[]
        self.trec=[]
        ####################
        self.electrodes = 4      # How many points of the neuron should been recorded 
                        # (when SINGLE_TEST==True) - The electrodes are equally 
                        # distributed accross the compartments of a neuron

        self.runtime = 0
        self.input = input
        self.global_time = time.time()
        self.verbose = verbose
        self.num_neurons = num_neurons
        self.num_electrodes = num_electrodes
        # HH parameters - (Na is Sodium, K is Potassium)
        # SOS: For Na = 0.48, K below 0.0125 is not bistable, above something as well
        self.potassium = potassium #My limit: 0.0125 # Klauss used: 0.072
        self.sodium = sodium

        # Store spike trains here.
        self.spike_trains = None
        
        # Nice combination of values for debugging because the neuron doesn't fire
        # Na = 0.2
        # K = 0.06

        # K = 0.02
        # Na = 0.48

        # SOS: We should leave Sodium constant and vary the Potassium
        # The thick dendrites should be around 5 microMeters
        # the thin ones around 1.5...

        # Plot an array of electrodes for neurons 0 and 1
        self.plot_activity = plot_activity
        self.num_pixels = num_pixels
        self.max_current = max_current  # 10.0
        self.min_current = min_current  # 5

        # Save spike rate to txt file
        self.saveSpikeRate = False

        # Minimum and maximum allowed weight of input neurons to CSTMDs.
        self.min_weight = min_weight
        self.max_weight = max_weight

        # running time of the simulation
        self.duration = duration

        # For website purposes
        self.description = description

        # THINGS THAT RUN ONLY ONCE 

        # Number of compartments for each neuron 
        self.NSize = []
   
        # Calculate the number of compartments of each neuron
        self.calc_compartments()

        # Take the coordinates of the middle of all the compartments:
        self.find_middle_coordinates()
        self.num_synapses = num_synapses
        self.synaptic_distance = synaptic_distance
           
    # -- Helper functions ------------------------------------------------------
    def calc_rand_weight(self, x, MIN, MAX, m=0.0, sigma=7.0) :
        return MIN + np.random.rand()*(MAX-MIN)*np.exp( -((x-m)**2.0)/(2.0*sigma**2.0)  )



    # Calculate the number of compartments of each neuron and Load all neurons!
    def calc_compartments(self) :

        for n in range(self.num_neurons) :
            #h.load_file(1, "cstmd/RESULTED_NEURONS/neuron"+str(n)+".hoc")
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
                
            if self.verbose : print "This neuron has ", self.NSize[n], " compartments!"

        # This is calculated only to confirm the previous
        nAll = 0
        for sec in h.allsec(): # All neuron's compartments together
            nAll = nAll + 1
        if self.verbose : print "All neurons have ", nAll, " compartments!"
    
    
    # Take the coordinates of the middle of all the compartments:
    def find_middle_coordinates(self) :
        cell_list = []
        self.m_coordinates = []
        for n in range(self.num_neurons) :
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

    def run(self) :

        # Find all the compartments of neuron n+1 that are closer than D to to each
        # compartment of neuron n (intersection points) and could accomodate 
        # possible synapses and then  create 'synapses_no' synapses..!
        ss = []
        ssSize = 0
        nc = []
        ncSize = 0
        for n in range(self.num_neurons-1): # Note: So we need at least two neurons for it to work!
    
            # -- Find intersection points ------------------------------------------
            if self.verbose :
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
                        if self.synaptic_distance > dist :
                            synapses = synapses + 1
                            syn.append((a,b-self.NSize[n]))
                    else :
                        print "WORNING: We reached the maximum number of synapses"
            if self.verbose :
                print "Synapses found: ", synapses
    
            # -- Reduce intersection points to number of synapses ------------------
            if synapses < self.num_synapses or len(syn) < self.num_synapses :
                sys.exit("ERROR: There are not enough intersections to create "+\
                         "synapses. Change parameter D and run again!!")
            random.seed(self.synapses_seed)
            # Reduce the amount of synapses
            while len(syn) > self.num_synapses :
                random_synapse = int(random.uniform(0,len(syn)-1))
                syn.pop(random_synapse)
            print "Synapses used: ", len(syn)
                
            # ------------------------------------------------------------------- #
            if self.verbose :
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
            if self.verbose :
                print "OK!"
        
        if self.verbose :
            print "Generating parameters..."
        h('forall {uninsert pas}')
        h('forall {insert hh}')
        for sec in h.allsec() :
            sec.gnabar_hh =  self.sodium
            sec.gkbar_hh =  self.potassium
       
        #Stimulation
        self.stimNet = []
        self.syn0net = []
        self.nc0net = []
        for p in range(self.num_pixels) :

            self.stimNet.append(h.IntFire2())
            self.stimNet[p].taum = 100
            self.stimNet[p].taus = 1
            self.stimNet[p].ib = self.min_current


            # Connect every neuron to this input that represents a pixel
            for n in range(self.num_neurons) :
                
                Centre = np.sqrt(self.num_pixels)/2.0
                x = p % np.sqrt(self.num_pixels)
                y = p / np.sqrt(self.num_pixels)
                Dist = np.sqrt( (x-Centre)**2 + (y-Centre)**2 )

                weight = self.calc_rand_weight(Dist, self.min_weight, self.max_weight)
               
                exec "self.syn0net.append(h.Exp2Syn(h.neuron"+str(n)+"_tree[3](0.5)))"
                self.nc0net.append(h.NetCon(self.stimNet[p],
                                            self.syn0net[-1],
                                            0, # Threshold
                                            0.025+40.0*np.random.rand(), # Delay
                                            weight)) # Weight  
        # Define the compartments whose activity will be recorded
    
        self.t_vec = [] #time
        self.id_vec = [] #cell number
        self.raster = []
	
        # Initialize the electrodes
        for n in range(self.num_neurons) :
            self.t_vec.append(h.Vector())
            self.id_vec.append(h.Vector())
            exec "self.raster.append(h.NetCon(h.neuron"+str(n)+"_tree[1](.5)._ref_v, None, sec=h.neuron"+str(n)+"_tree[1]))" #(.5)
            self.raster[-1].threshold = 0 #-10 #set threshold to a value of your choice
            self.raster[-1].record(self.t_vec[-1], self.id_vec[-1], n)
        # ----------------------------------------------------------------------

        # -- Spiking recording for pattern recognition output-------------------
        self.t_out_vec = []     # Time.
        self.id_out_vec = []    # Cell number.
        self.out_raster = []

        # Initialize the electrodes
        for n in range(self.num_neurons) :
            for i in range(self.num_electrodes):
                # The compartment number which will be recorded
                comp_idx=self.start_patt_rec_index+i*(self.step_patt_rec_index )
                #print "Neuron No ",n, " elec no: ",i," comp num: ",comp_idx
                self.t_out_vec.append(h.Vector())
                self.id_out_vec.append(h.Vector())
                exec "self.out_raster.append(h.NetCon(h.neuron"+str(n)+"_tree[comp_idx](.5)._ref_v, None, sec=h.neuron"+str(n)+"_tree[comp_idx]))" #(.5)
                self.out_raster[-1].threshold = 0 #-10 #set threshold to a value of your choice
                self.out_raster[-1].record(self.t_out_vec[-1], self.id_out_vec[-1], n)
        # ----------------------------------------------------------------------
    
        # RUN THE SIMULATION: Plot recordings

        #define the compartments whose activity will be recorded
        recsize=[]
        self.rec=[]
        for n in range(self.num_neurons) :
            self.rec.append([])
            recsize.append(int(self.NSize[n] / self.electrodes))
            for i in range(self.electrodes) :
                self.rec[n].append(recsize[n]*i)

        # Initialize the electrodes
        for e in range(self.electrodes):
            for n in range(self.num_neurons):
                exec "self.vrec" + str(n) + str(e) + " = h.Vector()"
                exec "self.trec" + str(n) + str(e) + " = h.Vector()"
                exec "self.vrec" + str(n) + str(
                    e) + ".record(h.neuron" + str(
                    n) + "_tree[" + str(self.rec[n][e]) + "](0.5)._ref_v)"
                exec "self.trec" + str(n) + str(e) + ".record(h._ref_t)"

        # Finalize initialization
        h.finitialize(-60)
        h.dt = self.dt


        # Run the simulation
        pixels=len(self.input[0])	
        #print "pix",len(self.input[0]),self.num_pixels
        self.runtime = self.duration

        for frame_object in self.input:
            frame = np.array(frame_object['frame'])
            for n in range(pixels) :
                self.stimNet[n].ib = self.min_current+100*frame[n]*(self.max_current-self.min_current)

            neuron.run(self.runtime)
            self.runtime += self.duration

            print "Raster stuff:"
            for i in range(len(self.t_vec)):
                print "Spikes of neuron", str(i) + ":", len(self.t_vec[i])

        return list(self.t_vec),self.sp_trains()

    def sp_trains(self):

        # Container for spike trains.
        spike_trains = np.zeros((self.num_neurons * self.num_electrodes,
                                 self.runtime))

        # Add spike occurrences to spike train

        # For each neuron.
        for n in range(self.num_neurons):

            # And each electrode.
            for i in range(self.num_electrodes):
                elec_index = (n + 1) * (i + 1) - 1
                elec_len = len(self.t_out_vec[elec_index])

                for y in range(elec_len):
                    timestamp = round(self.t_out_vec[elec_index][y], 0)
                    spike_trains[elec_index][timestamp-1] = 1

        return spike_trains

    def plot_compart_act(self,_id) :     
        plt.figure(1)

        for e in range(self.electrodes) :
            for n in range(self.num_neurons) :
                exec "t"+str(n)+str(e)+" = np.array(self.trec"+str(n)+str(e)+")"
                exec "v"+str(n)+str(e)+" = np.array(self.vrec"+str(n)+str(e)+")"
        for e in range(self.electrodes) :
            for n in range(self.num_neurons) :

                if n == 0:
                   exec "plt.subplot("+str(self.num_neurons)+","+str(self.electrodes+1)+","+str(e+1)+")"
                   exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='b')"
                   exec "plt.legend(loc=0)"
                elif n == 1:
                   exec "plt.subplot("+str(self.num_neurons)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                   exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='r')"
                   exec "plt.legend(loc=0)"
                elif n == 2:
                   exec "plt.subplot("+str(self.num_neurons)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                   exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='g')"
                   exec "plt.legend(loc=0)"
                elif n == 3:
                   exec "plt.subplot("+str(self.num_neurons)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                   exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='y')"
                   exec "plt.legend(loc=0)"
                elif n == 4:
                   exec "plt.subplot("+str(self.num_neurons)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                   exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='k')"
                   exec "plt.legend(loc=0)"

        # Save Plots.
        relative_path = "../../server/assets/cstmd/" + str(_id)

        # Create the path for the plots
        if not os.path.exists(relative_path):
            os.makedirs(relative_path)

        out_directory = os.path.abspath(relative_path + "compart_act" + ".png")      
        print "Saving animation in: " + out_directory  
        plt.savefig(out_directory)

    def plot_fir_rate(self,_id) :
        plt.figure(2)  
        for neu in range(self.num_neurons) :
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

            if neu == 0:
                plt.plot(spikes, fr, c='b')
            elif neu == 1:
                plt.plot(spikes, fr, c='r')
            elif neu == 2:
                plt.plot(spikes, fr, c='g')
            elif neu == 3:
                plt.plot(spikes, fr, c='y')
            elif neu == 4:
                plt.plot(spikes, fr, c='k')

        # Save Plots.
        relative_path = "../../server/assets/cstmd/" + str(_id)

        # Create the path for the plots
        if not os.path.exists(relative_path):
            os.makedirs(relative_path)

        out_directory = os.path.abspath(relative_path + "fir_rate" + ".png")
        print "Saving animation in: " + out_directory
        plt.savefig(out_directory)
