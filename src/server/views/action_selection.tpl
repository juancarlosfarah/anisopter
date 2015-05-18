<!DOCTYPE html>
<html>
% include('head.tpl', title="Action Selection")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>Action Selection</h1>
            <p>
                This module takes as input the spike trains from the
                pattern recognition neurons and the original target
                animation video. Its function is to select an action
                for the biomimetic agent at each time step given that
                input. Biologically, our model emulates the connection
                between the visual processing and the motor
                neurons. It can be trained using STDP combined with
                reward modulation so that the dragonfly learns to
                maximise target capture based on recurring patterns in
                its visual field. The final output is the original
                animation with the position of the dragonfly
                superimposed onto each frame for observation of how
                effectively it chases targets.
            </p>
            <a href="/action_selection/simulations" class="h2">Simulations</a>
            <p>
                Your action selection simulations.
            </p>
        </div>
    </div>
    <br />
    <br />
    <div class="row">
        <div class="col-md-12">
            <div class="row">
                <div class="col-md-12 text-center">
                    <button type="button"
                            onclick="window.location.href='/action_selection/simulation/new'"
                            class="btn btn-lg btn-primary">New Action Selection Simulation</button>
                </div>
            </div>
        </div>
    </div>
</div>
% include('footer.tpl')
</body>
</html>
