__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import sys
from optparse import OptionParser

import os
import bottle
from bottle import route, post, get, template
import pymongo
import signal
import logging
import simulation_dao
import sample_dao
import animation_dao
import estmd_dao
import cstmd_dao

# Import simulation module.
pr = os.path.abspath(os.path.join("..", "stage1", "pattern_recognition"))
sys.path.append(pr)


@route('/')
def show_index():

    obj = dict()

    return bottle.template('index', obj)


@route('/target_animation')
def show_target_animation():

    obj = dict()
    return bottle.template('target_animation', obj)


@route('/target_animation/animation/new')
def new_animation():

    obj = dict()
    return bottle.template('new_animation', obj)


@route('/target_animation/animations')
def show_animations():

    obj = dict()
    obj['animations'] = animations.get_animations(50)
    return bottle.template('animations', obj)


@get("/target_animation/animation/<_id>")
def show_animation(_id):

    anim = animations.get_animation(_id)
    if anim is None:
        bottle.redirect("/")

    obj = dict()
    obj['animation'] = anim
    return bottle.template("animation", obj)


@route('/cstmd')
def show_cstmd():

    obj = dict()
    return bottle.template('cstmd', obj)


@route('/cstmd/simulation/new')
def new_cstmd_simulation():

    obj = dict()
    obj['samples'] = estmd.get_simulations(50)
    return bottle.template('new_cstmd_simulation', obj)


@post('/cstmd/simulation/run')
def run_cstmd_simulation():
    form = bottle.request.forms
    sample_id = form.get("sample")
    num_neurons = int(form.get("num_neurons"))
    num_electrodes = int(form.get("num_electrodes"))
    duration = int(form.get("duration"))
    description = form.get("description")
    sample = estmd.get_simulation(sample_id)
    frames = estmd.get_frames(sample_id)
    _id = cstmd.run_simulation(sample,
                               frames,
                               num_neurons,
                               num_electrodes,
                               duration,
                               description)
    bottle.redirect("/cstmd/simulation/" + str(_id))


@route('/cstmd/simulations')
def show_cstmd_simulations():

    obj = dict()
    obj['simulations'] = cstmd.get_simulations(50)
    return bottle.template('cstmd_simulations', obj)


@get("/cstmd/simulation/<_id>")
def show_cstmd_simulation(_id):

    sim = cstmd.get_simulation(_id)

    if sim is None:
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("cstmd_simulation", obj)


@route('/pattern_recognition')
def show_pattern_recognition():

    obj = dict()
    return bottle.template('pattern_recognition', obj)


@route('/pattern_recognition/simulations')
def show_simulations():

    obj = dict()
    obj['simulations'] = simulations.get_simulations(50)

    return bottle.template('simulations', obj)


@route('/pattern_recognition/simulation/new')
def new_simulation():

    obj = dict()
    obj['samples'] = samples.get_samples(10)
    obj['cstmd'] = cstmd.get_simulations(10)
    return bottle.template('new_simulation', obj)


@post('/pattern_recognition/simulation/run')
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
    bottle.redirect("/pattern_recognition/simulation/" + str(_id))


@get("/pattern_recognition/simulation/<_id>")
def show_simulation(_id):

    sim = simulations.get_simulation(_id)

    if sim is None:
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("simulation", obj)


@route('/pattern_recognition/samples')
def show_samples():

    obj = dict()
    obj['samples'] = samples.get_samples(10)

    return bottle.template('samples', obj)


@get("/pattern_recognition/sample/<_id>")
def show_sample(_id):

    sample = samples.get_sample(_id)

    if sample is None:
        bottle.redirect("/")

    obj = dict()
    obj['sample'] = sample
    return bottle.template("sample", obj)


@route('/pattern_recognition/samples/new')
def new_sample():

    obj = dict()
    return bottle.template('new_sample', obj)


@post('/pattern_recognition/sample/generate')
def generate_sample():
    form = bottle.request.forms
    duration = int(form.get("duration"))
    num_neurons = int(form.get("num_neurons"))
    num_patterns = int(form.get("num_patterns"))
    description = form.get("description")
    _id = samples.generate_sample(duration, num_neurons,
                                  num_patterns, description)
    bottle.redirect("/pattern_recognition/sample/" + str(_id))


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
    bottle.run(host="localhost",
               port=8082,
               reloader=True)


def connect_db(db_name="anisopter"):
    global db, simulations, samples, animations, cstmd, estmd
    host = "localhost"
    port = 27017
    connection = pymongo.MongoClient(host=host, port=port)
    db = connection[db_name]

    # Data Access Objects.
    animations = animation_dao.AnimationDao(db)
    estmd = estmd_dao.EstmdDao(db)
    cstmd = cstmd_dao.CstmdDao(db)
    simulations = simulation_dao.SimulationDao(db)
    samples = sample_dao.SampleDao(db)

if __name__ == "__main__":
    connect_db("anisopter")
    start()
else:
    # Run bottle in application mode.
    connect_db("anisopter")
    app = application = bottle.default_app()