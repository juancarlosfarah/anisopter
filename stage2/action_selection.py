from brian2 import *

N = 100 # number of action selection neurons
M = 100 # number of fake pattern recognition neurons

tau = 10 * ms

eqs = '''dv/dt = (2-v)/tau : 1'''

G = NeuronGroup(M, eqs, threshold = 'v>0.8', reset = 'v=0')
H = NeuronGroup(N, eqs, threshold = 'v>0.8', reset = 'v=0')

G.v = 'rand()'

S = Synapses(G, H, 'w : 1', 

M = SpikeMonitor(G)
State = StateMonitor(G, 'v', record=0)

run(100*ms)

subplot(2,1,1)
plot(M.t/ms, M.i, '.')
subplot(2,1,2)
plot(State.t/ms, State.v[0])
show()
