<!DOCTYPE html>
<html>
% include('head.tpl', title="Pattern Recognition Sample")
<body>
% include('header.tpl')
<div class="container">
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Sample ID</td>
            <td>{{sample['_id']}}</td>
        </tr>
        <tr>
            <td>Number of Afferents</td>
            <td>{{sample['num_afferents']}}</td>
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
</body>
</html>