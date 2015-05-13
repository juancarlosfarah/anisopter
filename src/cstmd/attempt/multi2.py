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


def run(K,Na,SYN,DATA_NAME):
    call(["python", "example.py", "-file", "frame_target_strong.pkl", "-K", str(K), "-Na", str(Na), "-SYN", str(SYN),"d",DATA_NAME])
    with open(DATA_NAME, 'rb') as my_file :
        data1 = pickle.load(my_file)

    call(["python", "example.py", "-file", "frame_target_weak.pkl", "-K", str(K), "-Na", str(Na), "-SYN", str(SYN),"d",DATA_NAME])
    with open(DATA_NAME, 'rb') as my_file :
        data2 = pickle.load(my_file)

    call(["python", "example.py", "-file", "frame_target_both.pkl", "-K", str(K), "-Na", str(Na), "-SYN", str(SYN),"d",DATA_NAME])
    with open(DATA_NAME, 'rb') as my_file :
        databoth = pickle.load(my_file)


    real_fr_1 = real_firing_rates(data1)
    real_fr_2 = real_firing_rates(data2)
    real_fr_both = real_firing_rates(databoth)

    scorelen=min(len(real_fr_1),len(real_fr_2),len(real_fr_both))
    score=[]

    for i in range(scorelen):
        dist1=real_fr_both[i]-real_fr_1[i]
        dist2=real_fr_both[i]-real_fr_2[i]
        score.append(min(dist1,dist2))
    avgscore=np.mean(score)

    """
    fig = plt.figure()
    graph = fig.add_subplot(111)
    graph.set_title("Firing rates of CSTMD1, Avg Score= "+str(avgscore))
    graph.set_xlabel("Time (10ms)")
    graph.set_ylabel("Firing rate (Hz)")

    target1, = plt.plot(real_fr_1, c='r', lw=2.0, label = "Target 1")
    target2, = plt.plot(real_fr_2, c='b', lw=2.0, label = "Target 2")
    targetboth, = plt.plot(real_fr_both, c='g', lw=2.0, label = "Both Targets")

    #plt.title("FR")
    plt.legend([target1, target2,targetboth])
    fig.savefig("multi.png")
    plt.show()
    """

    returned_data = dict()
    returned_data['K'] = K
    returned_data['Na'] = Na
    returned_data['SYN'] = SYN
    returned_data['avgscore'] = avgscore
    returned_data['real_fr_1'] = real_fr_1
    returned_data['real_fr_2'] = real_fr_2
    returned_data['real_fr_both'] = real_fr_both

    return returned_data

#Already have default values
K=0.06
Na=0.48
SYN = 500


"""
from sys import argv
if len(argv) != 3 :
    print "You need to specify starting and ending K point (normally between 0.01 - 0.1)"
    exit()
else :
    START_K = float(argv[1])
    END_K = float(argv[2])
"""
START_K = 0.01
END_K = 0.1


FILENAME = "results.pkl"

import os.path
if os.path.isfile(FILENAME)  :
    with open(FILENAME, 'rb') as my_file :
        SAVED_DATA = pickle.load(my_file)
else :
    SAVED_DATA = []


results=[]

def myFunction(k):
    #s = 500
    runs_here = []
    for s in range(0, 3000, 100) : # Synapses
        fl="{:.2f}".format(k) 
        res = run(k, Na, s, DATA_NAME="data_"+fl+".pkl")
        print s*k/(10*30)" % COMPLETE"
        runs_here.append(res)
    return runs_here

import multiprocessing as mp
myPool = mp.Pool(7)
results = myPool.map(myFunction, np.arange(START_K, END_K, 0.01))

# It's the same as this results = [myFunction(k) for k in np.arange(...) ] in parallel!

# FOR ONE THREAD!
# results=[]
# for k in np.arange(START_K, END_K, 0.01) : # K level
#    s = 500
#    #for s in range(0, 3000, 250) : # Synapses
#    results.append(run(k,Na,s))


SAVED_DATA = SAVED_DATA + results

with open(FILENAME, 'wb') as my_file :
    pickle.dump(results, my_file)


#for i in range(len(data)):
#    print data[i]




