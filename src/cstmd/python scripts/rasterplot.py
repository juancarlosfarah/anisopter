import neuron, matplotlib.pylab as mp

h = neuron.h
Section = h.Section

list_of_cells = [] #this list will contain all the cells

for i in range(50): #assuming you want 50 cells in the population.
   list_of_cells.append(Section()) #append the list with NEURON sections (equivalent to creating a cell)


# here you will have to specify cell parameters, network connectivity, import mechanisms, etc.


#create vectors that will record data for the raster plot:
tvec = h.Vector() #time
idvec = h.Vector() #cell number


recording_netcon = h.NetCon(list_of_cells[i].soma(.5)._ref_v, h.nil, sec=list_of_cells[i].soma(.5))
recording_netcon.threshold = -10 #set threshold to a value of your choice
recording_netcon.record(tvec, idvec, i)

h.load_file('stdrun.hoc')
h.tstop = 100 #simulation time in ms
h.run() #run the simulation

#once the simulation is finished, plot using matplotlib:

#you may add titles, axis labels, legends, etc. as well.  The how-to is in the pylab documentation
mp.figure(1) #to change the size of the plot use: mp.figure(1, figsize=(20,20))
mp.scatter(tvec, idvec, c='b', marker='+') #you can change the color and marker according to the pylab documentation
mp.savefig('screenshots/raster_plot.png') #this will save the plot - comment out if this is not needed

mp.draw() 
mp.show() #this allows you to view the plot - comment out if this not needed
mp.close()
