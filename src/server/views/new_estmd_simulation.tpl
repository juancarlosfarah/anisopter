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

        <div class="form-group optional">
            <label for="H_filter">H_filter</label>
            <textarea class="form-control" rows="5" id="H_filter"
                      name="H_filter">
            [[-1, -1, -1, -1, -1],
             [-1,  0,  0,  0, -1],
             [-1,  0,  2,  0, -1],
             [-1,  0,  0,  0, -1],
             [-1, -1, -1, -1, -1]]</textarea>
        </div>

        <div class="form-group optional">
            <label for="b">b</label>
            <textarea class="form-control" rows="1" id="b"
                      name="b">
            [0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]</textarea>
        </div>

        <div class="form-group optional">
            <label for="a">a</label>
            <textarea class="form-control" rows="1" id="a"
                      name="a">
            [1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]</textarea>
        </div>

        <div class="form-group optional">
            <label for="CSKernel">CSKernel</label>
            <textarea class="form-control" rows="3" id="CSKernel"
                      name="CSKernel">
            [[-1.0 / 9.0, -1.0 / 9.0, -1.0 / 9.0],
             [-1.0 / 9.0,  8.0 / 9.0, -1.0 / 9.0],
             [-1.0 / 9.0, -1.0 / 9.0, -1.0 / 9.0]]</textarea>
        </div>

        <div class="form-group optional">
            <label for="b1">b1</label>
            <textarea class="form-control" rows="1" id="b1"
                      name="b1">
            [1.0, 1.0] </textarea>
        </div>

        <div class="form-group optional">
            <label for="a1">a1</label>
            <textarea class="form-control" rows="1" id="a1"
                      name="a1">
            [51.0, -49.0]</textarea>
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
