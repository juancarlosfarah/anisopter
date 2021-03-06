__author__ = 'eg1114'
__authoremail__ = 'erikgrabljevec5@gmail.com'


from bson.objectid import ObjectId
import os
import pickle
import pymongo

import action_selection_dao
import animation_dao
import cstmd_dao
import estmd_dao
import simulation_dao

from training.training import Training


class TrainingDao(object):

    # Constructor for the class.
    def __init__(self, database):
        self.db = database
        self.collection = self.db.trainings

        self.ad = animation_dao.AnimationDao(self.db)
        self.ed = estmd_dao.EstmdDao(self.db)
        self.cd = cstmd_dao.CstmdDao(self.db)
        self.sd = simulation_dao.SimulationDao(self.db)

    def save(self, tr_set):
        """
        Saves the training set to the database.

        :param tr_set: Training set that we are saving.
        :return: _id of training set inserted.
        """

        # General animation data.
        a = {
            "repetitions": tr_set.n,
            "vertical": tr_set.types[0],
            "horizontal": tr_set.types[1],
            "diagonal": tr_set.types[2],
            "anti_diagonal": tr_set.types[3],
        }

        _id = self.collection.insert(a)

        return _id

    def remove(self, _id):
        """
        Removes one training from the database. Deletes its related files.
        :param _id: ID of training to remove.
        :return: None.
        """
        self.collection.remove({"_id": ObjectId(_id)})

        return

    def get_simulations(self, num_sets):
        """
        Fetches a given number of training sets from the database.
        :param num_animations: Number of trainings set to fetch.
        :return: Array of training sets.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_sets)
        trainings = []

        for training in cursor:
            if "description" not in training:
                training['description'] = "Description"

            trainings.append(
                    {
                    '_id': training['_id'],
                    'date': training['_id'].generation_time,
                    'description': training['description'],
                    })

        return trainings

    def get_simulation(self, _id):
        """
        Fetches an training set by _id.
        :param _id: _id of training set to fetch.
        :return: Training set.
        """

        training = self.collection.find_one({'_id': ObjectId(_id)})
        if "description" not in training:
            training['description'] = "Description"

        return training

    def generate_training_simulation(self, input_id, types,
                                     n, return_object=False):
        """
        Generates and saves a training set.

        :return: _id of training set generated.
        """

        print "Input ID:"
        print input_id
        print "------------------------------"

        sim = self.sd.get_simulation(input_id)

        ani_id = sim['animation_id']

        print ani_id

        estmd_id = sim['estmd_id']
        cstmd_id = sim['cstmd_id']
        id = sim['_id']

        ani = self.ad.get_animation(ani_id, True)
        estmd = self.ed.get_simulation(estmd_id, True)
        cstmd = self.cd.get_simulation(cstmd_id, True)
        sim = self.sd.get_simulation(id, True)

        tr_set = Training(types, n, ani, estmd, cstmd, sim)

        if return_object:
            return tr_set

        tr_set.run()


if __name__ == "__main__":
    print "Starting test!"

    host = "146.169.47.184"
    port = 27017
    db_name = "anisopter"

    connection = pymongo.MongoClient(host=host, port=port)
    db = connection[db_name]

    sd = simulation_dao.SimulationDao(db)
    id = "5557942e2d1baa4cefc6d7de"

    t = TrainingDao(db)
    t.generate_training_simulation(id, [1, 1, 1, 1], 1)

    print "Connected and done."
