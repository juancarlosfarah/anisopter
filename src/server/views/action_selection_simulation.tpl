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
            <td>{{simulation['reward_distance']}}</td>
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
    <h2>Animation</h2>
    <div class="row">
        <div class="col-md-12 text-center">
            <video width="640" height="480" autoplay loop>
                <source src="/assets/action_selection/{{simulation['_id']}}/{{simulation['_id']}}.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
    <h2>Graphs</h2>
    <div class="row">
        % for i in range(1, 13):
        <div class="col-lg-4 col-md-4 col-sm-6 col-xs-12 text-center">
            <img class="img-responsive" src="/assets/action_selection/{{simulation['_id']}}/{{i}}.png" />
        </div>
        % end
    </div>
</div>
% include('footer.tpl')
</body>
</html>