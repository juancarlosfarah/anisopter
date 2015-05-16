<!DOCTYPE html>
<html>
% include('head.tpl', title="Training set")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Animation</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/training/simulations/new'"
                    class="btn btn-primary">New Training</button>
        </div>
        <div class="col-md-2">
            <form action="/training/remove" method="post">
                <input type="hidden" name="_id" value="{{training['_id']}}" />
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
    </div>
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Training ID</td>
            <td>{{training['_id']}}</td>
        </tr>
        <tr>
            <td>Description</td>
            <td>{{training['description']}}</td>
        </tr>
    </table>
    <h2>Training set</h2>
</div>
% include('footer.tpl')
</body>
</html>