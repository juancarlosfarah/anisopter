<!DOCTYPE html>
<html>
% include('head.tpl', title="Pattern Recognition Samples")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Samples</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/pattern_recognition/samples/new'"
                    class="btn btn-primary">New Sample</button>
        </div>
    </div>


    <table class="table">
        <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Number of Afferents</th>
            <th>Duration</th>
        </tr>
        %for s in samples:
        <tr>
            <td><a href="/pattern_recognition/sample/{{s['_id']}}">{{s['date']}}</a></td>
            <td><a href="/pattern_recognition/sample/{{s['_id']}}">{{s['description']}}</a></td>
            <td><a href="/pattern_recognition/sample/{{s['_id']}}">
                    {{s['num_efferents']}}
                </a>
            </td>
            <td><a href="/pattern_recognition/sample/{{s['_id']}}">{{s['duration']}}</a></td>
        </tr>
        %end
    </table>
</div>
% include('footer.tpl')
</body>
</html>