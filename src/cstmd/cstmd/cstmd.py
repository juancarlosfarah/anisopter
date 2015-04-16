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


class Cstmd(object):
    PLOTS = True
    electrodes = 4      # How many points of the neuron should been recorded 
                        # (when PLOT_ACTIVITY==True) -The electrodes are equally 
                        # distributed accross the compartments of a neuron

    t_stop = 500
    dt = 0.25                           # default 0.025
    h.celsius = 20                      # Temperature of the cells

    # SEEDS
    stim_seed = int(time.time())        # 400
    synapses_seed = int(time.time())    # 20

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
    step_patt_rec_index = 10

    def __init__(self,
                 num_neurons,
                 num_synapses,
                 synaptic_distance,
                 num_electrodes,
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
        
        self.global_time = time.time()
        self.verbose = verbose
        self.num_neurons = num_neurons
        self.num_electrodes = num_electrodes
        # HH parameters - (Na is Sodium, K is Potassium)
        # SOS: For Na = 0.48, K below 0.0125 is not bistable, above something as well
        self.potassium = potassium #My limit: 0.0125 # Klauss used: 0.072
        self.sodium = sodium
        
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
    
        # Calculate the number of compartments of each neuron
        self.calc_compartments()

        # Take the coordinates of the middle of all the compartments:
        self.find_middle_coordinates()
        self.num_synapses = num_synapses
        self.synaptic_distance = synaptic_distance
        self.generate_synapses(self.num_synapses,
                               self.synaptic_distance,
                               potassium=-1)
        self.set_input_output()

    def calc_rand_weight(self, x, MIN, MAX, m=0.0, sigma=7.0):
        return MIN + np.random.rand()*(MAX-MIN)*np.exp(-((x-m)**2.0)/(2.0*sigma**2.0))

    # Calculate the number of compartments of each neuron and Load all neurons!
    def calc_compartments(self):
        self.NSize = []
        for n in range(self.num_neurons) :
            h.load_file(1, "../RESULTED_NEURONS/neuron"+str(n)+".hoc")
            # count the number of sections:
            self.NSize.append(0)

            # Find the total number of compartments in neurons
            for sec in h.allsec():
                self.NSize[n] += 1

            # Remove compartments of prev. neurons so we get the no of current
            i = n - 1
            while i >= 0:
                self.NSize[n] -= self.NSize[i]
                i -= 1
                
            print "This neuron has ", self.NSize[n], " compartments!"

        # This is calculated only to confirm the previous
        nAll = 0

        # All neuron's compartments together.
        for sec in h.allsec():
            nAll = nAll + 1
        print "All neurons have ", nAll, " compartments!"

    # Take the coordinates of the middle of all the compartments:
    def find_middle_coordinates(self):
        cell_list = []
        self.m_coordinates = []
        for n in range(self.num_neurons):
            cell = []
            for i in range(self.NSize[n]):
                exec "cell.append(h.neuron"+str(n)+"_tree["+str(i)+"])"
                cell[i].push()

                # Variable middle has to be an integer.
                middle = int(h.n3d() / 2)
                self.m_coordinates.append((h.x3d(middle),
                                           h.y3d(middle),
                                           h.z3d(middle)))

                # print "Yo(", i, ") Middle is ", middle, Coordinates[i]
                h.pop_section()
            cell_list.append(cell)
        self.m_coordinates
    
    def generate_synapses(self, synapses_no, synaptic_distance, potassium=-1):
        if potassium == -1:
            potassium = self.potassium

        # Find all the compartments of neuron n+1 that are closer than D to each
        # compartment of neuron n (intersection points) and could accommodate
        # possible synapses and then create 'synapses_no' synapses..!
        ss = []
        ssSize = 0
        nc = []
        ncSize = 0

        # Note: So we need at least two neurons for it to work!
        for n in range(self.num_neurons-1):
    
            # -- Find intersection points --------------------------------------
            if self.verbose :
                print "Searching for synapses for neurons ", n, " and ", n+1
            synapses = 0
            syn = []
            for a in range(self.NSize[n]):
                minimum = sys.float_info.max
                (x1, y1, z1) = self.m_coordinates[a]
                for b in range(self.NSize[n],self.NSize[n]+self.NSize[n+1]):
                    (x2, y2, z2) = self.m_coordinates[b]
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
                    if synapses < self.max_synapses:
                        if synaptic_distance > dist:
                            synapses = synapses + 1
                            syn.append((a, b-self.NSize[n]))
                    else:
                        print "WARNING: Maximum number of synapses reached!"
            if self.verbose:
                print "Synapses found: ", synapses
    
            # -- Reduce intersection points to number of synapses --------------
            if synapses < synapses_no or len(syn) < synapses_no :
                sys.exit("ERROR: There are not enough intersections to create "+\
                         "synapses. Change parameter D and run again!!")
            random.seed(self.synapses_seed)
            # Reduce the amount of synapses
            while len(syn) > synapses_no :
                random_synapse = int(random.uniform(0,len(syn)-1))
                syn.pop(random_synapse)
            print "Synapses used: ", len(syn)

            if self.verbose:
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

        if self.verbose:
            print "Generating parameters..."
        h('forall {uninsert pas}')
        h('forall {insert hh}')
        for sec in h.allsec():
            sec.gnabar_hh = self.sodium
            sec.gkbar_hh = potassium

    def set_input_output(self) :

        self.stimNet = []
        self.syn0net = []
        self.nc0net = []
        for p in range(self.num_pixels) :
            self.stimNet.append(h.IntFire2())
            self.stimNet[p].taum = 100
            self.stimNet[p].taus = 1
            # SOS: For debugging purposes, use a fixed value here so all 
            #      neurons can fire together and you can observe a 
            #      consistent EPSP
            self.stimNet[p].ib = self.min_current
            #self.stimNet[p].ib = 10.0*np.random.rand()#self.MIN_CURRENT
            # To see the current state of variable m or input current i, check
            # self.stimNet.M
            # self.stimNet.I

            # Connect every neuron to this input that represents a pixel
            for n in range(self.num_neurons) :
                # This means that the maximum weight of the whole input
                # stimulus will be from MIN to MAX
                # MIN = 0.001
                # MAX = 0.01
                
                centre = np.sqrt(self.num_pixels)/2.0
                x = p % np.sqrt(self.num_pixels)
                y = p / np.sqrt(self.num_pixels)
                dist = np.sqrt((x - centre) ** 2 + (y - centre) ** 2)
                weight = self.calc_rand_weight(dist,
                                               self.min_weight,
                                               self.max_weight)
                # weight=float(abs(self.PIXEL_NO-p))/float (self.PIXEL_NO)
                # print weight
                exec "self.syn0net.append(h.Exp2Syn(h.neuron"\
                     + str(n) + "_tree[self.input_index](0.5)))"
                self.nc0net.append(h.NetCon(self.stimNet[p],
                                            self.syn0net[-1],
                                            # Threshold.
                                            0,
                                            # Delay.
                                            0.025 + 40.0 * np.random.rand(),
                                            # Weight.
                                            weight))

        # -- Spiking recording -------------------------------------------------
        # Define the compartments whose activity will be recorded
        self.rec_output = [self.output_index] * self.num_neurons
        self.t_vec = []     # time
        self.id_vec = []    # cell number
        self.raster = []

        # Initialize the electrodes
        for n in range(self.num_neurons):
            self.t_vec.append(h.Vector())
            self.id_vec.append(h.Vector())
            exec "self.raster.append(h.NetCon(h.neuron" \
                 + str(n) + \
                 "_tree[self.rec_output[n]](.5)._ref_v, None, sec=h.neuron" \
                 + str(n) + "_tree[self.rec_output[n]]))"  # (.5)
            # -10 set threshold to a value of your choice
            self.raster[-1].threshold = 0
            self.raster[-1].record(self.t_vec[-1], self.id_vec[-1], n)

        # -- Spiking recording for pattern recognition output-------------------
        self.t_out_vec = []     # Time.
        self.id_out_vec = []    # Cell number.
        self.out_raster = []

        # Initialize the electrodes
        for n in range(self.num_neurons) :
            for i in range(self.num_electrodes):
                # The compartment number which will be recorded
                comp_idx=(i+1)*self.step_patt_rec_index+self.start_patt_rec_index
                #print "Neuron No ",n, " elec no: ",i," comp num: ",comp_idx
                self.t_out_vec.append(h.Vector())
                self.id_out_vec.append(h.Vector())
                exec "self.out_raster.append(h.NetCon(h.neuron"+str(n)+"_tree[comp_idx](.5)._ref_v, None, sec=h.neuron"+str(n)+"_tree[comp_idx]))" #(.5)
                self.out_raster[-1].threshold = 0 #-10 #set threshold to a value of your choice
                self.out_raster[-1].record(self.t_out_vec[-1], self.id_out_vec[-1], n)

        # -- Electrodes for observations ---------------------------------------
        if self.plot_activity == True :
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

    def run(self, rates, ib=0):

        if len(rates) > self.num_pixels:
            print "Error: Not enough stimuli!\nReturning..."
            return [], []            

        count = 0

        # Normalizing pixel values.
        norm = sum(rates)
        if norm != 0:
            for i in range(len(rates)):
                rates[i] = rates[i] / norm
        
        for i in range(len(rates)):
            diff = self.max_current - self.min_current
            self.stimNet[i].ib = self.min_current + 2000 * rates[i] * diff

        # print sum(rates)

        self.curr_time += self.duration

        # Adjust the limit of time in the plots.
        self.t_stop = self.curr_time

        if not self.plot_activity:
            # Delete previously recorded spikes from the vectors.
            for i in range(len(self.t_vec)):
                self.t_vec[i].clear()

        # Run the simulation.
        neuron.run(self.curr_time)
        if self.plot_activity :
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
        
        t = list(self.t_vec)
        id = self.id_vec

        return t, id, self.sp_trains()

    def sp_trains(self):

        # Container for spike trains.
        spike_trains = np.zeros((self.num_neurons*self.num_electrodes, self.curr_time))

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

    def sp_trains_save(self):

        # Container for spike trains.
        spike_trains = np.zeros((self.num_neurons*self.num_electrodes, self.curr_time))

        # Add spike occurrences to spike train.

        # For each neuron
        for n in range(self.num_neurons):

            # And each electrode.
            for i in range(self.num_electrodes):
                elec_index = (n + 1) * (i + 1) - 1
                elec_len = len(self.t_out_vec[elec_index])

                for y in range(elec_len):
                    timestamp = round(self.t_out_vec[elec_index][y], 0)
                    spike_trains[elec_index][timestamp-1] = 1
                    #print "Timestanmp" ,spike_trains[elec_index][timestamp-1]
                    #print self.t_out_vec[elec_index][y], spike_trains[elec_index][timestamp-1]  

        filename = "spike_trains/{}_{}_{}_{}_{}_{}".format(self.num_neurons,"neur",
                                                         self.num_electrodes,"elecs",
                                                         self.curr_time,"runtime")
        np.savez(filename, spike_trains=spike_trains)

    def plot(self) :
        # -- Plot the recordings -----------------------------------------------    
        if self.plot_activity == True :
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

            plt.subplot(2, self.electrodes + 1, self.electrodes + 1)
            # to change the size of the plot use: mp.figure(1, figsize=(20,20))
            # You can change the color and marker according to the pylab documentation
            a = plt.gca()
            a.set_xlim([0,self.t_stop])
            self.idvec1temp = [x*(-1.0) for x in self.id_vec[1]]
            plt.scatter(self.t_vec[0], self.id_vec[0], c='b', marker='+')
            plt.scatter(self.t_vec[1], self.idvec1temp, c='r', marker='+')

            # Firing rate.
            plt.subplot(2, self.electrodes + 1, 2 * self.electrodes + 2)
            a = plt.gca()
            a.set_xlim([0, self.t_stop])
        
            # The following part is also used in experiment 2 where we need
            # to calculate and then compare the firing rate of the first neuron.
            for neu in range(2):
                spikes = [0.0]
                my_length = len(self.t_vec[neu])

                # Save the spike occurences in a .txt file
                if self.saveSpikeRate == True :             
                    exec "spikes_file=open('CSTMD_out_spikes/spikes"+str(neu+1)+".txt','w')"

                for s in range(my_length) :
                    spikes.append(self.t_vec[neu][s])                    

                    # Save the spike occurences in a .txt file
                    if self.saveSpikeRate == True :
                       spikes_file.write(str(self.t_vec[neu][s])+"\n") 
                
                fr = []
                s = 0

                for i in range(len(spikes) - 1):
                    t0 = spikes[i]
                    t1 = spikes[i + 1]
                    s = t1 - t0
                    if s == 0:
                        sys.exit("ERROR: Division by zero!")
                    else:
                        fr.append(1000.0 / s)

                if s == 0:
                    fr.append(0.0)
                else:
                    fr.append(1000.0/s)

                if False:
                    print fr
                    return fr, []

                if neu == 0:
                    plt.plot(spikes, fr, c='b')
                elif neu == 1:
                    plt.plot(spikes, fr, c='r')
                
                if self.saveSpikeRate:
                    spikes_file.close()

            plt.figure()
            plt.scatter(self.id_input, self.t_input, c='b', marker='+')
            plt.xlim(0, self.curr_time)
            plt.show()