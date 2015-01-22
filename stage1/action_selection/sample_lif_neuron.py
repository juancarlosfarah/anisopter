__author__ = 'Juan Carlos Farah, Panagiotis Almpouras'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk, panagiotis.almpouras12@imperial.ac.uk'

import numpy as np
import pylab

"""
Simulate a leaky integrate-and-fire (LIF) neuron using the
Euler method based on Professor Murray Shanahan's MatLab code.
http://www.doc.ic.ac.uk/~mpsha/CourseworkCode/LIFNeuronDemo.m
"""

# Constants
DT = 1          # Euler method step size in ms.
T_MIN = 0       # Start of observed period in ms.
T_MAX = 50      # Length of observed period in ms.
I = 20          # Base current.
R = 1           # Resistance.
TAU = 5         # Membrane time constant.
VR = -65        # Resting potential in mV.
PULSE = 30      # Dirac pulse.
THETA = -50     # Threshold in mV.

# Array of time intervals.
T = np.arange(T_MIN, T_MAX, DT, dtype=np.int32)

# Initial condition.
v = [T_MIN for i in range(T_MAX + 1)]
v[T_MIN] = VR

# Simulation
for t in T:
    v[t + 1] = v[t] + DT * ((VR - v[t] + R * I) / TAU)

    # Reset the neuron if it has spiked
    if v[t + 1] >= THETA:
        v[t] = PULSE
        v[t + 1] = VR

# Plot
pylab.plot(T, v[T_MIN:T_MAX])
pylab.xlabel('Time (ms)')
pylab.ylabel('Membrane Potential (v)')
pylab.title('Leaky Integrate-and-Fire Neuron')
pylab.show()