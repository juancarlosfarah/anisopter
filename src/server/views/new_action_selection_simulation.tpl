<!DOCTYPE html>
<html>
% include('head.tpl', title="New Action Selection Simulation")
<body>
% include('header.tpl')
<div class="container">
    % include('form_header.tpl', title="New Action Selection Simulation")
    <form action="/action_selection/simulation/run" method="post">
        <div class="form-group">
            <label for="input">Input</label>
            <select class="form-control" name="input" id="input">
                <option value="random" selected>Random</option>
                <option disabled="disabled">--- Input ---</option>
                %for s in inputs:
                    <option value="{{s['_id']}}">
                        Date: {{s['date']}},
                        Duration: {{s['duration']}},
                        Afferents: {{s['num_afferents']}},
                        Efferents: {{s['num_neurons']}}
                    </option>
                %end
            </select>
        </div>
        <div class="form-group">
            <label for="num_neurons">Number of Neurons</label>
            <input class="form-control" type="number" max="5" min="1"
                   id="num_neurons" name="num_neurons"
                   value="4" disabled/>
        </div>
        <div class="form-group">
            <label for="weights">Weights</label>
            <select class="form-control optional" name="weights" id="weights">
                <option value="none" selected>None</option>
                <option disabled="disabled">--- Saved Weights ---</option>
                %for s in simulations:
                <option value="{{s['_id']}}">
                    Date: {{s['date']}},
                    Description: {{s['description']}}
                </option>
                %end
            </select>
        </div>
        <div class="form-group">
            <div class="checkbox" id="training">
                <label>
                    <input type="checkbox" value="true" name="training" checked>
                    Training
                </label>
            </div>
        </div>
	    <div class="form-group">
            <label for="frame_length">Frame Length</label>
            <div class="input-group">
                <input class="form-control" type="text" id="frame_length"
                       name="frame_length" value="10.0" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="optional">
            <p>
                The values below are explained by the following equations:
            </p>
            <h4>Integrate-and-Fire Neurons:</h4>
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae0x.png"
                     alt="Formula" class="math-display" />
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae1x.png"
                     class="math-display">
            </div>
            <br />
            In the above equations,
            <em>v</em> is the membrane potential,
            <em>g</em>
            <sub><em class="small">e</em></sub> is the synaptic conductance,
            <em>E</em>
            <sub><em class="small">e</em></sub> and
            <em>E</em><sub>
            <em class="small">l</em></sub> are reverse potentials,
            <em>v</em><sub>
            <em class="small">r</em></sub> is the resting potential and
            <em>&#x03C4;</em><sub>
            <em>m</em></sub> is a time constant.
            <br /><br />
            <h4>Reward-modulated Synapses with STDP:</h4>
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae2x.png"
                        alt="Formula" class="math-display">
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae3x.png"
                     alt="Formula" class="math-display">
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae4x.png"
                     alt="Formula" class="math-display">
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae5x.png"
                     alt="Formula"
                     class="math-display">
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae6x.png"
                     alt="Formula"
                     class="math-display">
            </div>
            <br />
            <p>In the above equations,
            <em>w</em> is the weight of the synapse,
            <em>c</em> is the eligibility
            trace, <em>Dop</em> is the level of
            dopamine, <em>dApre</em> and <em>dApost</em> are
            variables that govern the STDP, and the <em>&#x03C4;</em>s are 
                    time constants.
            </p>
            <h4>Pre-Synaptic Neuron Updates:</h4>
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae7x.png"
                     alt="Formula"
                     class="math-display">
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae8x.png"
                     alt="Formula"
                class="math-display">
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae9x.png"
                     alt="Formula" class="math-display" />
            </div>
            <br />
            <h4>Post-Synaptic Neuron Updates:</h4>
            <p>
                When the post-synaptic neuron fires, the following updates are
                executed, where <em>Apre</em><sub>
                <em class="small">step</em></sub> and
                <em>Apost</em><sub>
                <em class="small">step</em></sub> are constants.
            </p>
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae10x.png"
                     alt="Formula"
                     class="math-display" />
            </div>
            <br />
            <div class="text-center">
                <img src="/assets/images/action_selection_formulae11x.png"
                     alt="Formula"
                     class="math-display">
            </div>
            <br />
        </div>
        <div class="form-group optional">
            <label for="tau_m">Tau M</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_m"
                       name="tau_m" value="10" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="tau_pre">Tau Pre</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_pre"
                       name="tau_pre" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="tau_post">Tau Post</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_post"
                       name="tau_post" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="tau_c">Tau C</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_c"
                       name="tau_c" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="tau_dop">Tau Dop</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_dop"
                       name="tau_dop" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="Ee">Ee</label>
            <div class="input-group">
                <input class="form-control" type="text" id="Ee"
                       name="Ee" value="0" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group optional">
            <label for="vt">vt</label>
            <div class="input-group">
                <input class="form-control" type="text" id="vt"
                       name="vt" value="-54" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group optional">
            <label for="vr">vr</label>
            <div class="input-group">
                <input class="form-control" type="text" id="vr"
                       name="vr" value="-60" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="El">El</label>
            <div class="input-group">
                <input class="form-control" type="text" id="El"
                       name="El" value="-74" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="dop_boost">Dopamine Boost</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dop_boost"
                       name="dop_boost" value="0.5" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group optional">
            <label for="tau_e">Tau E</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_e"
                       name="tau_e" value="5" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group optional">
            <label for="F">F</label>
            <div class="input-group">
                <input class="form-control" type="text" id="F"
                       name="F" value="15" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group optional">
            <label for="gmax">Max Weight</label>
            <div class="input-group">
                <input class="form-control" type="text" id="gmax"
                       name="gmax" value="1" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group optional">
            <label for="dApre">dApre</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dApre"
                       name="dApre" value="1" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="duration">Duration</label>
            <div class="input-group">
                <input class="form-control" type="text" id="duration"
                       name="duration" value="100.0" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="reward_distance">Reward Distance</label>
            <div class="input-group">
                <input class="form-control" type="text" id="reward_distance"
                       name="reward_distance" value="40" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="speed_factor">Speed Factor</label>
            <div class="input-group">
                <input class="form-control" type="text" id="speed_factor"
                       name="speed_factor" value="2" />
                <span class="input-group-addon">s</span>
            </div>
        </div>
	<div class="form-group">
            <label for="dragonfly_x">Dragonfly X Coordinate</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dragonfly_x"
                       name="dragonfly_x" value="300" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="dragonfly_y">Dragonfly Y Coordinate</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dragonfly_y"
                       name="dragonfly_y" value="300" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>
        <button type="reset"
                class="btn btn-warning">Reset Defaults</button>

        <button id="submit"
                type="submit"
                class="btn btn-success">Run</button>
    </form>
</div>
% include('footer.tpl')
</body>
</html>
