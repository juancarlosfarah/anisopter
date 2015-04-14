<!DOCTYPE html>
<html>
% include('head.tpl', title="Animations")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Animations</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/target_animation/animation/new'"
                    class="btn btn-primary">New Animation</button>
        </div>
    </div>

    <table class="table">
        <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Background</th>
            <th>Number of Targets</th>
            <th>Duration</th>
        </tr>
        %for a in animations:
        <tr>
            <td><a href="/animation/{{a['_id']}}">{{a['date']}}</a></td>
            <td><a href="/animation/{{a['_id']}}">{{a['description']}}</a></td>
            <td><a href="/animation/{{a['_id']}}">{{a['background']}}</a></td>
            <td><a href="/animation/{{a['_id']}}">{{a['width']}}</a></td>
            <td><a href="/animation/{{a['_id']}}">{{a['height']}}</a></td>
            <td><a href="/animation/{{a['_id']}}">{{a['num_targets']}}</a></td>
            <td><a href="/animation/{{a['_id']}}">{{a['duration']}}</a></td>
        </tr>
        %end
    </table>
</div>
</body>
</html>