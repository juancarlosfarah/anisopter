__author__ = 'juancarlosfarah'

import unittest
import sample_dao
import simulation_dao
import bottle
import server
import os
import pymongo


class SampleDaoTests(unittest.TestCase):

    def setUp(self):
        """
        Sets up for the tests.
        :return: None.
        """
        host = "146.169.47.184"
        port = 27017
        connection = pymongo.MongoClient(host=host, port=port)
        db = connection["anisopter"].test

        # Data Access Objects.
        self.simulations = simulation_dao.SimulationDao(db)
        self.samples = sample_dao.SampleDao(db)
        self.simulations.collection.drop()
        self.samples.collection.drop()

    def test_index(self):
        """
        Tests if index can be accessed.
        :return: None.
        """
        page = server.show_index()
        obj = dict()
        self.failUnless(bottle.template('index', obj) == page)

    def test_everything(self):
        """
        One big badass test.
        :return: None.
        """
        page = server.show_target_animation()
        page = server.new_animation()
        page = server.show_animations()
        with self.assertRaises(KeyError):
            page = server.remove_animation()
        with self.assertRaises(TypeError):
            page = server.generate_animation()
        page = server.new_animation_background()
        with self.assertRaises(KeyError):
            page = server.upload_animation_background()
        page = server.show_backgrounds()
        page = server.show_estmd()
        page = server.new_estmd_simulation()
        page = server.show_estmd_simulations()
        page = server.show_cstmd()
        page = server.new_cstmd_simulation()
        with self.assertRaises(KeyError):
            page = server.run_cstmd_simulation()
        with self.assertRaises(NameError):
            page = server.show_cstmd_simulations()
        page = server.show_pattern_recognition()
        page = server.show_simulations()
        page = server.run_simulation()
        page = server.show_samples()
        page = server.new_sample()
        page = server.generate_sample()
        page = server.show_as()
        page = server.new_as_simulation()
        page = server.run_action_selection_simulation()
        page = server.show_action_selection_simulations()
        page = server.show_tr()
        page = server.show_training_simulations()
        page = server.new_training_simulation()
        page = server.generate_simulation()


        
'''
    def test_simulation(self):
        """
        Tests if a simulation can be accessed.
        :return: None.
        """

        # Save new simulation.
        duration = 500
        num_neurons = 100
        num_patterns = 1
        description = "Test_1"
        _id = self.simulations.run_simulation(duration,
                                              num_neurons,
                                              num_patterns,
                                              description)

        # Get page.
        page = server.show_simulation(_id)

        # Test for equality.
        sim = self.simulations.get_simulation(_id)
        obj = dict()
        obj['simulation'] = sim
        # self.failUnless(bottle.template('simulation', obj) == page)

    def test_new_simulation(self):
        """
        Tests if the new simulation page can be accessed.
        :return: None.
        """

        # Get page.
        page = server.new_simulation()

        # Test for equality.
        obj = dict()
        self.failUnless(bottle.template('new_simulation', obj) == page)

    def test_samples(self):
        """
        Tests if samples can be accessed.
        :return: None.
        """
        page = server.show_samples()
        obj = dict()
        obj['samples'] = self.samples.get_samples(10)
        self.failUnless(bottle.template('samples', obj) == page)

    def test_sample(self):
        """
        Tests if a sample can be accessed.
        :return: None.
        """

        # Save new simulation.
        duration = 500
        num_neurons = 100
        num_patterns = 1
        description = "Test_1"
        _id = self.samples.generate_sample(duration,
                                           num_neurons,
                                           num_patterns,
                                           description)

        # Get page.
        page = server.show_sample(_id)

        # Test for equality.
        sample = self.samples.get_sample(_id)
        obj = dict()
        obj['sample'] = sample
        self.failUnless(bottle.template('sample', obj) == page)

    def test_new_sample(self):
        """
        Tests if the new sample page can be accessed.
        :return: None.
        """

        # Get page.
        page = server.new_sample()

        # Test for equality.
        obj = dict()
        self.failUnless(bottle.template('new_sample', obj) == page)

    def test_static(self):
        """
        Tests if static files can be accessed.
        :return: None.
        """

        # Get files.
        jq = server.jquery("jquery.js")
        js = server.bootstrap_js("bootstrap.js")
        css = server.bootstrap_css("bootstrap.css")

        # Get roots.
        root_jq = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               "static"))
        root_js = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               "static",
                                               "bootstrap",
                                               "js"))
        root_css = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "static",
                                                "bootstrap",
                                                "css"))

        # Assertions.
        # self.failUnless(jq == bottle.static_file("jquery.js", root=root_jq))
        # self.failUnless(js == bottle.static_file("bootstrap.js", root=root_js))
        # self.failUnless(css == bottle.static_file("bootstrap.css",
        #                                           root=root_css))

    def tearDown(self):
        """
        Resets the sample for the tests.
        :return:
        """
        self.simulations = None
        self.samples = None
'''


def main():
    unittest.main()

if __name__ == '__main__':
    main()
