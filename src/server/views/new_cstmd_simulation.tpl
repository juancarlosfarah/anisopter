<!DOCTYPE html>
<html>
% include('head.tpl', title="New CSTMD1 Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New CSTMD1 Simulation</h2>

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
            <label for="sample">Number of Neurons</label>
            <input class="form-control" type="number" max="5" min="1"
                   id="num_neurons" name="num_neurons"
                   placeholder="Number of Neurons (1 to 5)"/>
        </div>
        <div class="form-group">
            <label for="num_electrodes">Number of Electrodes</label>
            <input class="form-control" type="number" id="num_electrodes"
                   name="a_plus" min="1" max="500"
                   placeholder="Number of Electrodes (1 to 500)"/>
        </div>
        <div class="form-group">
            <label for="sample">Duration</label>
            <input class="form-control" type="number" max="5000" min="1"
                   id="duration" name="duration"
                   placeholder="Number of Neurons (1 to 5000)"/>
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