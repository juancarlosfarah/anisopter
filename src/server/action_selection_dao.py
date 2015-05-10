__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import pymongo
from action_selection.action_selection import ActionSelection
from brian2 import *
import pickle

class ActionSelectionDao:

    def __init__(self, database):
        self.db = database
        self.collection = self.db.action_selections

    def save(self, a_s):
        """
        Saves the action selection simulation to the database.
        :return: _id of simulation inserted.
        """

        # General action data.
        a_s = {
            'description': a_s.description,
            'N': a_s.N,
            'tau_m': a_s.taum,
            'tau_pre':  a_s.taum,
            'tau_post': a_s.taupost,
            'tau_c': a_s.tauc,
            'tau_dop': a_s.tauDop,
            'tau_e': a_s.taue,
            'Ee': a_s.Ee,
            'vt': a_s.vt,
            'vr': a_s.vr,
            'El': a_s.El,
            'F': a_s.F,
            'gmax': a_s.gmax,
            'dA_pre': a_s.dApre,
            'dA_post': a_s.dApost,
            'duration': a_s.sim_time,
            'frame_length': a_s.frame_length,
            'dop_boost': a_s.dopBoost,
            'reward_distance': a_s.reward_distance,
            'speed_factor': a_s.SPEED_FACTOR,
            'dragonfly_start': a_s.dragonfly_start,
            'output_dir': a_s.output_dir
        }

        # Save general data.
        _id = self.collection.insert(a_s)

        return _id

    def get_simulations(self, num_simulations):
        """
        Fetches a given number of simulations from the database.
        :param num_simulations: Number of simulations to fetch.
        :return: Array of simulations.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_simulations)
        simulations = list(cursor)

        return simulations

    def get_simulation(self, _id):
        """
        Fetches an simulation by _id.
        :param _id: _id of simulation to fetch.
        :return: Simulation.
        """

        simulation = self.collection.find_one({'_id': ObjectId(_id)})

        return simulation

    def run_simulation_preprocessor(self,
                                    N=4,
                                    taum=10,
                                    taupre=20,
                                    taupost=20,
                                    tauc=20,
                                    tauDop=20,
                                    Ee=0,
                                    vt=-54,
                                    vr=-60,
                                    El=-74,
                                    taue=5,
                                    F=15,
                                    gmax=1,
                                    dApre=1,
                                    sim_time=100.0,
                                    frame_length=10.0,
                                    dopBoost=0.5,
                                    reward_distance=40,
                                    fromAnim=True,
                                    SPEED_FACTOR=2,
                                    dragonfly_start=[300, 300, 0.0],
                                    description="",
                                    output_dir="assets/action_selection/output.avi"):

        _id = self.run_simulation(N,
                                   taum*ms,
                                   taupre*ms,
                                   taupost*ms,
                                   tauc*ms,
                                   tauDop*ms,
                                   Ee*mV,
                                   vt*mV,
                                   vr*mV,
                                   El*mV,
                                   taue*ms,
                                   F*Hz,
                                   gmax,
                                   dApre,
                                   sim_time*ms,
                                   frame_length*ms,
                                   dopBoost,
                                   reward_distance,
                                   fromAnim,
                                   SPEED_FACTOR*second,
                                   dragonfly_start,
                                   description,
                                   output_dir)

        return _id

    def run_simulation(self, 
                       N=4,
                       taum=10*ms,
                       taupre=20*ms,
                       taupost=20*ms,
                       tauc=20*ms,
                       tauDop=20*ms,
                       Ee=0*mV,
                       vt=-54*mV,
                       vr=-60*mV,
                       El=-74*mV,
                       taue=5*ms,
                       F=15*Hz,
                       gmax=1,
                       dApre=1,
                       sim_time=100.0*ms,
                       frame_length=10.0*ms,
                       dopBoost=0.5,
                       reward_distance=40,
                       fromAnim=True,
                       SPEED_FACTOR=2*second,
                       dragonfly_start=[300, 300, 0.0],
                       description="",
                       output_dir="assets/action_selection/output.avi"):
        """
        Generates and saves a simulation.
        """

        # Get the input.

        # Instantiate an ActionSelection object.
        a_s = ActionSelection(N=N,
                              taum=taum,
                              taupre=taupre,
                              taupost=taupost,
                              tauc=tauc,
                              tauDop=tauDop,
                              Ee=Ee,
                              vt=vt,
                              vr=vr,
                              El=El,
                              taue=taue,
                              F=F,
                              gmax=gmax,
                              dApre=dApre,
                              sim_time=sim_time,
                              frame_length=frame_length,
                              dopBoost=dopBoost,
                              reward_distance=reward_distance,
                              fromAnim=fromAnim,
                              SPEED_FACTOR=SPEED_FACTOR,
                              dragonfly_start=dragonfly_start,
                              description=description,
                              output_dir="output.avi")

        a_s.run()

        # Save video to filesystem.
        
        # Save action selection simulation.
        _id = self.save(a_s)

        return _id

    def save_pickles(self, a_s, _id):
        
        pickle.dump(a_s.synapse_mon, open(output_dir+"/synapse_mon.pkl", "wb"))
        pickle.dump(a_s.w0_mon, open(output_dir+"/w0_mon.pkl", "wb"))
        pickle.dump(a_s.w1_mon, open(output_dir+"/w1_mon.pkl", "wb"))
        pickle.dump(a_s.w2_mon, open(output_dir+"/w2_mon.pkl", "wb"))
        pickle.dump(a_s.w3_mon, open(output_dir+"/w3_mon.pkl", "wb"))
        pickle.dump(a_s.spike_mon, open(output_dir+"/spike_mon.pkl", "wb"))
        pickle.dump(a_s.r0_mon, open(output_dir+"/r0_mon.pkl", "wb"))
        pickle.dump(a_s.r1_mon, open(output_dir+"/r1_mon.pkl", "wb"))
        pickle.dump(a_s.r2_mon, open(output_dir+"/r2_mon.pkl", "wb"))
        pickle.dump(a_s.r3_mon, open(output_dir+"/r3_mon.pkl", "wb"))

    def plot_graphs(self, input_dir):
        synapse

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter
