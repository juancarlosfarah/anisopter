from subprocess import call
import numpy as np 
import pickle
import matplotlib.pyplot as plt

MAX_TIME = 500 # ??????!

def bin_data(data) :
    binned = [0]*MAX_TIME
    for d in data :
        binned[int(d)] += 1
    return binned

length = 50

def firing_rates(binned_data) :
    FR = []
    buf = [0]*length
    for t in range(len(binned_data)) :
        buf[t%length] = binned_data[t]
        FR.append(np.mean(buf[:min(t,length-1)])*1000.0)
    return FR

def real_firing_rates(data) :
    fr = []
    for i in range(len(data)-4) :
        fr.append(4000.0 / (data[i+4] - data[i]))
    return fr


call(["python", "example.py", "-file", "64x64_no_input_200.pkl"])
with open("data.pkl", 'rb') as my_file :
    data0 = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_strong_200.pkl"])
with open("data.pkl", 'rb') as my_file :
    data_strong = pickle.load(my_file)
"""
call(["python", "example.py", "-file", "64x64_weak_closer_200.pkl"])
with open("data.pkl", 'rb') as my_file :
    data_weak = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_diag_200.pkl"])
with open("data.pkl", 'rb') as my_file :
    data_diag = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_3_targets_200.pkl"])
with open("data.pkl", 'rb') as my_file :
    data_both = pickle.load(my_file)
"""

real_fr_0 = real_firing_rates(data0)
real_fr_strong = real_firing_rates(data_strong)
"""
real_fr_weak = real_firing_rates(data_weak)
real_fr_diag = real_firing_rates(data_diag)
real_fr_3 = real_firing_rates(data_both)
"""
#plt.subplot(2,1,1)
#plt.plot(bin_data(data1), c='b', lw=2.0)
#plt.plot(bin_data(data2), c='g', lw=2.0)
#plt.plot(bin_data(data12), c='k', lw=2.0)
#plt.title("binned  data")

#plt.subplot(2,1,1)
fig = plt.figure()
graph = fig.add_subplot(111)
graph.set_title("Firing rates of CSTMD1 given various inputs")
graph.set_xlabel("Time (10ms)")
graph.set_ylabel("Firing rate (Hz)")

no_target, = plt.plot(real_fr_0, c='r', lw=2.0, label = "No targets")
strong_target, = plt.plot(real_fr_strong, c='b', lw=2.0, label = "Central target")
"""
weak_target, = plt.plot(real_fr_weak, c='g', lw=2.0, label = "Peripheral target")
diag_target, = plt.plot(real_fr_diag, c='m', lw=2.0, label = "Diagonal target")
three_targets, = plt.plot(real_fr_3, c='k', lw=2.0, label = "All targets")
"""
#plt.title("FR")
plt.legend([no_target, strong_target])#, weak_target, diag_target, three_targets])
fig.savefig("letssee.png")
plt.show()







