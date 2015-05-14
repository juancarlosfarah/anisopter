__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import os
import pymongo
from action_selection.action_selection import ActionSelection
from brian2 import *
import pickle

class ActionSelectionDao:

    def __init__(self, database):
        self.db = database
        self.collection = self.db.action_selection

    def save(self, a_s):
        """
        Saves the action selection simulation to the database.
        :return: _id of simulation inserted.
        """

        # General action data.
        a_s = {
            'description': a_s.description,
            'num_neurons': a_s.N,
            'tau_m': (a_s.taum/ms).tolist(),
            'tau_pre':  (a_s.taum/ms).tolist(),
            'tau_post': (a_s.taupost/ms).tolist(),
            'tau_c': (a_s.tauc/ms).tolist(),
            'tau_dop': (a_s.tauDop/ms).tolist(),
            'tau_e': (a_s.taue/ms).tolist(),
            'Ee': (a_s.Ee/mV).tolist(),
            'vt': (a_s.vt/mV).tolist(),
            'vr': (a_s.vr/mV).tolist(),
            'El': (a_s.El/mV).tolist(),
            'F': (a_s.F/Hz).tolist(),
            'gmax': a_s.gmax,
            'dA_pre': a_s.dApre,
            'dA_post': a_s.dApost,
            'duration': (a_s.sim_time/ms).tolist(),
            'frame_length': (a_s.frame_length/ms).tolist(),
            'dop_boost': a_s.dopBoost,
            'reward_distance': a_s.reward_distance,
            'speed_factor': (a_s.SPEED_FACTOR/second).tolist(),
            'dragonfly_start': a_s.dragonfly_start,
            'animation_id': a_s.animation_id,
            'pattern_recognition_id': a_s.pattern_recognition_id,
            'weights': (a_s.saved_weights).tolist(),
            'training': a_s.training
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
        simulations = []

        for s in cursor:
            s['date'] = s['_id'].generation_time
            simulations.append(s)

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
                                    animation=None,
                                    pattern_input=None,
                                    pattern_duration=None,
                                    SPEED_FACTOR=2,
                                    dragonfly_start=[300, 300, 0.0],
                                    description="",
                                    animation_id=None,
                                    pattern_recognition_id=None,
                                    saved_weights=None,
                                    training=True):

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
                                   SPEED_FACTOR*second,
                                   dragonfly_start,
                                   description,
                                   pattern_duration,
                                   pattern_input,
                                   animation,
                                   animation_id,
                                   pattern_recognition_id,
                                   saved_weights,
                                   training)

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
                       SPEED_FACTOR=2*second,
                       dragonfly_start=[300, 300, 0.0],
                       description="",
                       pattern_duration=None,
                       pattern_input=None,
                       animation=None,
                       animation_id=None,
                       pattern_recognition_id=None,
                       saved_weights=None,
                       training=True):
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
                              SPEED_FACTOR=SPEED_FACTOR,
                              dragonfly_start=dragonfly_start,
                              description=description,
                              animation=animation,
                              pattern_duration=pattern_duration,
                              pattern_input=pattern_input,
                              animation_id=animation_id,
                              pattern_recognition_id=pattern_recognition_id,
                              saved_weights=saved_weights,
                              training=training)

        a_s.run()

        # Save action selection simulation.
        _id = self.save(a_s)

        # Save video to filesystem.
        self.save_video(a_s, str(_id))

        return _id

    def save_video(self, a_s, _id):

        save_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "assets",
                                                 "action_selection",
                                                 _id))
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Save video file.
        print "Current working directory: " + os.getcwd()
        out_directory = os.path.abspath(save_path + "/" + str(_id) + ".avi")
        print "Saving animation in: " + out_directory

        a_s.run_animation(out_directory)

    def plot_graphs(self, input_dir):
        pass

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter
