<!DOCTYPE html>
<html>
% include('head.tpl', title="New Sample")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Sample</h2>

    <form action="/sample/generate" method="post">
        <div class="form-group">
            <label for="duration">Duration</label>
            <input type="number" class="form-control" id="duration"
                   name="duration" placeholder="Duration">
        </div>
        <div class="form-group">
            <label for="num_neurons">Number of Afferents</label>
            <input type="number" class="form-control" id="num_neurons"
                   name="num_neurons" placeholder="Number of Afferents">
        </div>
        <div class="form-group">
            <label for="num_patterns">Number of Patterns</label>
            <input type="number" class="form-control" id="num_patterns"
                   name="num_patterns" placeholder="Number of Patterns">
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