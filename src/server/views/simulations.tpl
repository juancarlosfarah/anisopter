<!DOCTYPE html>
<html>
% include('head.tpl', title="Pattern Recognition Simulations")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Simulations</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/pattern_recognition/simulation/new'"
                    class="btn btn-primary">New Simulation</button>
        </div>
    </div>


    <table class="table">
        <tr>
            <th>Date</th>
            <th>Number of Neurons</th>
            <th>Number of Afferents</th>
            <th>Duration</th>
            <th>Description</th>
            <th>Action</th>
        </tr>
        %for s in simulations:
        <tr>
            <td>
                <a href="/pattern_recognition/simulation/{{s['_id']}}">
                    {{s['date']}}
                </a>
            </td>
            <td>
                <a href="/pattern_recognition/simulation/{{s['_id']}}">
                    {{s['num_neurons']}}
                </a>
            </td>
            <td>
                <a href="/pattern_recognition/simulation/{{s['_id']}}">
                    {{s['num_afferents']}}
                </a>
            </td>
            <td>
                <a href="/pattern_recognition/simulation/{{s['_id']}}">
                    {{s['duration']}}
                </a>
            </td>
            <td>
                <a href="/pattern_recognition/simulation/{{s['_id']}}">
                    {{s['description']}}
                </a>
            </td>
            <td class="text-center">
                <form action="/pattern_recognition/simulation/remove" method="post">
                    <input type="hidden" name="_id" value="{{s['_id']}}" />
                    <button type="submit"
                            class="btn btn-xs btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        %end
    </table>
</div>
% include('footer.tpl')
</body>
</html>