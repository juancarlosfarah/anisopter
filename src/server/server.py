__author__ = 'juancarlosfarah'
__authoremail__ = 'juancarlos.farah14@imperial.ac.uk'

import sys
from optparse import OptionParser

import os
import bottle
from bottle import route, post, get, template, request
import pymongo
import numpy as np
import simulation_dao
import sample_dao
import animation_dao
import estmd_dao
import cstmd_dao
import action_selection_dao
import training_dao
from bson.objectid import ObjectId

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
    bg_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "assets",
                                           "backgrounds"))
    bgs = os.listdir(bg_path)
    obj = dict()
    obj['bgs'] = bgs
    return bottle.template('new_animation', obj)


@route('/target_animation/animations')
def show_animations():

    obj = dict()
    obj['animations'] = animations.get_animations(50)
    return bottle.template('animations', obj)

@post('/target_animation/remove')
def remove_animation():
    form = bottle.request.forms
    _id = form.get("_id")
    animations.remove(_id)

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
    background = request.json['background']
    background_speed = int(request.json['background_speed'])
    width = int(request.json['width'])
    height = int(request.json['height'])
    description = request.json['description']
    targets = request.json['targets']
    frames = int(request.json['frames'])
    _id = animations.generate_animation(width, height, description,
                                        targets, frames, background, 
                                        background_speed)
    rvalue = {"url": "/target_animation/animation/" + str(_id)}
    return rvalue


@route('/target_animation/background/new')
def new_animation_background():

    obj = dict()
    return bottle.template('new_animation_background', obj)


@post('/target_animation/background/upload')
def upload_animation_background():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed."

    filename = str(ObjectId()) + ext
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             "assets",
                                             "backgrounds"))
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=filename)
    upload.save(file_path)

    bottle.redirect("/target_animation/backgrounds")


@route('/target_animation/backgrounds')
def show_backgrounds():
    bg_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "assets",
                                           "backgrounds"))
    bgs = os.listdir(bg_path)
    obj = dict()
    obj['bgs'] = bgs
    return template('backgrounds', obj)


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
    H_filter = form.get("H_filter")
    b = form.get("b")
    a = form.get("a")
    CSKernel = form.get("CSKernel")
    b1 = form.get("b1")
    a1 = form.get("a1")

    _id = estmd.run_simulation(sample_id, description, H_filter, b, a,
                               CSKernel, b1, a1)
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
    obj['simulations'] = simulations.get_simulations(50)
    obj['samples'] = samples.get_samples(50)
    obj['cstmd'] = cstmd.get_simulations(50)
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
    weights_id = form.get("weights")
    is_training = form.get("training")
    a_ratio = a_minus / a_plus

    # Get sample.
    sample = samples.get_sample(sample_id)

    # Get weights from previous simulation.
    if weights_id != "none":
        sim = simulations.get_simulation(weights_id)
        weights = []

        for neuron in sim['neurons']:
            weights.append(neuron['weights'])
    else:
        weights = None

    # Toggle training.
    if is_training == "true":
        is_training = True
    else:
        is_training = False

    # If no sample is found, perhaps it's a CSTMD simulation.
    if sample is None:
        sample = cstmd.get_simulation(sample_id)

    spikes = samples.get_spikes(sample_id)
    _id = simulations.run_simulation(sample, spikes, num_neurons,
                                     description, a_plus, a_ratio, theta,
                                     weights, is_training)
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
    obj['simulations'] = a_s.get_simulations(50)
    obj['inputs'] = simulations.get_simulations(50, True)
    return bottle.template('new_action_selection_simulation', obj)


@post('/action_selection/simulation/run')
def run_action_selection_simulation():

    # Number of neurons fixed at 4.
    N = 4

    # Retrieve form and values.
    form = bottle.request.forms
    input_id = form.get("input")
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
    description = form.get("description")
    weights_id = form.get("weights")
    training = form.get("training")

    if weights_id != "none":
        sim = a_s.get_simulation(weights_id)
        weights = None
        if "weights" in sim:
            weights = np.array(sim.weights)
    else:
        weights = None

    if training == "true":
        is_training = True
    else:
        is_training = False

    if input_id != "random":
        sim = simulations.get_simulation(input_id)
        pattern_input = []
        pattern_duration = sim['duration']
        animation_id = sim['animation_id']

        for neuron in sim['neurons']:
            pattern_input.append(neuron['spike_times'])

    else:
        animation_id = None
        pattern_input = None
        pattern_duration = None

    if animation_id is not None:
        a = animations.get_animation(animation_id)
        animation = animations.generate_animation(a['width'],
                                                  a['height'],
                                                  a['description'],
                                                  a['targets'],
                                                  a['num_frames'],
                                                  a['background_id'],
                                                  a['background_speed'],
                                                  return_object=True)
    else:
        animation = None

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
                                          animation=animation,
                                          pattern_input=pattern_input,
                                          pattern_duration=pattern_duration,
                                          SPEED_FACTOR=speed_factor,
                                          dragonfly_start=[dragonfly_x,
                                                           dragonfly_y, 0.0],
                                          description=description,
                                          training=is_training,
                                          saved_weights=weights)
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


# Training
# ========
################################################################################
################################################################################
################################################################################

@route('/training')
def show_as():
    obj = dict()
    return bottle.template('training', obj)


@route('/training/simulations')
def show_training_simulations():
    obj = dict()
    obj['training'] = training.get_simulations(50)
    return bottle.template('training_simulations', obj)


@get("/training/simulations/new")
def new_training_simulation():
    obj = dict()
    obj['inputs'] = estmd.get_simulations(50)
    return bottle.template('new_training_simulation', obj)


@post('/training/simulations/generate')
def generate_simulation():

    # Retrieve form and values.
    form = bottle.request.forms

    input_id = form.get("input")
    n = int(form.get("repetitions"))
    v = int(form.get("vertical"))
    h = int(form.get("horizontal"))
    d = int(form.get("diagonal"))
    ad = int(form.get("anti_diagonal"))

    _id = training.generate_training_simulation(input_id, [v, h, d, ad], n)
    bottle.redirect("/training/simulation/" + str(_id))


@get("/training/simulation/<_id>")
def show_training_simulation(_id):

    tr = training.get_simulation(_id)

    if tr is None:
        bottle.redirect("/")

    obj = dict()
    obj['training'] = tr
    return bottle.template("training_simulation", obj)

################################################################################
################################################################################
################################################################################

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


@get('/assets/<folder>/<subfolder>/<filename>')
def assets_two_level(filename, subfolder, folder):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "assets",
                                        folder,
                                        subfolder))
    return bottle.static_file(filename, root=root)


def start():
    bottle.run(host="localhost",
               port=8092)


def connect_db(db_name="anisopter"):
    global db, simulations, samples, animations, cstmd, estmd, a_s, training
    host = "146.169.47.184"
    port = 27017
    connection = pymongo.MongoClient(host=host, port=port)
    db = connection[db_name]

    # Data Access Objects.
    animations = animation_dao.AnimationDao(db)
    estmd = estmd_dao.EstmdDao(db)
    a_s = action_selection_dao.ActionSelectionDao(db)
    simulations = simulation_dao.SimulationDao(db)
    samples = sample_dao.SampleDao(db)
    training = training_dao.TrainingDao(db)


if __name__ == "__main__":
    connect_db("anisopter")
    start()
else:
    # Run bottle in application mode.
    connect_db("anisopter")
    app = application = bottle.default_app()
