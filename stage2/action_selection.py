from brian2 import *
N = 4
taum = 10*ms
taupre = 20*ms
taupost = taupre
tauc = 1*second # from Izhikevich paper
tauDop = 20*ms #  Izhikevich paper 200ms
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms
F = 15*Hz
gmax = 1

dApre = 1 # 0.01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

sim_time = 1 * second

eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

input = PoissonGroup(N, rates=F)
neurons = NeuronGroup(N, eqs_neurons, threshold='v>vt', reset='v = vr')
S = Synapses(input, neurons,
             '''
                dApre/dt = -Apre / taupre : 1 
                dApost/dt = -Apost / taupost : 1 
                dDop/dt = -Dop / tauDop : 1 
                dc/dt = -c / tauc : 1
                dw/dt = c*Dop : 1
             ''',
             pre='''ge += w
                    Apre += dApre
                    c = c + Apost
                    w = clip(w, 0, gmax)''',
             post='''Apost += dApost
                     c = c + Apre
                     w = clip(w, 0, gmax)''',
             connect=True,
             )

S.w = 'rand() * gmax'
S.c = 'rand()'

mon = StateMonitor(S, ('w', 'Dop', 'c'), record=[0, 1])
s_mon = SpikeMonitor(neurons)
r_mon = PopulationRateMonitor(input)

#run(sim_time, report='text')

num_spikes = 0
for i in range(100):
    run(10*ms, report='text')
    if s_mon.num_spikes > num_spikes:
        num_spikes = s_mon.num_spikes
        if s_mon.i[-1] == 0:
            S.Dop += 0.5
    
subplot(321)
plot(S.w / gmax, '.k')
ylabel('Weight / gmax')
xlabel('Synapse index')
subplot(322)
hist(S.w / gmax, 20)
xlabel('Weight / gmax')
subplot(323)
plot(mon.t/second, mon.w.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(324)
plot(s_mon.t/second, s_mon.i, '.')
xlabel('Time (s)')
ylabel('Neuron number')
subplot(325)
plot(mon.t/second, mon.Dop[0])
ylabel('Dopamine')
subplot(326)
plot(mon.t/second, mon.c[0])
ylabel('c')
tight_layout()
show()
