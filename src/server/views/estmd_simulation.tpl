<!DOCTYPE html>
<html>
% include('head.tpl', title="ESTMD Simulation")
<body>
% include('header.tpl')
<div class="container">
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Simulation ID</td>
            <td>{{simulation['_id']}}</td>
        </tr>
        <tr>
            <td>Date</td>
            <td>{{simulation['date']}}</td>
        </tr>
        <tr>
            <td>Description</td>
            <td>{{simulation['description']}}</td>
        </tr>
    </table>
</div>
</body>
</html>