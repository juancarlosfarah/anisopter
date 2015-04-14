<!DOCTYPE html>
<html>
% include('head.tpl', title="New Animation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Animation</h2>

    <form action="/target_animation/animation/generate" method="post">
        <div class="form-group">
            <label for="width">Width</label>
            <div class="input-group">
                <input type="number" class="form-control" id="width"
                       name="duration" placeholder="640" max="1000" />
                <span class="input-group-addon">px</span>
            </div>
        </div>
        <div class="form-group">
            <label for="num_neurons">Height</label>
            <div class="input-group">
              <input type="number" class="form-control" id="height"
                     name="height" placeholder="480" max="1000" />
              <span class="input-group-addon">px</span>
            </div>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>
        <div class="form-group">
            <label for="num_targets">Number of Targets</label>
            <input type="number" class="form-control"
                   name="num_targets" placeholder="1" id="num_targets" />
        </div>
        <button type="button" id="addTargets" class="btn btn-default">Add Targets</button>
        <button type="submit" class="btn btn-default">Submit</button>
    </form>
</div>
<script>
    $(document).ready(function() {
        $("#addTargets").click(function() {
            // Add form for targets.

        });
    });
</script>
</body>
</html>