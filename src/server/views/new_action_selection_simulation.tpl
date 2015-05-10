<!DOCTYPE html>
<html>
% include('head.tpl', title="New Action Selection Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Action Selection Simulation</h2>

    <form action="/action_selection/simulation/run" method="post">
        <div class="form-group">
            <label for="sample">Input</label>
            <select class="form-control" name="input" id="input">
                %for s in input:
                    <option value="{{s['_id']}}">
                        ID: {{s['_id']}}
                    </option>
                %end
            </select>
        </div>
        <div class="form-group">
            <label for="num_neurons">Number of Neurons</label>
            <input class="form-control" type="number" max="5" min="1"
                   id="num_neurons" name="num_neurons"
                   placeholder="Number of Neurons (1 to 5)"/>
        </div>
	<div class="form-group">
            <label for="frame_length">Frame Length</label>
            <div class="input-group">
                <input class="form-control" type="text" id="frame_length"
                       name="frame_length" value="10.0" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="tau_m">Tau M</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_m"
                       name="tau_m" value="10" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="tau_pre">Tau Pre</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_pre"
                       name="tau_pre" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="tau_post">Tau Post</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_post"
                       name="tau_post" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="tau_c">Tau C</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_c"
                       name="tau_c" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="tau_dop">Tau Dop</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_dop"
                       name="tau_dop" value="20" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="Ee">Ee</label>
            <div class="input-group">
                <input class="form-control" type="text" id="Ee"
                       name="Ee" value="0" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="vt">vt</label>
            <div class="input-group">
                <input class="form-control" type="text" id="vt"
                       name="vt" value="-54" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="vr">vr</label>
            <div class="input-group">
                <input class="form-control" type="text" id="vr"
                       name="vr" value="-60" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="El">El</label>
            <div class="input-group">
                <input class="form-control" type="text" id="El"
                       name="El" value="-74" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="dop_boost">Dopamine Boost</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dop_boost"
                       name="dop_boost" value="0.5" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="tau_e">Tau E</label>
            <div class="input-group">
                <input class="form-control" type="text" id="tau_e"
                       name="tau_e" value="5" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="F">F</label>
            <div class="input-group">
                <input class="form-control" type="text" id="F"
                       name="F" value="15" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="gmax">Max Weight</label>
            <div class="input-group">
                <input class="form-control" type="text" id="gmax"
                       name="gmax" value="1" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="dApre">dApre</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dApre"
                       name="dApre" value="1" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="duration">Duration</label>
            <div class="input-group">
                <input class="form-control" type="text" id="duration"
                       name="duration" value="100.0" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="reward_distance">Reward Distance</label>
            <div class="input-group">
                <input class="form-control" type="text" id="reward_distance"
                       name="reward_distance" value="40" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="from_animation">From Animation</label>
            <select class="form-control"
                    name="from_animation"
                    id="from_animation">
                <option value="1" selected>True</option>
                <option value="0">False</option>
            </select>
        </div>
        <div class="form-group">
            <label for="speed_factor">Speed Factor</label>
            <div class="input-group">
                <input class="form-control" type="text" id="speed_factor"
                       name="speed_factor" value="2" />
                <span class="input-group-addon">s</span>
            </div>
        </div>
	<div class="form-group">
            <label for="dragonfly_x">Dragonfly x coordinate</label>
            <div class="input-group">
                <input class="form-control" type="text" id="dragonfly_x"
                       name="dragonfly_x" value="300" />
                <span class="input-group-addon">ms</span>
            </div>
        </div>
	<div class="form-group">
            <label for="dragonfly_y">Dragonfly x coordinate</label>
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
        <button type="submit" class="btn btn-default">Submit</button>
    </form>
</div>
</body>
</html>
