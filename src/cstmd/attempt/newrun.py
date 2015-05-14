from subprocess import call
import numpy as np 
import pickle
import matplotlib.pyplot as plt

call(["python", "example.py", "-file", "64x64_no_input_200.pkl"])
with open("dat.pkl", 'rb') as my_file :
    data0 = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_strong_200.pkl"])
with open("dat.pkl", 'rb') as my_file :
    data_strong = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_weak_closer_200.pkl"])
with open("dat.pkl", 'rb') as my_file :
    data_weak = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_diag_200.pkl"])
with open("dat.pkl", 'rb') as my_file :
    data_diag = pickle.load(my_file)

call(["python", "example.py", "-file", "64x64_3_targets_200.pkl"])
with open("dat.pkl", 'rb') as my_file :
    data_both = pickle.load(my_file)


real_fr_0 = data0
real_fr_strong = data_strong
real_fr_weak = data_weak
real_fr_diag = data_diag
real_fr_3 = data_both



fig = plt.figure()
graph = fig.add_subplot(111)
graph.set_title("Firing rates of CSTMD1 given various inputs")
graph.set_xlabel("Time (10ms)")
graph.set_ylabel("Firing rate (Hz)")

no_target, = plt.plot(real_fr_0, c='r', lw=2.0, label = "No targets")
strong_target, = plt.plot(real_fr_strong, c='b', lw=2.0, label = "Central target")

weak_target, = plt.plot(real_fr_weak, c='g', lw=2.0, label = "Peripheral target")
diag_target, = plt.plot(real_fr_diag, c='m', lw=2.0, label = "Diagonal target")
three_targets, = plt.plot(real_fr_3, c='k', lw=2.0, label = "All targets")

#plt.title("FR")
plt.legend([no_target, strong_target,weak_target, diag_target, three_targets])
fig.savefig("letssee.png")
plt.show()







