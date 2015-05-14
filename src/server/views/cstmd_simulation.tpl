<!DOCTYPE html>
<html>
% include('head.tpl', title="CSTMD1 Simulation")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Simulation</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/cstmd/simulation/new'"
                    class="btn btn-primary">New Simulation</button>
        </div>
    </div>
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
    <h2>Graphs</h2>
    <h3>Compartmental Activity</h3>
    <div class="row">
        % for i in range(simulation['num_plots']):
        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12 text-center">
            <img class="img-responsive"
                 src="/assets/cstmd/{{simulation['_id']}}/{{i}}.png" />
        </div>
        % end
    </div>
    <h3>Firing Rate</h3>
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center">
            <img class="img-responsive"
                 src="/assets/cstmd/{{simulation['_id']}}/{{simulation['num_plots']}}.png" />
        </div>
    </div>
</div>
</body>
</html>