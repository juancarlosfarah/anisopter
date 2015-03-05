__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import sys
import os
import bottle
import pymongo
import simulation_dao

# Import simulation module.
pr = os.path.abspath(os.path.join("..", "stage1", "pattern_recognition"))
sys.path.append(pr)

@bottle.route('/')
def show_index():

    obj = dict()
    obj['simulations'] = simulations.get_simulations(5)

    return bottle.template('index', obj)

@bottle.get("/simulation/<_id>")
def show_simulation(_id):

    sim = simulations.get_simulation(_id)

    if sim is None:
        print "None!"
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("simulation", obj)

# Static Routes
@bottle.get('/static/bootstrap/css/<filename>')
def bootstrap_css(filename):
    return bottle.static_file(filename, root='static/bootstrap/css')

@bottle.get('/static/bootstrap/js/<filename>')
def bootstrap_js(filename):
    return bottle.static_file(filename, root='static/bootstrap/js')

@bottle.get('/static/<filename>')
def jquery(filename):
    return bottle.static_file(filename, root='static')


if __name__ == '__main__':
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter

    # Data Access Objects.
    simulations = simulation_dao.SimulationDao(db)

    # Start the webserver running and wait for requests.
    bottle.debug(True)
    bottle.run(host='localhost', port=508080, reloader=True)