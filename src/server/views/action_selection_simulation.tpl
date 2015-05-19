<!DOCTYPE html>
<html>
% include('head.tpl', title="Action Selection Simulation")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <h1>Action Selection</h1>
        </div>
        <div class="col-md-2 text-right">
            <button type="button"
                    onclick="window.location.href='/action_selection/simulation/new'"
                    class="btn btn-primary">New Simulation</button>
        </div>
        <div class="col-md-2 text-right">
            <form action="/action_selection/remove" method="post">
                <input type="hidden" name="_id" value="{{simulation['_id']}}" />
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
    </div>
    <p>
        Below you will find the results from your simulations. The distance
        between dragonfly’s focal point (which is initialised to some
        position at the start) and the nearest target is calculated. If the
        distance is within a preset distance, a dopamine boost is administered
        to the system. The movement of the dragonfly is calculated by
        translating the firing rate of each of the four neurons into the
        velocity of the focal point in the corresponding direction. The overall
        velocity and hence distance travelled for the time step was
        averaged between the four and the dragonfly position updated.
    </p>
    <h2>Key Metrics</h2>
    <div class="row">
        % for i in range(1, 13):
        <div class="col-lg-4 col-md-4 col-sm-6 col-xs-12 text-center">
            <img class="img-responsive" src="/assets/action_selection/{{simulation['_id']}}/{{i}}.png" />
        </div>
        % end
    </div>
    <h2>Animation</h2>
    <div class="row">
        <div class="col-md-12 text-center">
            <video width="640" height="480" autoplay loop>
                <source src="/assets/action_selection/{{simulation['_id']}}/{{simulation['_id']}}.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
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
</div>
% include('footer.tpl')
</body>
</html>