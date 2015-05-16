<!DOCTYPE html>
<html>
% include('head.tpl', title="Animation")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Animation</h1>
        </div>
        <div class="col-md-2">
            <form action="/target_animation/remove" method="post">
                <input type="hidden" name="_id" value="{{animation['_id']}}" />
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
        <div class="col-md-2">
            <form action="/target_animation/remove" method="post">
                <input type="hidden" name="_id" value="{{animation['_id']}}" />
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
    </div>
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
% include('footer.tpl')
</body>
</html>