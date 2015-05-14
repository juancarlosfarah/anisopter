# Action selection system
# Author: Christos Kaplanis

import math
import os
import numpy as np
import pickle

from animation.target_animation import Animation
from brian2 import *

class ActionSelection(object):
    def __init__(self,
                 N=4,
                 taum=10*ms,
                 taupre=20*ms,
                 taupost=20*ms,
                 tauc=20*ms,
                 tauDop=20*ms,
                 Ee=0*mV,
                 vt=-54*mV,
                 vr=-60*mV,
                 El=-74*mV,
                 taue=5*ms,
                 F=15*Hz,
                 gmax=1,
                 dApre=1,
                 sim_time=100.0*ms,
                 frame_length=10.0*ms,
                 dopBoost=0.5,
                 reward_distance=40,
                 fromAnim=True,
                 SPEED_FACTOR=2*second,
                 dragonfly_start=[300, 300, 0.0],
                 description="",
                 output_dir="output.avi",
                 animation = None,
                 total_anim_frames = None,
                 pattern_input=None,
                 pattern_duration=None,
                 animation_id=None,
                 pattern_recognition_id=None,
                 saved_weights = None,
                 training = True):
        
        # Neuron Variables
        self.N = N
        self.taum = taum
        self.taupre = taupre
        self.taupost = taupost
        self.tauc = tauc # Izhikevich paper 1s
        self.tauDop = tauDop #  Izhikevich paper 200ms
        self.Ee = Ee
        self.vt = vt
        self.vr = vr
        self.El = El
        self.taue = taue
        self.F = F
        self.gmax = gmax

        self.dApre = dApre # 0.01
        self.dApost = -dApre * taupre / taupost *1.05 #* 1.05
        self.dApost *= gmax
        self.dApre *= gmax

        # Simulation variables
        self.sim_time = sim_time
        self.frame_length = frame_length

        # Reward variables
        self.dopBoost = dopBoost
        self.reward_distance = reward_distance

        # Animation variables
        self.fromAnim = fromAnim
        self.SPEED_FACTOR = SPEED_FACTOR
        self.dragonfly_start = dragonfly_start
        
        # Description
        self.description = description

        # Video output directory
        self.output_dir = output_dir

        # Input
        self.pattern_input = pattern_input
        if pattern_duration is not None:
            print "Selecting minimum duration of simulation."
            print sim_time, pattern_duration
            print sim_time/ms
            self.sim_time = min(sim_time/ms, pattern_duration)*ms
        self.animation = animation
        self.animation_id = animation_id
        self.pattern_recognition_id = pattern_recognition_id
        self.saved_weights = saved_weights
        self.training = training

        if total_anim_frames is None:
            self.total_anim_frames = int(sim_time / frame_length)

    def run(self, show_plots=True):
        
        # Neuron Variables
        N = self.N
        taum = self.taum
        taupre = self.taupre
        taupost = self.taupost
        tauc = self.tauc # Izhikevich paper 1s
        tauDop = self.tauDop #  Izhikevich paper 200ms
        Ee = self.Ee
        vt = self.vt
        vr = self.vr
        El = self.El
        taue = self.taue
        F = self.F
        gmax = self.gmax

        dApre = self.dApre 
        dApost = self.dApost 

        # Simulation variables
        sim_time = self.sim_time
        frame_length = self.frame_length

        # Reward variables
        dopBoost = self.dopBoost
        reward_distance = self.reward_distance

        # Animation variables
        fromAnim = self.fromAnim
        SPEED_FACTOR = self.SPEED_FACTOR
        dragonfly_start = self.dragonfly_start

        # Neuron equations.
        eqs_neurons = '''
       	dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
       	dge/dt = -ge / taue : 1
       	'''

        # Poisson input.
        if self.pattern_input is None:
            input = PoissonGroup(N, rates=F)
        else:
            # Pattern recognition input
            print self.pattern_input

            pattern = self.pattern_input
            num_input = len(pattern)

            input_indices = []
            input_times = []
            for i in range(num_input):
                for j in range(len(pattern[i])):
                    input_indices.append(i)
                    input_times.append(pattern[i][j])

            combined = zip(input_times, input_indices)

            sort_combined = [list(t) for t in zip(*sorted(combined))]

            input_times = np.asarray(sort_combined[0])*ms
            input_indices = np.asarray(sort_combined[1])

            print input_times
            print input_indices

            input = SpikeGeneratorGroup(num_input, input_indices, input_times)

        # Action selection neurons.
        neurons = NeuronGroup(N, eqs_neurons, threshold='v>vt', reset='v=vr')
        
        # Synapses.
        S = Synapses(input, neurons,
                     '''
                     dApre/dt = -Apre / taupre : 1 
                     dApost/dt = -Apost / taupost : 1 
                     dDop/dt = -Dop / tauDop : 1 
                     dc/dt = -c / tauc : 1
                     dw/dt = c*Dop : 1
	       	     ''',
                     pre='''w = clip(w, 0, gmax)
                     ge += w
                     Apre += dApre
                     c = c + Apost''',
                     post='''w = clip(w, 0, gmax)
                     Apost += dApost
                     c = c + Apre''',
                     connect=True,
                    )

        # Set up weights
        self.synapses = S
        if self.saved_weights is None:
            S.w = 'rand() * gmax'
        else:
            S.w = self.saved_weights
        if self.training is False:
            dopBoost = 0.0
            self.dopBoost = dopBoost
        S.c = 'rand() * gmax'

        # Subgroups
        neuron0=neurons[0:1]
        neuron1=neurons[1:2]
        neuron2=neurons[2:3]
        neuron3=neurons[3:4]

        # Monitors
        mon = StateMonitor(S, ('w', 'Dop', 'c'), record=True)
        w0_mon = StateMonitor(S, 'w', S[:,0])
        w1_mon = StateMonitor(S, 'w', S[:,1])
        w2_mon = StateMonitor(S, 'w', S[:,2])
        w3_mon = StateMonitor(S, 'w', S[:,3])
        s_mon = SpikeMonitor(neurons)
        r0_mon = PopulationRateMonitor(neuron0)
        r1_mon = PopulationRateMonitor(neuron1)
        r2_mon = PopulationRateMonitor(neuron2)
        r3_mon = PopulationRateMonitor(neuron3)

        #run(sim_time, report='text')

        rate0 = []
        rate1 = []
        rate2 = []
        rate3 = []

        rates_t = range(0, sim_time/ms, frame_length/ms)
        rates_t = [x / 1000.0 for x in rates_t]

        # Animation
        dragon_path = [dragonfly_start]
        if self.animation is None:
            self.animation = Animation()
            self.animation.add_target(2, start=[250,0], velocity=[1,1], size=5, v=4)
        else:
            pass


        # Simulation loop
        num_spikes = 0
        rate_window = int(frame_length / (0.1 * ms))
        for i in range(sim_time / frame_length):
            run(frame_length, report='text')
            
            mean0 = np.mean(r0_mon.rate[-rate_window:])
            rate0.append(mean0)
            mean1 = np.mean(r1_mon.rate[-rate_window:])
            rate1.append(mean1)
            mean2 = np.mean(r2_mon.rate[-rate_window:])
            rate2.append(mean2)
            mean3 = np.mean(r3_mon.rate[-rate_window:])
            rate3.append(mean3)

            ##### Dragonfly movement
            up = mean0
            down = mean2
            left = mean1
            right = mean3
            vy = (up - down) * SPEED_FACTOR
            vx = (right - left) * SPEED_FACTOR
            x = dragon_path[-1][0] + vx / 10.0
            y = dragon_path[-1][1] + vy / 10.0
            t = 1.0 * i / (sim_time / frame_length)
            dragon_path.append([x, y, t])

            # Find distance of closest target
            norm_time = i / (sim_time / frame_length)
            targets = self.animation.get_targets_positions(norm_time)
            min_dist = np.sqrt((dragon_path[-1][0] - targets[0][0])**2 + (dragon_path[-1][1] - targets[0][1])**2)
            for i in range(1, len(targets)):
                dist = np.sqrt((dragon_path[-1][0] - targets[i][0])**2 + (dragon_path[-1][1] - targets[i][1])**2)
                if dist < min_dist:
                    min_dist = dist

            # Apply dopamine if dragonfly close to a target
            if fromAnim:
                if min_dist < reward_distance:
                    S.Dop += dopBoost

            else:
                if s_mon.num_spikes > num_spikes:
                    if 0 in s_mon.i[range(num_spikes, s_mon.num_spikes)]:
                        S.Dop += dopBoost
                        num_spikes = s_mon.num_spikes

        # Add dragon path.
        self.animation.add_dragonfly(dragon_path)

        # Save rates
        self.rates = []
        (self.rates).append(rate0)
        (self.rates).append(rate1)
        (self.rates).append(rate2)
        (self.rates).append(rate3)
        
        self.rates_t = rates_t


        # Save monitors
        self.synapse_mon = mon
        self.w0_mon = w0_mon
        self.w1_mon = w1_mon
        self.w2_mon = w2_mon
        self.w3_mon = w3_mon
        self.spike_mon = s_mon
        self.r0_mon = r0_mon
        self.r1_mon = r1_mon
        self.r2_mon = r2_mon
        self.r3_mon = r3_mon

        # Save weights
        self.synapses = S
        self.saved_weights = np.asarray(self.synapses.w[:])

        print self.saved_weights

    def save_plots(self, graph_dir):
        # Plots
        figure(1)
        plot(self.synapses.w / self.gmax, '.k')
        title('Weights of synapses')
        ylabel('Weight / gmax')
        xlabel('Synapse index')
        savefig(graph_dir+'/1.png')
        figure(2)
        plot(self.w0_mon.t/second, self.w0_mon.w.T)
        title('Weights of synapses to Up Neuron')
        xlabel('Time (s)')
        ylabel('Weight / gmax')
        savefig(graph_dir+'/2.png')
        figure(3)
        plot(self.w1_mon.t/second, self.w1_mon.w.T)
        title('Weights of synapses to Left Neuron')
        xlabel('Time (s)')
        ylabel('Weight / gmax')
        savefig(graph_dir+'/3.png')
        figure(4)
        plot(self.w2_mon.t/second, self.w2_mon.w.T)
        title('Weights of synapses to Down Neuron')
        xlabel('Time (s)')
        ylabel('Weight / gmax')
        savefig(graph_dir+'/4.png')
        figure(5)
        plot(self.w3_mon.t/second, self.w3_mon.w.T)
        title('Weights of synapses to Right Neuron')
        xlabel('Time (s)')
        ylabel('Weight / gmax')
        savefig(graph_dir+'/5.png')
        figure(6)
        plot(self.spike_mon.t/second, self.spike_mon.i, '.')
        title('Raster plot')
        xlabel('Time (s)')
        ylabel('Neuron number')
        savefig(graph_dir+'/6.png')
        figure(7)
        plot(self.synapse_mon.t/second, self.synapse_mon.Dop[0])
        title('Dopamine level')
        ylabel('Dopamine')
        savefig(graph_dir+'/7.png')
        figure(8)
        title('Eligibility trace of Up Neuron')
        plot(self.synapse_mon.t/second, self.synapse_mon.c[0])
        ylabel('c')
        savefig(graph_dir+'/8.png')
        
        # Firing rates
        figure(9)
        plot(self.rates_t, self.rates[0]/Hz)
        title('Up Neuron firing rate')
        xlabel('Time/s')
        ylabel('Firing rate / Hz')
        savefig(graph_dir+'/9.png')
        figure(10)
        plot(self.rates_t, self.rates[1]/Hz)
        title('Left Neuron firing rate')
        xlabel('Time/s')
        ylabel('Firing rate / Hz')
        savefig(graph_dir+'/10.png')
        figure(11)
        plot(self.rates_t, self.rates[2]/Hz)
        title('Down Neuron firing rate')
        xlabel('Time/s')
        ylabel('Firing rate / Hz')
        savefig(graph_dir+'/11.png')
        figure(12)
        plot(self.rates_t, self.rates[3]/Hz)
        title('Right Neuron firing rate')
        xlabel('Time/s')
        ylabel('Firing rate / Hz')
        savefig(graph_dir+'/12.png')

    def run_animation(self, _id):
        """
        Runs animation for target selection.
        :param _id:
        :return: None.
        """
        save_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "assets",
                                                 "action_selection",
                                                 _id))
        self.animation.run(save_path, 10, self.total_anim_frames)


if __name__ == "__main__":
    action = ActionSelection()
    action.run()
    action.save_plots("")
    action.animation.run("test1.avi", 10, 10)
    show()
