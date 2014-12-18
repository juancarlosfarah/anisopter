# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 13:05:29 2013, Telluride, USA
Creates random targets inside the borders of area I
@author: Zafeirios Fountas - Imperial College London (zfountas@imperial.ac.uk)
"""
import pylab
import matplotlib.pyplot as plt
from random import *

# PARAMETERS
radius = 3.0
soma_x = 0
soma_y = 0
soma_z = 0
max_length = 1000
output_name = "my_tree_from_python"
scale = 100.5       # Used by trees library for 'quaddiameter_tree' function
                    #from help: scale of diameter of root {DEFAULT: 0.5}
offset = 10.0       #from help: added base diameter {DEFAULT: 0.5}
points = 2000

# INITIALIZATION
# Set the boarders of area I
border_xL = []
border_xL.append(-700.0)
border_xL.append(-625.0)
border_xL.append(-675.0)
border_xL.append(-750.0)
border_xL.append(-750.0)
border_xL.append(-700.0)
border_xL.append(-700.0)
border_xL.append(-837.5)
border_xL.append(-900.0)
border_xL.append(-1100.0)
border_xL.append(-1200.0)
border_xL.append(-1050.0)
border_xL.append(-700.0)

border_yL = []
border_yL.append(150.0)
border_yL.append(125.0)
border_yL.append(62.5)
border_yL.append(-125.0)
border_yL.append(-175.0)
border_yL.append(-225.0)
border_yL.append(-412.5)
border_yL.append(-675.0)
border_yL.append(-725.0)
border_yL.append(-625.0)
border_yL.append(-300.0)
border_yL.append(-25.0)
border_yL.append(150.0)

for a in range(len(border_xL)):
    border_xL[a] = border_xL[a] - 530

for a in range(len(border_yL)):
    border_yL[a] = border_yL[a] + 300

# Check if a randomly generated 2D point is inside the polygon defined by the border_xL, yL
def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

# Creates a matlab/octave file which can be used to create the morphology of the CSTMD1.
# If plots != 0, the function also prints the intersection points of the neuron's dendrite.
def create_matlab_code(neur_no, plots):
    myfile = open("py_tree_script.m", "w")
    myfile.write('cd ../trees\n\n')
    myfile.write('start_trees\n\n')
    myfile.write('X=zeros('+str(points)+',1);\n')
    myfile.write('Y=zeros('+str(points)+',1);\n')
    myfile.write('Z=zeros('+str(points)+',1);\n\n')
    
    for n in range(neur_no) :
        targets = []
    
        soma_z = n * 25
        output_name = "neuron" + str(n)
        
        myfile.write('X(1) = '+str(-200) +'; Y(1) = '+str(260)+'; Z(1) = '+str(soma_z)+';\n')
        myfile.write('X(2) = '+str(-400) +'; Y(2) = '+str(300)+'; Z(2) = '+str(soma_z)+';\n')
        myfile.write('X(3) = '+str(-450) +'; Y(3) = '+str(290)+'; Z(3) = '+str(soma_z)+';\n')
        myfile.write('X(4) = '+str(-680) +'; Y(4) = '+str(260)+'; Z(4) = '+str(soma_z)+';\n')
        myfile.write('X(5) = '+str(-890) +'; Y(5) = '+str(200)+'; Z(5) = '+str(soma_z)+';\n')
        myfile.write('X(6) = '+str(-980) +'; Y(6) = '+str(130)+'; Z(6) = '+str(soma_z)+';\n')
        myfile.write('X(7) = '+str(-1030)+'; Y(7) = '+str(140)+'; Z(7) = '+str(soma_z)+';\n')
        myfile.write('X(8) = '+str(-1090)+'; Y(8) = '+str(20) +'; Z(8) = '+str(soma_z)+';\n\n')
        
        targets.append((-200,260))
        targets.append((-400, 300))
        targets.append((-450,290))
        targets.append((-680, 260))
        targets.append((-890, 200))
        targets.append((-980, 130))
        targets.append((-1030, 140))
        targets.append((-1090, 20))
        
        while len(targets) < points :
            x = uniform(-1750.0, -1000.0)
            y = uniform(-450.0, 460.0)
            z = uniform(-20.0+soma_z, 20.0+soma_z)
            if point_inside_polygon(x, y, zip(border_xL,border_yL)):
                targets.append((x,y))
                myfile.write('X('+str(len(targets))+') = '+str(x)+ '; Y('+str(len(targets))+') = '+str( y)+ '; Z('+str(len(targets))+') = '+str(z)+';\n') 
    
        myfile.write("\nzaf_tree = MST_tree (1, ["+str(soma_x)+";X], ["+str(soma_y)+";Y], ["+str(soma_z)+";Z], .5, "+str(max_length)+", [], [], 'none');\n")
        myfile.write("quaddiameter_tree (zaf_tree, "+str(scale)+", "+str(offset)+");\n")

        myfile.write("swc_tree(zaf_tree,\"" + output_name + ".swc\")\n")
        myfile.write("neuron_tree(zaf_tree,\"" + output_name + ".hoc\")\n")
        myfile.write("\n")
    
    myfile.close()
    
    if plots :
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        circ = plt.Circle((0, 0), radius=10.0, color='g')
        ax.add_patch(circ)
    
        plt.scatter(border_xL, border_yL)
        plt.plot(border_xL, border_yL)
        ax.add_patch(circ)
        
        for a in targets :
            circ = plt.Circle(a, radius=radius, color='b')
            ax.add_patch(circ)
        
        plt.show()









