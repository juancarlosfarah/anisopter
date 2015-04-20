# Action selection system
# Author: Christos Kaplanis


from brian2 import *

# Variables
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

sim_time = 10000 * ms
frame_length = 10 * ms

dopBoost = 0.5

# Neuron equations
eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

# Poisson input
input = PoissonGroup(N, rates=F)

# Action selection neurons
neurons = NeuronGroup(N, eqs_neurons, threshold='v>vt', reset='v = vr')

# Synapses
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
#S.w = 0.5 * gmax
S.w = 'rand() * gmax'
S.c = 'rand() * gmax'

# Monitors
mon = StateMonitor(S, ('w', 'Dop', 'c'), record=True)
w0_mon = StateMonitor(S, 'w', S[:,0])
w1_mon = StateMonitor(S, 'w', S[:,1])
w2_mon = StateMonitor(S, 'w', S[:,2])
w3_mon = StateMonitor(S, 'w', S[:,3])
s_mon = SpikeMonitor(neurons)
r_mon = PopulationRateMonitor(neurons)

#run(sim_time, report='text')

# Simulation loop
num_spikes = 0
for i in range(sim_time / frame_length):
    run(frame_length, report='text')
    if s_mon.num_spikes > num_spikes:
        if 0 in s_mon.i[range(num_spikes, s_mon.num_spikes)]:
            S.Dop += dopBoost
        num_spikes = s_mon.num_spikes

# Plots
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
plot(r_mon.t/second, r_mon.rate/Hz)
xlabel('Time/s')
ylabel('Firing rate / Hz')
tight_layout()
show()
