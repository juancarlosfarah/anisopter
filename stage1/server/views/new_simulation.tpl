<!DOCTYPE html>
<html>
% include('head.tpl', title="New Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Simulation</h2>

    <form action="/simulation/run" method="post">
        <div class="form-group">
            <label for="sample">Sample</label>
            <select class="form-control" name="sample" id="sample">
                %for s in samples:
                    <option value="{{s['_id']}}">
                        Afferents: {{s['num_afferents']}}
                        Duration: {{s['duration']}}
                    </option>
                %end
            </select>
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