<!DOCTYPE html>
<html>
% include('head.tpl', title="Training sets")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Training sets</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/training/simulations/new'"
                    class="btn btn-primary">New Training set</button>
        </div>
    </div>

    <table class="table">
        <tr>
            <th>Date</th>
            <th>Description</th>
        </tr>
        %for a in training:
        <tr>
            <td><a href="/training/simulation/{{a['_id']}}">{{a['date']}}</a></td>
            <td><a href="/training/simulation/{{a['_id']}}">{{a['description']}}</a></td>
        </tr>
        %end
    </table>

</div>
</body>
</html>