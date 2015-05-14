<!DOCTYPE html>
<html>
% include('head.tpl', title="ESTMD Simulation")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Simulation</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/estmd/simulation/new'"
                    class="btn btn-primary">New Simulation</button>
        </div>
    </div>
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
    <div class="row">
        <div class="col-md-6 col-sm-12 text-center">
            <h3>Input</h3>
            <video width="640" height="480" autoplay loop>
                <source src="/assets/animations/{{simulation['animation_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="col-md-6 col-sm-12 text-center">
            <h3>Output</h3>
            <video width="640" height="480" autoplay loop>
                <source src="/assets/estmd/{{simulation['_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
</div>
</body>
</html>