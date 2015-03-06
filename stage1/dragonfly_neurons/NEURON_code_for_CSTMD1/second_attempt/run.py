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

K = 1
Na = 0.48
#for K in np.arange(0.01, 0.1, 0.01) :
K = 0.05

call(["python", "example.py", "-file", "frame_target1.pkl", "-K", str(K), "-Na", str(Na)])
with open("data.pkl", 'rb') as my_file :
    data1 = pickle.load(my_file)
call(["python", "example.py", "-file", "frame_target2.pkl", "-K", str(K), "-Na", str(Na)])
with open("data.pkl", 'rb') as my_file :
    data2 = pickle.load(my_file)
call(["python", "example.py", "-file", "frame_target12.pkl", "-K", str(K), "-Na", str(Na)])
with open("data.pkl", 'rb') as my_file :
    data12 = pickle.load(my_file)

call(["python", "example.py", "-file", "frame_targets.pkl", "-K", str(K), "-Na", str(Na)])
with open("data.pkl", 'rb') as my_file :
    data_test = pickle.load(my_file)

#FRTEST = firing_rates(bin_data(data_test))
#FR1 = firing_rates(bin_data(data1))
#FR2 = firing_rates(bin_data(data2))
#FR12 = firing_rates(bin_data(data12))

#real_fr_test = real_firing_rates(data_test)
real_fr_1 = real_firing_rates(data1)
real_fr_2 = real_firing_rates(data2)
real_fr_12 = real_firing_rates(data12)


print data1

plt.subplot(2,1,1)
#plt.plot(bin_data(data1), c='b', lw=2.0)
#plt.plot(bin_data(data2), c='g', lw=2.0)
#plt.plot(bin_data(data12), c='k', lw=2.0)
plt.title("binned  data")

plt.subplot(2,1,2)
plt.plot(real_fr_1, c='b', lw=2.0)
plt.plot(real_fr_2, c='g', lw=2.0)
plt.plot(real_fr_12, c='k', lw=2.0)
#plt.plot(FR1, c='b', lw=2.0)
#plt.plot(FR2, c='g', lw=2.0)
#plt.plot(FR12, c='k', lw=2.0)
#plt.plot(real_fr_test, c='k', lw=2.0)
plt.title("FR")

plt.savefig("letssee.png")
plt.show()







