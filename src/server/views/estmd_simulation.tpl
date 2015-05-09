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
    <div class="row">
        <div class="col-md-6 col-sm-12 text-center">
            <h3>Input</h3>
            <video width="640" height="480" autoplay>
                <source src="/assets/animations/{{simulation['input_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="col-md-6 col-sm-12 text-center">
            <h3>Output</h3>
            <video width="640" height="480" autoplay>
                <source src="/assets/estmd/{{simulation['_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
</div>
</body>
</html>