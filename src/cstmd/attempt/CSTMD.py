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

class CSTMD(object) :

    # -- PARAMETERS ------------------------------------------------------------
    electrodes = 4      # How many points of the neuron should been recorded 
                        # (when SINGLE_TEST==True) - The electrodes are equally 
                        # distributed accross the compartments of a neuron

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
    max_synapses = 10000 # maximum limit of synapses in case where we are very close

    # Stimulation
    IC = 0
    IntFire =1
 
    
    delay_of_T1 = 13 # [ms]
    delay_of_T2 = 50 # [ms]
    stim_start = 50 # [ms]
    stim_duration = 1500 # [ms]
    stim_amp = 1.6 # [nA] amplitude
    stim_numb = 20
    stim_noise = 0




    def __init__(self, 
                neurons_no,
                synapses_no,
                D,
                electrds,
		input,
                PLOT_ACTIVITY ,
                PRINT = True,
                K=0.06,
                Na=0.48,
                PIXEL_NO = 4096,
                MAX_CURRENT = 30,
                MIN_CURRENT = 2.0,
                MIN = 0.000005,
                MAX = 0.00005,
                runtime=10,
                description="") :
        
	self.global_time = time.time()
        self.PRINTS = PRINT
        self.neurons_no = neurons_no
        self.electrds=electrds    
        # HH parameters - (Na is Sodium, K is Potassium)
        # SOS: For Na = 0.48, K below 0.0125 is not bistable, above something as well
        self.K = K #My limit: 0.0125 # Klauss used: 0.072
        self.Na = Na
        
        # Nice combination of values for debugging because the neuron doesn't fire
        #Na = 0.2
        #K = 0.06

        #K = 0.02
        #Na = 0.48


        # SOS: We should leave Sodium constant and vary the Potassium
        # The thick dendrites should be arround 5 microMeters
        # the thin ones arround 1.5...


        # Plot an array of electrodes for neurons 0 and 1
        self.PLOT_ACTIVITY = PLOT_ACTIVITY

        self.PIXEL_NO = PIXEL_NO
        self.MAX_CURRENT = MAX_CURRENT #10.0
        self.MIN_CURRENT = MIN_CURRENT #5

        #Save spike rate to txt file
        self.saveSpikeRate=False    
     

        # Minimum and maximum allowed weight of input neurons to CSTMDs
        self.MIN = MIN
        self.MAX = MAX

        #running time of the simulation
        self.runtime=runtime

        # For website purposes
        self.description=description
	self.synapses_no=synapses_no

	self.input=input
	self.D=D
        # THINGS THAT RUN ONLY ONCE 
    
        # Calculate the number of compartments of each neuron
        self.calc_compartments()

        
        # Take the coordinates of the middle of all the compartments:
        self.find_middle_coordinates()

           
    # -- Helper functions ------------------------------------------------------
    def calc_rand_weight(self, x, MIN, MAX, m=0.0, sigma=7.0) :
    	return MIN + np.random.rand()*(MAX-MIN)*np.exp( -((x-m)**2.0)/(2.0*sigma**2.0)  )



    # Calculate the number of compartments of each neuron and Load all neurons!
    def calc_compartments(self) :
        self.NSize = []
        for n in range(self.neurons_no) :
            h.load_file(1, "cstmd/RESULTED_NEURONS/neuron"+str(n)+".hoc")
            #h.load_file(1, "../RESULTED_NEURONS/neuron"+str(n)+".hoc")
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
                
            if self.PRINTS : print "This neuron has ", self.NSize[n], " compartments!"

        # This is calculated only to confirm the previous
        nAll = 0
        for sec in h.allsec(): # All neuron's compartments together
            nAll = nAll + 1
        if self.PRINTS : print "All neurons have ", nAll, " compartments!"
    
    
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

    def run(self) :

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
                        if self.D > dist :
                            synapses = synapses + 1
                            syn.append((a,b-self.NSize[n]))
                    else :
                        print "WORNING: We reached the maximum number of synapses"
            if self.PRINTS :
                print "Synapses found: ", synapses
    
            # -- Reduce intersection points to number of synapses ------------------
            if synapses < self.synapses_no or len(syn) < self.synapses_no :
                sys.exit("ERROR: There are not enough intersections to create "+\
                         "synapses. Change parameter D and run again!!")
            random.seed(self.synapses_seed)
            # Reduce the amount of synapses
            while len(syn) > self.synapses_no :
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
            sec.gkbar_hh =  self.K
       
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
        
        elif self.IntFire:

            self.stimNet = []
            self.syn0net = []
            self.nc0net = []
            for p in range(self.PIXEL_NO) :

                self.stimNet.append(h.IntFire2())
                self.stimNet[p].taum = 100
                self.stimNet[p].taus = 1
                self.stimNet[p].ib = 50 +2*p #self.MIN_CURRENT


                # Connect every neuron to this input that represents a pixel
                for n in range(self.neurons_no) :
                    
                    Centre = np.sqrt(self.PIXEL_NO)/2.0
                    x = p % np.sqrt(self.PIXEL_NO)
                    y = p / np.sqrt(self.PIXEL_NO)
                    Dist = np.sqrt( (x-Centre)**2 + (y-Centre)**2 )

                    weight = self.calc_rand_weight(Dist, self.MIN, self.MAX)
                   
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
        for n in range(self.neurons_no) :
            self.t_vec.append(h.Vector())
            self.id_vec.append(h.Vector())
            exec "self.raster.append(h.NetCon(h.neuron"+str(n)+"_tree[1](.5)._ref_v, None, sec=h.neuron"+str(n)+"_tree[1]))" #(.5)
            self.raster[-1].threshold = 0 #-10 #set threshold to a value of your choice
            self.raster[-1].record(self.t_vec[-1], self.id_vec[-1], n)
        # ----------------------------------------------------------------------
              

        
        if self.PRINTS :
            print "OK!"
    
        # RUN THE SIMULATION:

	
        #define the compartments whose activity will be recorded
        recsize=[]
        self.rec=[]

        if self.PLOT_ACTIVITY: 
	    for n in range(self.neurons_no) :
	        self.rec.append([])
                recsize.append(int(self.NSize[n] / self.electrodes))
		for i in range(self.electrodes) :
		    self.rec[n].append(recsize[n]*i)

        # Initialize the electrodes
 
	    for e in range(self.electrodes) :
	        for n in range(self.neurons_no) :
		    exec "self.vrec"+str(n)+str(e)+" = h.Vector()"
		    exec "self.trec"+str(n)+str(e)+" = h.Vector()"
		    exec "self.vrec"+str(n)+str(e)+".record(h.neuron"+str(n)+"_tree["+str(self.rec[n][e])+"](0.5)._ref_v)"
		    exec "self.trec"+str(n)+str(e)+".record(h._ref_t)"
    	
        # Finalize initialization
        h.finitialize(-60)
        h.dt = self.dt

        print "sim starting running!"
        # Run the simulation


	frames=len(self.input)
	pixels=len(self.input[0])	
	print "frames",len(self.input)
	#print "pix",len(self.input[0]),self.PIXEL_NO
	duration=self.runtime

	for i in range(frames):
	    for n in range(pixels) :
	        self.stimNet[n].ib = self.MIN_CURRENT+100*self.input[i][n]*(self.MAX_CURRENT-self.MIN_CURRENT)
	
	    neuron.run(duration)
	    duration+=self.runtime
	
	    print "Raster stuff:"
	    for i in range(len(self.t_vec)) :
		print "Spikes of neuron",str(i)+":", len(self.t_vec[i])
 	
	return list(self.t_vec)

    def plot(self) :     
         # Plot the recordings    
        if self.PLOT_ACTIVITY :
            plt.figure(1)

            for e in range(self.electrodes) :
                for n in range(self.neurons_no) :
                    exec "t"+str(n)+str(e)+" = np.array(self.trec"+str(n)+str(e)+")"
                    exec "v"+str(n)+str(e)+" = np.array(self.vrec"+str(n)+str(e)+")"
            for e in range(self.electrodes) :
                for n in range(self.neurons_no) :

                    if n == 0:
                       exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(e+1)+")"
                       exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='b')"
                       exec "plt.legend(loc=0)"
                    elif n == 1:
                       exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                       exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='r')"
                       exec "plt.legend(loc=0)"
                    elif n == 2:
                       exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                       exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='g')"
                       exec "plt.legend(loc=0)"
                    elif n == 3:
                       exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                       exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='y')"
                       exec "plt.legend(loc=0)"
                    elif n == 4:
                       exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(n*5+e+1)+")"
                       exec "plt.plot(t"+str(n)+str(e)+",v"+str(n)+str(e)+",label='Section "+str(self.rec[n][e])+"', c='k')"
                       exec "plt.legend(loc=0)"


            exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(self.electrodes+1)+")"
            # to change the size of the plot use: mp.figure(1, figsize=(20,20))
            # You can change the color and marker according to the pylab documentation
            a = plt.gca()
            a.set_xlim([0,self.t_stop])

            #idvec1temp = [x*(-1.0) for x in idvec1]

            for n in range(self.neurons_no) :
                if n == 0:
                    plt.scatter(self.t_vec[n], self.id_vec[n], c='b', marker='+')
                elif n == 1:
                    plt.scatter(self.t_vec[n], self.id_vec[n], c='r', marker='+')
                elif n == 2:
                    plt.scatter(self.t_vec[n], self.id_vec[n], c='g', marker='+')
                elif n == 3:
                    plt.scatter(self.t_vec[n], self.id_vec[n], c='y', marker='+')
                elif n == 4:
                    plt.scatter(self.t_vec[n], self.id_vec[n], c='k', marker='+')

    
            # FIRING RATE
            exec "plt.subplot("+str(self.neurons_no)+","+str(self.electrodes+1)+","+str(2*self.electrodes+2)+")"
            a = plt.gca()
            a.set_xlim([0,self.t_stop])

        # The following part is also used in experiment 2 where we need to calculate
        # and then compare the firing rate of the first neuron
        if self.PLOT_ACTIVITY:
            for neu in range(self.neurons_no) :
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
            #plt.savefig('screenshots/raster_plot.png') #this will save the plot - comment out if this is not needed
            #plt.draw() 
            plt.show() #this allows you to view the plot - comment out if this not needed


