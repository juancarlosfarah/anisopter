# Action selection system
# Author: Christos Kaplanis


import math
import numpy as np

from animation.target_animation import Animation
from brian2 import *


# Variables.
N = 4
taum = 10*ms
taupre = 20*ms
taupost = taupre
tauc = 20*ms # Izhikevich paper 1s
tauDop = 20*ms #  Izhikevich paper 200ms
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms
F = 15*Hz
gmax = 1

dApre = 1 # 0.01
dApost = -dApre * taupre / taupost *1.05 #* 1.05
dApost *= gmax
dApre *= gmax

sim_time = 100 * ms
frame_length = 10 * ms

dopBoost = 0.5

fromAnim = False

SPEED_FACTOR = 2 * second

# Neuron equations.
eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

# Poisson input.
input = PoissonGroup(N, rates=F)

# Action selection neurons.
neurons = NeuronGroup(N, eqs_neurons, threshold='v>vt', reset='v = vr')

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

# S.w = 0.5 * gmax.
S.w = 'rand() * gmax'
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

rates_t = range(0, sim_time/(1*ms), frame_length/(1*ms))


######################### CONSTANTS TO CHANGE!
dragon_path = [[300, 300, 0.0]]
##########################

# Animation
test = Animation()
test.add_target(2, start=[250,0], velocity=[1,1], size=5, v=4)

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

    ##### Dragonfly stuff
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

    #####


    if fromAnim:
        # TO-DO
        pass

    else:
        if s_mon.num_spikes > num_spikes:
            if 0 in s_mon.i[range(num_spikes, s_mon.num_spikes)]:
                S.Dop += dopBoost
            num_spikes = s_mon.num_spikes


######## Animation stuff
test.add_dragonfly(dragon_path)
test.run("test.avi", 10, 10)
print dragon_path
########

# Plots
figure(1)
subplot(331)
plot(S.w / gmax, '.k')
ylabel('Weight / gmax')
xlabel('Synapse index')
subplot(332)
plot(w0_mon.t/second, w0_mon.w.T)
title('Synapses to Neuron 0')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(333)
plot(w1_mon.t/second, w1_mon.w.T)
title('Synapses to Neuron 1')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(334)
plot(w2_mon.t/second, w2_mon.w.T)
title('Synapses to Neuron 2')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(335)
plot(w3_mon.t/second, w3_mon.w.T)
title('Synapses to Neuron 3')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(336)
plot(s_mon.t/second, s_mon.i, '.')
xlabel('Time (s)')
ylabel('Neuron number')
subplot(337)
plot(mon.t/second, mon.Dop[0])
ylabel('Dopamine')
subplot(338)
plot(mon.t/second, mon.c[0])
ylabel('c')
subplot(339)
plot(r0_mon.t/second, r0_mon.rate/Hz)
xlabel('Time/s')
ylabel('Firing rate / Hz')
tight_layout()

figure(2)
subplot(221)
plot(rates_t, rate0/Hz)
title('Neuron 0 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')
subplot(222)
plot(rates_t, rate1/Hz)
title('Neuron 1 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')
subplot(223)
plot(rates_t, rate2/Hz)
title('Neuron 2 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')
subplot(224)
plot(rates_t, rate3/Hz)
title('Neuron 3 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')

show()
