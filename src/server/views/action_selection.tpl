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
                Lorem ipsum...
            </p>
            <a href="/action_selection/simulations" class="h2">Simulations</a>
            <p>
                Given input from the pattern recognition neurons...
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