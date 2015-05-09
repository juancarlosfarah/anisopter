<!DOCTYPE html>
<html>
% include('head.tpl', title="Animation")
<body>
% include('header.tpl')
<div class="container">
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Animation ID</td>
            <td>{{animation['_id']}}</td>
        </tr>
        <tr>
            <td>Description</td>
            <td>{{animation['description']}}</td>
        </tr>
        <tr>
            <td>Number of Targets</td>
            <td>{{len(animation['targets'])}}</td>
        </tr>
        <tr>
            <td>Width</td>
            <td>{{animation['width']}}</td>
        </tr>
        <tr>
            <td>Height</td>
            <td>{{animation['height']}}</td>
        </tr>
    </table>
    <h2>Animation</h2>
    <div class="row">
        <div class="col-md-12 text-center">
            <video width="640" height="480" autoplay loop>
                <source src="/assets/animations/{{animation['_id']}}.mp4"
                        type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
</div>
</body>
</html>