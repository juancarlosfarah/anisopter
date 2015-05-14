import numpy as np
import pickle
with open("results.pkl","rb") as ff :
    DATA = pickle.load(ff)

def score(T1,T2,T12) :
    res = []
    if len(T1) != len(T2) or len(T1) != len(T12) :
        print "Error! Bins not the same size!"
        exit()
    for t1,t2,t12 in zip(T1, T2, T12) :
        sc1 = abs(t1-t12)
        sc2 = abs(t2-t12)
        if sc1 > sc2 : res.append(sc1)
        else : res.append(sc2)
    return -np.mean(res)

def firing_rate(A, depth=50) :
    res = [0]*depth
    for i in range(depth,len(A)) :
        res.append(np.mean(A[i-depth:i])*1000)
    return res

K = []
scores = []
stds1 = []
stds2 = []
stds12 = []
m1 = []
m2 = []
m12 = []
SYN = []
for D1 in DATA :
    for D2 in D1 :
        K.append(D2['K'])
        #scores.append(D2['avgscore'])
        #scores.append(np.mean(D2['real_fr_1'])-np.mean(D2['real_fr_2']))        
        SYN.append(D2['SYN'])
        # Calculate firing rates
        fr1 = firing_rate(D2['real_fr_1'])
        fr2 = firing_rate(D2['real_fr_2'])
        fr12 = firing_rate(D2['real_fr_both'])
        scores.append(score(fr1, fr2, fr12))        
        stds1.append(np.std(fr1))
        stds2.append(np.std(fr2))
        stds12.append(np.std(fr12))
        m1.append(np.mean(fr1))
        m2.append(np.mean(fr2))
        m12.append(np.mean(fr12))

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm

fig = plt.figure(figsize=(25,10), frameon=False)

String = "Syns: "+str(DATA[6][3]['SYN']) + " K: " + str(DATA[6][3]['K'])

Bins1 = DATA[6][3]['real_fr_1']
FR1 = firing_rate(Bins1)
Bins2 = DATA[6][3]['real_fr_2']
FR2 = firing_rate(Bins2)
Bins12 = DATA[6][3]['real_fr_both']
FR12 = firing_rate(Bins12)

plt.subplot(251)
plt.plot(Bins1)

plt.subplot(256)
plt.plot(FR1,label="T1")
plt.plot(FR2,label="T2")
plt.plot(FR12,label="T12")
plt.legend()

ax = fig.add_subplot(2, 5, 7, projection='3d')
p = ax.plot_surface(K,SYN,scores, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
cb = fig.colorbar(p, shrink=0.5)
plt.xlabel("Score")

plt.subplot(258)
plt.scatter(K,SYN,c=m1,lw=0,s=80)
plt.colorbar()
plt.xlabel("mean 1")

plt.subplot(259)
plt.scatter(K,SYN,c=m2,lw=0,s=80)
plt.colorbar()
plt.xlabel("mean 2")

plt.subplot(2,5,10)
plt.scatter(K,SYN,c=m12,lw=0,s=80)
plt.colorbar()
plt.xlabel("mean 12")
plt.tight_layout()

plt.subplot(252)
plt.scatter(K,SYN,c=scores,lw=0,s=80)
plt.colorbar()
plt.xlabel("Score")

plt.subplot(253)
plt.scatter(K,SYN,c=stds1,lw=0,s=80)
plt.colorbar()
plt.xlabel("st. dev 1")

plt.subplot(254)
plt.scatter(K,SYN,c=stds2,lw=0,s=80)
plt.colorbar()
plt.xlabel("st. dev 2")

plt.subplot(255)
plt.scatter(K,SYN,c=stds12,lw=0,s=80)
plt.colorbar()
plt.xlabel("st. dev 12")
plt.tight_layout()
plt.show()
