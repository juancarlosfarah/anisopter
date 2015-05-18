<!DOCTYPE html>
<html>
% include('head.tpl', title="Pattern Recognition Sample")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <h1>Sample for Pattern Recognition</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/pattern_recognition/sample/new'"
                    class="btn btn-primary">New Sample</button>
        </div>
        <div class="col-md-2">
            <form action="/pattern_recognition/sample/remove" method="post">
                <input type="hidden" name="_id" value="{{sample['_id']}}" />
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
    </div>
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Sample ID</td>
            <td>{{sample['_id']}}</td>
        </tr>
        <tr>
            <td>Number of Efferents</td>
            <td>{{sample['num_efferents']}}</td>
        </tr>
        <tr>
            <td>Number of Patterns</td>
            <td>{{len(sample['start_positions'])}}</td>
        </tr>
        <tr>
            <td>Pattern Duration</td>
            <td>{{sample['pattern_duration']}} ms</td>
        </tr>
        <tr>
            <td>Duration</td>
            <td>{{sample['duration']}} ms</td>
        </tr>
    </table>
</div>
% include('footer.tpl')
</body>
</html>