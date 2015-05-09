<!DOCTYPE html>
<html>
% include('head.tpl', title="Action Selection Simulation")
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
            <td>Tau M</td>
            <td>{{simulation['tau_m']}}</td>
        </tr>
        <tr>
            <td>Tau Pre</td>
            <td>{{simulation['tau_pre']}}</td>
        </tr>
        <tr>
            <td>Tau Post</td>
            <td>{{simulation['tau_post']}}</td>
        </tr>
        <tr>
            <td>Synaptic Distance</td>
            <td>{{simulation['tau_c']}}</td>
        </tr>
        <tr>
            <td>Description</td>
            <td>{{simulation['description']}}</td>
        </tr>
        <tr>
            <td>Tau Dopamine</td>
            <td>{{simulation['tau_dop']}}</td>
        </tr>
        <tr>
            <td>Tau E</td>
            <td>{{simulation['tau_e']}}</td>
        </tr>
        <tr>
            <td>Reward Distance</td>
            <td>{{simulation['reward_disctance']}}</td>
        </tr>
        <tr>
            <td>Speed Factor</td>
            <td>{{simulation['speed_factor']}}</td>
        </tr>
        <tr>
            <td>Duration</td>
            <td>{{simulation['duration']}} ms</td>
        </tr>
        <tr>
            <td>Dopamine Boost</td>
            <td>{{simulation['dop_boost']}}</td>
        </tr>
        <tr>
            <td>Frame Length</td>
            <td>{{simulation['frame_length']}}</td>
        </tr>
    </table>
</div>
</body>
</html>