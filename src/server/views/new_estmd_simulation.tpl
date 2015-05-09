<!DOCTYPE html>
<html>
% include('head.tpl', title="New ESTMD Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New ESTMD Simulation</h2>
    <form action="/estmd/simulation/run" method="post">
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
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
    </form>
</div>
</body>
</html>