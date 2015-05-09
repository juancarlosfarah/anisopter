__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

from bson.objectid import ObjectId
import os
import sys
import pymongo

from animation.target_animation import Animation


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

        # Target data.
        # for each target:
        # t = {
        #     # target data
        # }
        # Append to targets.

        # General animation data.
        a = {
            "width": animation.width,
            "height": animation.height,
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
                    'width': animation['width'],
                    'height': animation['height'],
                })

        return animations

    def get_animation(self, _id):
        """
        Fetches an animation by _id.
        :param _id: _id of animation to fetch.
        :return: Animation.
        """

        animation = self.collection.find_one({'_id': ObjectId(_id)})
        if "description" not in animation:
            animation['description'] = "Description"

        return animation

    def generate_animation(self, width, height, description, targets):
        """
        Generates and saves an animation.

        :param width:
        :param height:
        :param description:
        :param targets: Array of target dictionaries of the form:
                        { 'color': 'rgb(20,97,107)',
                          'velocity': ['1', '2'],
                          'type': '1',
                          'start_pos': ['1', '2'],
                          'size': '1' }
        :return: _id of animation generated.
        """

        ani = Animation(width, heigh, description)
        for target in targets:
            start = [int(i) for i in target['start_pos']]
            velocity = [int(i) for i in target['velocity']]
            type = int(target['type'])
            size = int(target['size'])
            color = [int(i) for i in target['color'][4:-1].split(", ")]
            ani.add_target(type, start, velocity, v, size, color)


        _id = self.save(a)

        # Save video file.
        print "Current working directory: " + os.getcwd()
        relative_path = "assets/animations/"
        out_directory = os.path.abspath(relative_path + str(_id) + ".avi")
        print "Saving animation in: " + out_directory

        a.run(out_directory)

        return _id

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter