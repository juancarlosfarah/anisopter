__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import sys
from optparse import OptionParser

import os
from daemon import runner
import bottle
from bottle import route, post, get, template
import pymongo
import signal
import logging
import simulation_dao
import sample_dao
import bottledaemon as bottled

# Import simulation module.
pr = os.path.abspath(os.path.join("..", "stage1", "pattern_recognition"))
sys.path.append(pr)


@route('/')
def show_index():

    obj = dict()

    return bottle.template('index', obj)


@route('/simulations')
def show_simulations():

    obj = dict()
    obj['simulations'] = simulations.get_simulations(50)

    return bottle.template('simulations', obj)


@route('/simulation/new')
def new_simulation():

    obj = dict()
    obj['samples'] = samples.get_samples(10)
    return bottle.template('new_simulation', obj)


@post('/simulation/run')
def run_simulation():
    form = bottle.request.forms
    sample_id = form.get("sample")
    num_neurons = int(form.get("num_neurons"))
    a_plus = float(form.get("a_plus"))
    a_minus = float(form.get("a_minus"))
    theta = float(form.get("theta"))
    description = form.get("description")
    a_ratio = a_minus / a_plus
    sample = samples.get_sample(sample_id)
    spikes = samples.get_spikes(sample_id)
    _id = simulations.run_simulation(sample, spikes, num_neurons,
                                     description, a_plus, a_ratio, theta)
    bottle.redirect("/simulation/" + str(_id))


@get("/simulation/<_id>")
def show_simulation(_id):

    sim = simulations.get_simulation(_id)

    if sim is None:
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("simulation", obj)


@route('/samples')
def show_samples():

    obj = dict()
    obj['samples'] = samples.get_samples(10)

    return bottle.template('samples', obj)


@get("/sample/<_id>")
def show_sample(_id):

    sample = samples.get_sample(_id)

    if sample is None:
        bottle.redirect("/")

    obj = dict()
    obj['sample'] = sample
    return bottle.template("sample", obj)


@route('/samples/new')
def new_sample():

    obj = dict()
    return bottle.template('new_sample', obj)


@post('/sample/generate')
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
@get('/static/bootstrap/css/<filename>')
def bootstrap_css(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "static",
                                        "bootstrap",
                                        "css"))
    return bottle.static_file(filename, root=root)


@get('/static/bootstrap/js/<filename>')
def bootstrap_js(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "static",
                                        "bootstrap",
                                        "js"))
    return bottle.static_file(filename, root=root)


@get('/static/<filename>')
def jquery(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
    return bottle.static_file(filename, root=root)


def start():
    # # Parse command line options.
    # parser = OptionParser()
    # parser.add_option("--host", dest="host", default='localhost',
    #                   help="specify HOST", metavar="HOST")
    # parser.add_option("-p", "--port", dest="port", default=8082,
    #                   help="specify PORT", metavar="PORT")
    # parser.add_option("-d", "--debug", action="store_true", dest="debug",
    #                   help="run locally", default=False)
    #
    # (options, args) = parser.parse_args()
    #
    # # Start the webserver running and wait for requests.
    # if options.debug:
    #     bottle.debug(True)
    #     bottle.run(host=options.host, port=options.port, reloader=True)
    # else:
    #     print "Running as daemon"
    #     host = "localhost" #"146.169.47.153"
    #     port = 8082 #55080
    #     bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(
    #         os.path.dirname(__file__), "views")))
    #     bottled.daemon_run(host=host, port=port,
    #                        logfile="tmp/server.log", pidfile="tmp/server.pid")
    bottle.run(host="localhost",
               port=8082,
               reloader=True)


class Server():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = './tmp/server.log'
        self.stderr_path = './tmp/server.log'
        self.pidfile_path = '/tmp/server.pid'
        self.pidfile_timeout = 5

    def run(self):
        bottle.run(host="localhost",
                   port=8082,
                   reloader=True)


def connect_db(db_name="anisopter"):
    global db, simulations, samples
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    db = connection[db_name]

    # Data Access Objects.
    simulations = simulation_dao.SimulationDao(db)
    samples = sample_dao.SampleDao(db)

if __name__ == "__main__":
    connect_db("anisopter")
    # s = Server()
    # logger = logging.getLogger("DaemonLog")
    # logger.setLevel(logging.INFO)
    # formatter = logging.Formatter("%(asctime)s - %(name)s - "
    #                               "%(levelname)s - %(message)s")
    # handler = logging.FileHandler("./tmp/server.log")
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # daemon_runner = runner.DaemonRunner(s)
    # daemon_runner.do_action()
    start()
else:
    # Run bottle in application mode.
    app = application = bottle.default_app()