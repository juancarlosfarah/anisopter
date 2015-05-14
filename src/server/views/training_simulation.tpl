<!DOCTYPE html>
<html>
% include('head.tpl', title="Training set")
<body>
% include('header.tpl')
<div class="container">
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
</body>
</html>