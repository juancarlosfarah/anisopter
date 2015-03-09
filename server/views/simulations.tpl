<!DOCTYPE html>
<html>
% include('head.tpl', title="Simulations")
<body>
% include('header.tpl')
<div class="container">
<h1>Simulations</h1>
<table class="table">
    <tr>
        <th>Date</th>
        <th>Description</th>
        <th>Number of Neurons</th>
        <th>Number of Afferents</th>
        <th>Duration</th>
    </tr>
    %for s in simulations:
    <tr>
        <td><a href="/simulation/{{s['_id']}}">{{s['date']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['description']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['num_neurons']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['num_afferents']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['duration']}}</a></td>
    </tr>
    %end
</table>

</div>
</body>
</html>