__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import sys
from optparse import OptionParser

import os

import bottle
import pymongo
from stage1.server import simulation_dao
from stage1.server import sample_dao
import bottledaemon as bottled


# Import simulation module.
pr = os.path.abspath(os.path.join("..", "stage1", "pattern_recognition"))
sys.path.append(pr)

@bottle.route('/')
def show_index():

    obj = dict()

    return bottle.template('index', obj)

@bottle.route('/simulations')
def show_simulations():

    obj = dict()
    obj['simulations'] = simulations.get_simulations(10)

    return bottle.template('simulations', obj)

@bottle.route('/simulation/new')
def new_simulation():

    obj = dict()
    return bottle.template('new_simulation', obj)


@bottle.post('/simulation/run')
def run_simulation():
    form = bottle.request.forms
    duration = int(form.get("duration"))
    num_neurons = int(form.get("num_neurons"))
    num_patterns = int(form.get("num_patterns"))
    description = form.get("description")
    _id = simulations.run_simulation(duration, num_neurons,
                                     num_patterns, description)
    bottle.redirect("/simulation/" + str(_id))

@bottle.get("/simulation/<_id>")
def show_simulation(_id):

    sim = simulations.get_simulation(_id)

    if sim is None:
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("simulation", obj)

@bottle.route('/samples')
def show_samples():

    obj = dict()
    obj['samples'] = samples.get_samples(10)

    return bottle.template('samples', obj)

@bottle.get("/sample/<_id>")
def show_sample(_id):

    sample = samples.get_sample(_id)

    if sample is None:
        bottle.redirect("/")

    obj = dict()
    obj['sample'] = sample
    return bottle.template("sample", obj)

@bottle.route('/samples/new')
def new_sample():

    obj = dict()
    return bottle.template('new_sample', obj)

@bottle.post('/sample/generate')
def generate_sample():
    form = bottle.request.forms
    duration = int(form.get("duration"))
    num_neurons = int(form.get("num_neurons"))
    num_patterns = int(form.get("num_patterns"))
    description = form.get("description")
    _id = samples.generate_sample(duration, num_neurons,
                                  num_patterns, description)
    bottle.redirect("/sample/" + str(_id))

# Static Routes
@bottle.get('/static/bootstrap/css/<filename>')
def bootstrap_css(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "static",
                                        "bootstrap",
                                        "css"))
    return bottle.static_file(filename, root=root)

@bottle.get('/static/bootstrap/js/<filename>')
def bootstrap_js(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "static",
                                        "bootstrap",
                                        "js"))
    return bottle.static_file(filename, root=root)

@bottle.get('/static/<filename>')
def jquery(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
    return bottle.static_file(filename, root=root)


def main():

    # Parse command line options.
    parser = OptionParser()
    parser.add_option("--host", dest="host", default='localhost',
                      help="specify HOST", metavar="HOST")
    parser.add_option("-p", "--port", dest="port", default=8082,
                      help="specify PORT", metavar="PORT")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="run locally", default=False)

    (options, args) = parser.parse_args()

    # Start the webserver running and wait for requests.
    if options.debug:
        bottle.debug(True)
        bottle.run(host=options.host, port=options.port, reloader=True)
    else:
        bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(
            os.path.dirname(__file__), "views")))
        bottled.daemon_run(host="146.169.47.153", port=55080)

if __name__ == "__main__":
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection.anisopter

    # Data Access Objects.
    simulations = simulation_dao.SimulationDao(db)
    samples = sample_dao.SampleDao(db)
    main()