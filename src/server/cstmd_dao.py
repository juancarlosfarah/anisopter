__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import os
import pymongo
import shutil
from cstmd.cstmd import Cstmd
import pickle
import mpld3
import matplotlib.pyplot as plt, mpld3
class CstmdDao:

    def __init__(self, database):
        self.db = database
        self.collection = self.db.cstmd
        self.spikes = self.db.spikes

    def save(self, cstmd, estmd_id, animation_id):
        """
        Saves the CSTMD1 simulation to the database.
        :return: _id of simulation inserted.
        """

        # General simulation data.
        sim = {
            'description': cstmd.description,
            'num_neurons': cstmd.num_neurons,
            'num_synapses': cstmd.num_synapses,
            'num_electrodes': cstmd.num_electrodes,
            'num_efferents': cstmd.num_neurons * cstmd.num_electrodes,
            'max_current': cstmd.max_current,
            'min_current': cstmd.min_current,
            'min_weight': cstmd.min_weight,
            'max_weight': cstmd.max_weight,
            'num_pixels': cstmd.num_pixels,
            'duration': cstmd.spike_trains.shape[1],
            'duration_per_frame': cstmd.duration,
            'potassium': cstmd.potassium,
            'sodium': cstmd.sodium,
            'synaptic_distance': cstmd.synaptic_distance,
            'animation_id': animation_id,
            'estmd_id': estmd_id,
            'num_plots': cstmd.num_plots
        }

        # Save general data.
        _id = self.collection.insert(sim)

        # Spike collection.
        collection = self.db.spikes

        # Save spikes.
        for dt in range(cstmd.spike_trains.shape[1]):
            obj = {
                "sample_id": _id,
                "spikes": cstmd.spike_trains[:, dt].tolist()
            }
            collection.insert(obj)

        return _id

    def remove(self, _id):
        """
        Removes one simulation from the database. Deletes its related files.
        :param _id: ID of simulation to remove.
        :return: None.
        """
        self.collection.remove({"_id": ObjectId(_id)})
        self.spikes.remove({"sample_id": ObjectId(_id)})

        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "assets",
                                            "cstmd"))
        # Remove Folder.
        folder = str(_id)
        file_path = "{path}/{folder}".format(path=path, folder=folder)
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

        return

    def get_simulations(self, num_simulations):
        """
        Fetches a given number of simulations from the database.
        :param num_simulations: Number of simulations to fetch.
        :return: Array of simulations.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_simulations)
        simulations = []

        for simulation in cursor:
            if "description" not in simulation:
                simulation['description'] = "Description"
            simulations.append(
                {
                    '_id': simulation['_id'],
                    'date': simulation['_id'].generation_time,
                    'description': simulation['description'],
                    'num_neurons': simulation['num_neurons'],
                    'num_efferents': simulation['num_efferents'],
                    'num_synapses': simulation['num_synapses'],
                    'num_electrodes': simulation['num_electrodes'],
                    'max_current': simulation['max_current'],
                    'min_current': simulation['min_current'],
                    'min_weight': simulation['min_weight'],
                    'max_weight': simulation['max_weight'],
                    'num_pixels': simulation['num_pixels'],
                    'duration': simulation['duration'],
                    'potassium': simulation['potassium'],
                    'sodium': simulation['sodium'],
                    'synaptic_distance': simulation['synaptic_distance']
                })

        return simulations

    def get_simulation(self, _id, return_object=False):
        """
        Fetches an simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        sim = self.collection.find_one({'_id': ObjectId(_id)})

        #get pickle file of the plot
        indir="../server/assets/cstmd/"+str(_id)+"/"+str(sim['num_plots'])+".pkl"
        with open(indir, 'rb') as my_file :
            data = pickle.load(my_file)
        html = mpld3.fig_to_d3(data,template_type="simple")
        sim['plot']=html

        if return_object:
            sample = 1
            frames = 1
            num_neurons = int(sim.get('num_neurons'))
            num_electrodes = int(sim.get('num_electrodes'))
            num_synapses = int(sim.get('num_synapses'))
            synaptic_distance = float(sim.get('synaptic_distance'))
            duration_per_frame = int(sim.get('duration_per_frame'))
            description = sim.get('description')
            potassium=float(sim.get('potassium'))
            sodium=float(sim.get('sodium'))
            max_current=float(sim.get('max_current'))
            min_current=float(sim.get('min_current'))
            min_weight=float(sim.get('min_weight'))
            max_weight=float(sim.get('max_weight'))
            
            cstmd = self.run_simulation(sample, frames, num_neurons,
                                        num_electrodes, num_synapses,
                                        synaptic_distance, duration_per_frame,
                                        description,potassium,sodium,max_current,
                                        min_current,min_weight,max_weight,True)

            return cstmd

        return sim

    def get_spikes(self, _id):
        cursor = self.spikes.find({'sample_id': ObjectId(_id)})
        cursor.sort('_id', direction=1)
        return cursor

    def run_simulation(self,
                       sample,
                       frames,
                       num_neurons,
                       num_electrodes,
                       num_synapses,
                       synaptic_distance,
                       duration_per_frame,
                       description,
                       potassium,
                       sodium,
                       max_current,
                       min_current,
                       min_weight,
                       max_weight,
                       return_object = False):
        """
        Generates and saves a simulation.
        :param sample: Dictionary with information about input sample.
        :param frames: Cursor containing frames.
        :param num_neurons: Number of neurons.
        :param num_electrodes: Number of electrodes.
        :param num_synapses: Number of synapses.
        :param synaptic_distance: Distance between the synapses.
        :param duration_per_frame: Duration per frame of simulation in ms.
        :param description: Optional description field.
        :param potassium: Potassium level.
        :param sodium: Sodium level.
        :param max_current: Maximum current.
        :param min_current: Minimum current.
        :param min_weight: Minimum weight.
        :param max_weight: Maximum weight.
        :return: _id of simulation generated.
        """

        cstmd = Cstmd(num_neurons=num_neurons,
                      num_synapses=num_synapses,
                      synaptic_distance=synaptic_distance,
                      num_electrodes=num_electrodes,
                      duration=duration_per_frame,
                      description=description,
                      potassium=potassium,
                      sodium=potassium,
                      max_current=max_current,
                      min_current=min_current,
                      min_weight=min_weight,
                      max_weight=max_weight,
                      input=frames)

        if return_object:
            return cstmd

        times, cstmd.spike_trains = cstmd.run()
        #cstmd.reset()
        
        # Save CSTMD simulation.
        _id = self.save(cstmd, sample['_id'], sample['animation_id'])

        # Save Plots.
        cstmd.plot_compart_act(str(_id))
        cstmd.plot_fir_rate(str(_id))

        return _id


if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter
