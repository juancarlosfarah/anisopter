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
        <div class="col-md-2">
            <form action="/estmd/remove" method="post">
                <input type="hidden" name="_id" value="{{simulation['_id']}}" />
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6 col-sm-12 text-center">
            <h3>Input</h3>
            <video width="480" height="360" autoplay loop>
                <source src="/assets/animations/{{simulation['animation_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="col-md-6 col-sm-12 text-center">
            <h3>Output</h3>
            <video width="480" height="360" autoplay loop>
                <source src="/assets/estmd/{{simulation['_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
    <br />
    <h3>Properties</h3>
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
        <tr>
            <td>H Filter</td>
            <td>{{simulation['h_filter']}}</td>
        </tr>
        <tr>
            <td>b</td>
            <td>{{simulation['b']}}</td>
        </tr>
        <tr>
            <td>a</td>
            <td>{{simulation['a']}}</td>
        </tr>
        <tr>
            <td>CS Kernel</td>
            <td>
                [
                % for row in simulation['cs_kernel']:
                [
                % for entry in row:
                {{'%.3f' % entry}}
                % end
                ]
                % end
                ]
            </td>
        </tr>
        <tr>
            <td>b1</td>
            <td>{{simulation['b1']}}</td>
        </tr>
        <tr>
            <td>a</td>
            <td>{{simulation['a1']}}</td>
        </tr>
    </table>
</div>
% include('footer.tpl')
</body>
</html>
