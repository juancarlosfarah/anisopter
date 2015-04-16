__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import os
import sys
import pymongo

# from animation.target_animation import Animation


class AnimationDao:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.collection = self.db.animations

    def save(self, animation):
        """
        Saves the animation to the database.
        :return: _id of animation inserted.
        """

        # Targets.
        targets = []

        # General animation data.
        a = {
            "width": animation.width,
            "height": animation.height,
            "duration": animation.duration,
            "targets": targets
        }

        _id = self.collection.insert(a)

        return _id

    def get_animations(self, num_animations):
        """
        Fetches a given number of animations from the database.
        :param num_animations: Number of animations to fetch.
        :return: Array of animations.
        """
        c = self.collection
        cursor = c.find().sort('_id', direction=-1).limit(num_animations)
        animations = []

        for animation in cursor:
            if "description" not in animation:
                animation['description'] = "Description"
            animations.append(
                {
                    '_id': animation['_id'],
                    'date': animation['_id'].generation_time,
                    'description': animation['description'],
                    'targets': animation['targets'],
                    'width': animation['width'],
                    'height': animation['height'],
                    'duration': animation['duration'],
                })

        return animations

    def get_animation(self, _id):
        """
        Fetches an animation by _id.
        :param _id: _id of animation to fetch.
        :return: Animation.
        """

        animation = self.collection.find_one({'_id': ObjectId(_id)})

        return animation

    def generate_animation(self):
        """
        Generates and saves an animation.
        :return: _id of animation generated.
        """

        _id = None
        # a = Animation()
        # a.add_target(2)
        #
        # _id = self.save()
        # out_directory = "assets/animations/" + "animation" + str(_id)
        # a.run(out_directory)

        return _id

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter