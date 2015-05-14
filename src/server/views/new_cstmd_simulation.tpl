<!DOCTYPE html>
<html>
% include('head.tpl', title="New CSTMD Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New CSTMD Simulation</h2>

    <form action="/cstmd/simulation/run" method="post">
        <div class="form-group">
            <label for="sample">Sample</label>
            <select class="form-control" name="sample" id="sample">
                %for s in samples:
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
		   value="5"
                   placeholder="Number of Neurons (1 to 5)"/>
        </div>
        <div class="form-group">
            <label for="num_electrodes">Number of Electrodes</label>
            <input class="form-control" type="number" id="num_electrodes"
                   name="num_electrodes" min="1" max="500"
		   value="50"
                   placeholder="Number of Electrodes (1 to 500)"/>
        </div>
        <div class="form-group">
            <label for="num_synapses">Number of Synapses</label>
            <input class="form-control" type="number" id="num_synapses"
                   name="num_synapses" min="1" max="500"
		   value="300"
                   placeholder="Number of Synapses (1 to 500)"/>
        </div>
        <div class="form-group">
            <label for="synaptic_distance">Synaptic Distance</label>
            <input class="form-control" type="number" id="synaptic_distance"
                   name="synaptic_distance" min="1" max="50"
		   value="30"
                   placeholder="Synaptic Distance (1 to 50)"/>
        </div>
        <div class="form-group">
            <label for="duration_per_frame">Duration per Frame</label>
            <div class="input-group">
                <input class="form-control" type="number" max="100" min="1"
                       id="duration_per_frame"
                       name="duration_per_frame"
		       value="10"
                       placeholder="Duration per Frame"/>
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
