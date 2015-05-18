<!DOCTYPE html>
<html>
% include('head.tpl', title="New CSTMD1 Simulation")
<body>
% include('header.tpl')
<div class="container">
    % include('form_header.tpl', title="New CSTMD1 Simulation")
    <form action="/cstmd/simulation/run" method="post">
        <div class="form-group">
            <label for="sample">Sample</label>
            <select class="form-control" name="sample" id="sample">
                %for s in samples:
                    <option value="{{s['_id']}}">
                        Date: {{s['date']}}
                        Description: {{s['description']}}
                    </option>
                %end
            </select>
            <p class="help-block">
                Choose the appropriate results from the ESTMD module to run your simulation.
            </p>
        </div>
        <div class="form-group">
            <label for="num_neurons">Number of Neurons</label>
            <input class="form-control" type="number" max="5" min="2"
                   id="num_neurons" name="num_neurons"
		   value="5"
                   placeholder="Number of Neurons (2 to 5)"/>
            <p class="help-block">
                Choose the number of neurons to be used for the simulation.
            </p>
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
            <p class="help-block">
                The CSTMD1 simulation runs as many times as the frames given
                by the ESTMD module. Define for how many milliseconds will
                each CSTMD1 simulation run.
            </p>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
                <p class="help-block">
                    Please write an appropriate description for this simulation.
                </p>
        </div>
        <div class="form-group optional">
            <label for="num_electrodes">Number of Electrodes</label>
            <input class="form-control" type="number" id="num_electrodes"
                   name="num_electrodes" min="1" max="500"
		   value="50"
                   placeholder="Number of Electrodes (1 to 500)"/>
            <p class="help-block">
                Choose the number of electrodes which will record different compartments of the neurons and provide input to the Pattern Recognition module.
            </p>
        </div>
        <div class="form-group optional">
            <label for="num_synapses">Number of Synapses</label>
            <input class="form-control" type="number" id="num_synapses"
                   name="num_synapses" min="1" max="500"
		   value="300"
                   placeholder="Number of Synapses (1 to 500)"/>
            <p class="help-block">
                Choose the number of synapses to be created within the neurons.
            </p>
        </div>

        <div class="form-group optional">
            <label for="potassium">Potassium</label>
            <input class="form-control" type="text" id="potassium"
                   name="potassium" value="0.06"
                   placeholder="Potassium"/>
            <p class="help-block">
                Choose the Potassium level.
            </p>
        </div>
        <div class="form-group optional">
            <label for="sodium">Sodium</label>
            <input class="form-control" type="text" id="sodium"
                   name="sodium"
		    value="0.048"
                   placeholder="Sodium"/>
            <p class="help-block">
                Choose the Sodium level.
            </p>
        </div>
        <div class="form-group optional">
            <label for="max_current">Maximum current</label>
            <input class="form-control" type="text" id="max_current"
                   name="max_current"   value="30.0"
                   placeholder="Maximum current "/>
            <p class="help-block">
                Choose the the maximum current to be given as an input to the CSTMD1.
            </p>
        </div>
        <div class="form-group optional">
            <label for="min_current">Minimum current</label>
            <input class="form-control" type="text" id="min_current"
                   name="min_current"   value="2.0"
                   placeholder="Minimum current "/>
            <p class="help-block">
                Choose the the minimum current to be given as an input to the CSTMD1.
            </p>
        </div>
        <div class="form-group optional">
            <label for="max_weight">Maximum weight</label>
            <input class="form-control" type="text" id="max_weight"
                   name="max_weight"   value="0.00005"
                   placeholder="Maximum weight "/>
            <p class="help-block">
                Choose the the maximum weight for each ESTMD input to the CSTMD1.
            </p>
        </div>
        <div class="form-group optional">
            <label for="min_weight">Minimum weight</label>
            <input class="form-control" type="text" id="min_weight"
                   name="min_weight"   value="0.000005"
                   placeholder="Minimum weight "/>
            <p class="help-block">
                Choose the the minimum weight for each ESTMD input to the CSTMD1.
            </p>
        </div>
        <div class="form-group optional">
            <label for="synaptic_distance">Synaptic Distance</label>
            <input class="form-control" type="number" id="synaptic_distance"
                   name="synaptic_distance" min="1" max="50"
		   value="30"
                   placeholder="Synaptic Distance (1 to 50)"/>
            <p class="help-block">
                Choose the appropriate synaptic distance to be established for the synapses of the neurons.
            </p>
        </div>
        <button type="reset"
                class="btn btn-warning">Reset Defaults</button>

        <button id="submit"
                type="submit"
                class="btn btn-success">Run</button>
    </form>
</div>
</body>
% include('footer.tpl')
</html>
