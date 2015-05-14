<!DOCTYPE html>
<html>
% include('head.tpl', title="Action Selection")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>Training</h1>
            <p>
                Lorem ipsum...
            </p>
            <a href="/training/training_sets" class="h2">Training sets</a>
            <p>
                Create new trainings and stuff.
            </p>
        </div>
    </div>

    <table class="table">
        <tr>
            <th>Date</th>
            <th>Description</th>
        </tr>
        %for a in trainings:
        <tr>
            <td><a href="/training/training_set/{{a['_id']}}">{{a['date']}}</a></td>
            <td><a href="/training/training_set/{{a['_id']}}">{{a['description']}}</a></td>
        </tr>
        %end
    </table>

</div>
</body>
</html>