<!DOCTYPE html>
<html>
% include('head.tpl', title="New Training Simulation")
<body>
% include('header.tpl')
<div class="container">
    % include('form_header.tpl', title="New Training Simulation")
    <form action="/training/simulations/generate" method="post">

        <div class="form-group">
            <label for="input">Action selection input</label>
            <select class="form-control" name="input" id="input">
                %for s in inputs:
                <option value="{{s['_id']}}">
                    ID: {{s['_id']}}
                </option>
                %end
            </select>
        </div>

        <div class="form-group">
            <label for="repetitions">Test repetitions</label>
            <div class="input-group">
                <input type="number" class="form-control" id="repetitions"
                       name="repetitions" value="10" max="100"/>
                <span class="input-group-addon">reps</span>
            </div>
        </div>

        <div class="form-group">
            <label for="vertical">Vertical tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="vertical"
                       name="vertical" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <div class="form-group">
            <label for="horizontal">Horizontal tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="horizontal"
                       name="horizontal" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <div class="form-group">
            <label for="diagonal">Diagonal tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="diagonal"
                       name="diagonal" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <div class="form-group">
            <label for="anti_diagonal">Anti-diagonal tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="anti_diagonal"
                       name="anti_diagonal" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <button type="submit"
                class="btn btn-success btn-default"
                id="submit">Submit</button>
    </form>
</div>
</body>
</html>
