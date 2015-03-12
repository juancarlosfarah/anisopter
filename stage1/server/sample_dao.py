__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import numpy as np
import mpld3
import pylab
import math
from matplotlib.patches import Rectangle
import pymongo
from stage1.pattern_recognition import sample


class SampleDao:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.collection = self.db.samples

    def save(self, sample):
        """
        Saves the sample to the database.
        :return: None.
        """
        # start_positions = []
        patterns = []
        for i in range(len(sample.start_positions)):
            # start_positions.append(sample.start_positions[i].tolist())
            patterns.append(sample.patterns[i].tolist())

        # General sample data.
        s = {
            "duration": sample.duration,
            "num_afferents": sample.num_neurons,
            "description": sample.description,
            "start_positions": sample.start_positions,
            "pattern_duration": sample.pattern_duration,
            "patterns": patterns,
            "dt": int(sample.dt * 100),
            "rep_ratio": sample.rep_ratio,
            "inv_ratio": sample.inv_ratio,
            "noise": sample.noise,
            "r_min": sample.r_min,
            "r_max": sample.r_max,
            "s_min": sample.s_min,
            "s_max": sample.s_max,
            "ds_min": sample.ds_min,
            "ds_max": sample.ds_max
        }

        _id = self.collection.insert(s)

        # Save the spike trains.
        collection = self.db.spikes
        for dt in range(sample.duration):
            obj = {
                "sample_id": _id,
                "spikes": sample.spike_trains[:, dt].tolist()
            }
            collection.insert(obj)

        return _id

    def get_samples(self, num_samples):
        """
        Fetches a given number of samples from the database.
        :param num_samples: Number of simulations to fetch.
        :return: Array of samples.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_samples)
        samples = []

        for sample in cursor:
            if "description" not in sample:
                sample['description'] = "Description"
            samples.append(
                {
                    '_id': sample['_id'],
                    'date': sample['_id'].generation_time,
                    'description': sample['description'],
                    'num_afferents': sample['num_afferents'],
                    'duration': sample['duration'],
                })

        return samples

    def get_sample(self, _id):
        """
        Fetches a sample by _id.
        :param _id: _id of sampleto fetch.
        :return: Sample.
        """

        sample = self.collection.find_one({'_id': ObjectId(_id)})

        return sample

    def generate_sample(self, duration, num_neurons, num_patterns, description):
        s = sample.SampleGenerator(duration,
                                   num_neurons=num_neurons,
                                   description=description)
        s.generate_sample()
        s.generate_patterns(num_patterns=num_patterns)
        s.insert_patterns()
        s.add_noise()
        _id = self.save(s)
        return _id

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter

    s = sample.SampleGenerator(1000, num_neurons=10)
    s.generate_sample()
    sample_dao = SampleDao(db)
    sample_dao.save(s)