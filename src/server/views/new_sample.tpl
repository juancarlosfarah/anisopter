<!DOCTYPE html>
<html>
% include('head.tpl', title="New Pattern Recognition Sample")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Sample</h2>

    <form action="/pattern_recognition/sample/generate" method="post">
        <div class="form-group">
            <label for="duration">Duration</label>
            <div class="input-group">
                <input type="number" class="form-control" id="duration"
                       value="15000"
                       name="duration" placeholder="Duration">
                <span class="input-group-addon">ms</span>
            </div>
        </div>
        <div class="form-group">
            <label for="num_neurons">Number of Afferents</label>
            <input type="number" class="form-control" id="num_neurons"
                   value="500"
                   name="num_neurons" placeholder="Number of Afferents">
        </div>
        <div class="form-group">
            <label for="num_patterns">Number of Patterns</label>
            <input type="number" class="form-control" id="num_patterns"
                   value="1"
                   name="num_patterns" placeholder="Number of Patterns">
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
                class="btn btn-success">Generate</button>
    </form>
</div>
% include('footer.tpl')
</body>
</html>