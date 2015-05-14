<!DOCTYPE html>
<html>
% include('head.tpl', title="New Pattern Recognition Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Simulation</h2>

    <form action="/pattern_recognition/simulation/run" method="post">
        <div class="form-group">
            <label for="sample">Sample</label>
            <select class="form-control" name="sample" id="sample">
                <option disabled="disabled">--- Samples ---</option>
                %for s in samples:
                    <option value="{{s['_id']}}">
                        Efferents: {{s['num_efferents']}}
                        Duration: {{s['duration']}}
                    </option>
                %end
                <option disabled="disabled">--- CSTMD ---</option>
                %for s in cstmd:
                    <option value="{{s['_id']}}">
                        Efferents: {{s['num_efferents']}}
                        Duration: {{s['duration']}}
                    </option>
                %end
            </select>
        </div>
        <div class="form-group">
            <label for="sample">Number of Post-Synaptic Neurons</label>
            <input class="form-control" type="number" max="5" min="1"
                   id="num_neurons" name="num_neurons"
		   value="1"
                   placeholder="Number of Neurons (1 to 5)"/>
        </div>
        <div class="form-group optional">
            <label for="a_plus">A Plus</label>
            <input class="form-control" type="text" id="a_plus"
		   value="0.03125"
                   name="a_plus" placeholder="A Plus"/>
        </div>
        <div class="form-group optional">
            <label for="a_minus">A Minus</label>
            <input class="form-control" type="text" id="a_minus"
		   value="0.028375"
                   name="a_minus" placeholder="A Minus"/>
        </div>
        <div class="form-group optional">
            <label for="theta">Theta</label>
            <input class="form-control" type="text" id="theta"
		   value="125"
                   name="theta" placeholder="Theta"/>
        </div>
        <div class="form-group optional">
            <label for="weights">Weights</label>
            <select class="form-control" name="weights" id="weights">
                <option value="none" selected>None</option>
                <option disabled="disabled">--- Saved Weights ---</option>
                %for s in simulations:
                <option value="{{s['_id']}}">
                    Date: {{s['date']}},
                    Neurons: {{s['num_neurons']}},
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
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>
        <button type="reset" class="btn btn-warning">Reset Defaults</button>

        <button id="submit"
                type="submit"
                class="btn btn-success">Run</button>
    </form>
</div>
% include('footer.tpl')
</body>
</html>
