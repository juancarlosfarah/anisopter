<!DOCTYPE html>
<html>
% include('head.tpl', title="CSTMD1 Simulation")
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
            <td>Number of Neurons</td>
            <td>{{simulation['num_neurons']}}</td>
        </tr>
        <tr>
            <td>Number of Pixels</td>
            <td>{{simulation['num_pixels']}}</td>
        </tr>
        <tr>
            <td>Number of Electrodes</td>
            <td>{{simulation['num_electrodes']}}</td>
        </tr>
        <tr>
            <td>Number of Synapses</td>
            <td>{{simulation['num_synapses']}}</td>
        </tr>
        <tr>
            <td>Synaptic Distance</td>
            <td>{{simulation['synaptic_distance']}}</td>
        </tr>
        <tr>
            <td>Description</td>
            <td>{{simulation['description']}}</td>
        </tr>
        <tr>
            <td>Max Current</td>
            <td>{{simulation['max_current']}}</td>
        </tr>
        <tr>
            <td>Min Current</td>
            <td>{{simulation['min_current']}}</td>
        </tr>
        <tr>
            <td>Max Weight</td>
            <td>{{simulation['max_weight']}}</td>
        </tr>
        <tr>
            <td>Min Weight</td>
            <td>{{simulation['min_weight']}}</td>
        </tr>
        <tr>
            <td>Duration</td>
            <td>{{simulation['duration']}} ms</td>
        </tr>
        <tr>
            <td>Potassium Level</td>
            <td>{{simulation['potassium']}}</td>
        </tr>
        <tr>
            <td>Sodium Level</td>
            <td>{{simulation['sodium']}}</td>
        </tr>
    </table>
</div>
</body>
</html>