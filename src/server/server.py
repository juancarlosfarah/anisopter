__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import sys
from optparse import OptionParser

import os
import bottle
from bottle import route, post, get, template, request
import pymongo
import simulation_dao
import sample_dao
import animation_dao
import estmd_dao
import cstmd_dao
import action_selection_dao


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


@post('/target_animation/animation/generate')
def generate_animation():
    width = int(request.json['width'])
    height = int(request.json['height'])
    description = request.json['description']
    targets = request.json['targets']
    frames = int(request.json['frames'])
    _id = animations.generate_animation(width, height, description,
                                        targets, frames)
    rvalue = {"url": "/target_animation/animation/" + str(_id)}
    return rvalue


@route('/estmd')
def show_estmd():

    obj = dict()
    return bottle.template('estmd', obj)


@route('/estmd/simulation/new')
def new_estmd_simulation():

    obj = dict()
    obj['samples'] = animations.get_animations(50)
    return bottle.template('new_estmd_simulation', obj)


@post('/estmd/simulation/run')
def run_estmd_simulation():
    form = bottle.request.forms
    sample_id = form.get("sample")
    description = form.get("description")
    _id = estmd.run_simulation(sample_id, description)
    bottle.redirect("/estmd/simulation/" + str(_id))


@route('/estmd/simulations')
def show_estmd_simulations():

    obj = dict()
    obj['simulations'] = estmd.get_simulations(50)
    return bottle.template('estmd_simulations', obj)


@get("/estmd/simulation/<_id>")
def show_estmd_simulation(_id):

    sim = estmd.get_simulation(_id)

    if sim is None:
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("estmd_simulation", obj)


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
    num_synapses = int(form.get("num_synapses"))
    synaptic_distance = int(form.get("synaptic_distance"))
    duration_per_frame = int(form.get("duration_per_frame"))
    description = form.get("description")
    sample = estmd.get_simulation(sample_id)
    frames = estmd.get_frames(sample_id)
    _id = cstmd.run_simulation(sample,
                               frames,
                               num_neurons,
                               num_electrodes,
                               num_synapses,
                               synaptic_distance,
                               duration_per_frame,
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

    # Get sample.
    sample = samples.get_sample(sample_id)

    # If no sample is found, perhaps it's a CSTMD simulation.
    if sample is None:
        sample = cstmd.get_simulation(sample_id)

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

# Action Selection
# ================
@route('/action_selection')
def show_as():
    obj = dict()
    return bottle.template('action_selection', obj)


@route('/action_selection/simulation/new')
def new_as_simulation():
    obj = dict()
    obj['input'] = simulations.get_simulations(50)
    return bottle.template('new_action_selection_simulation', obj)


@post('/action_selection/simulation/run')
def run_action_selection_simulation():
    form = bottle.request.forms
    input_id = form.get("sample")
    N = int(form.get("num_neurons"))
    taum = float(form.get("tau_m"))
    taupre = float(form.get("tau_pre"))
    taupost = float(form.get("tau_post"))
    tauc = float(form.get("tau_c"))
    tauDop = float(form.get("tau_dop"))
    Ee = float(form.get("Ee"))
    vt = float(form.get("vt"))
    vr = float(form.get("vr"))
    El = float(form.get("El"))
    taue = float(form.get("tau_e"))
    F = float(form.get("F"))
    gmax = float(form.get("gmax"))
    dApre = float(form.get("dApre"))
    sim_time = float(form.get("duration"))
    frame_length = float(form.get("frame_length"))
    dopBoost = float(form.get("dop_boost"))
    reward_distance = float(form.get("reward_distance"))
    speed_factor = float(form.get("speed_factor"))
    dragonfly_x = int(form.get("dragonfly_x"))
    dragonfly_y = int(form.get("dragonfly_x"))
    fromAnim = bool(form.get("from_animation"))
    description = form.get("description")
    _id = a_s.run_simulation_preprocessor(N=N,
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
                                          fromAnim=fromAnim,
                                          SPEED_FACTOR=speed_factor,
                                          dragonfly_start=[dragonfly_x,
                                                           dragonfly_y, 0.0],
                                          description=description)
    bottle.redirect("/action_selection/simulation/" + str(_id))


@route('/action_selection/simulations')
def show_action_selection_simulations():
    obj = dict()
    obj['simulations'] = a_s.get_simulations(50)
    return bottle.template('action_selection_simulations', obj)


@get("/action_selection/simulation/<_id>")
def show_action_selection_simulation(_id):

    sim = a_s.get_simulation(_id)

    if sim is None:
        bottle.redirect("/")

    obj = dict()
    obj['simulation'] = sim
    return bottle.template("action_selection_simulation", obj)

# Static Routes
# =============
@get('/static/<tool>/<folder>/<filename>')
def static_three_level(filename, folder, tool):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "static",
                                        tool,
                                        folder))
    return bottle.static_file(filename, root=root)


@get('/static/<tool>/<folder>/<subfolder>/<filename>')
def static_four_level(filename, subfolder, folder, tool):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "static",
                                        tool,
                                        folder,
                                        subfolder))
    return bottle.static_file(filename, root=root)


@get('/static/<filename>')
def static_one_level(filename):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
    return bottle.static_file(filename, root=root)


@get('/assets/<folder>/<filename>')
def assets(filename, folder):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "assets",
                                        folder))
    return bottle.static_file(filename, root=root)


def start():
    bottle.run(host="localhost",
               port=8082,
               reloader=True)


def connect_db(db_name="anisopter"):
    global db, simulations, samples, animations, cstmd, estmd, a_s
    host = "localhost"
    port = 27017
    connection = pymongo.MongoClient(host=host, port=port)
    db = connection[db_name]

    # Data Access Objects.
    animations = animation_dao.AnimationDao(db)
    estmd = estmd_dao.EstmdDao(db)
    cstmd = cstmd_dao.CstmdDao(db)
    a_s = action_selection_dao.ActionSelectionDao(db)
    simulations = simulation_dao.SimulationDao(db)
    samples = sample_dao.SampleDao(db)

if __name__ == "__main__":
    connect_db("anisopter")
    start()
else:
    # Run bottle in application mode.
    connect_db("anisopter")
    app = application = bottle.default_app()