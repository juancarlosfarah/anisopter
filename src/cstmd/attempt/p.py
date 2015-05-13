import numpy as np
import pickle
with open("results.pkl","rb") as ff :
    DATA = pickle.load(ff)
K = []
scores = []
SYN = []
for D1 in DATA :
    for D2 in D1 :
        K.append(D2['K'])
        #scores.append(D2['avgscore'])
        SYN.append(D2['SYN'])
        scores.append(np.mean(D2['real_fr_both'])-np.mean(D2['real_fr_2']))        
from matplotlib import pyplot as plt
plt.scatter(K,SYN,c=scores,lw=0,s=80)
plt.colorbar()
plt.show()
