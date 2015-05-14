<!DOCTYPE html>
<html>
% include('head.tpl', title="Training")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>Training</h1>
            <p>
                Lorem ipsum...
            </p>
            <a href="/training/simulations" class="h2">Training Sets</a>
            <p>
                Create new trainings and stuff.
            </p>
        </div>
    </div>
</div>
<br />
<br />
<div class="row">
    <div class="col-md-12">
        <div class="row">
            <div class="col-md-12 text-center">
                <button type="button"
                        onclick="window.location.href='/training/simulations/new'"
                        class="btn btn-lg btn-primary">New Training Simulation</button>
            </div>
        </div>
    </div>
</div>
% include('footer.tpl')
</body>
</html>