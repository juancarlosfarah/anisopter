<!DOCTYPE html>
<html>
% include('head.tpl', title="CSTMD1 Simulations")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Simulations</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/cstmd/simulation/new'"
                    class="btn btn-primary">New Simulation</button>
        </div>
    </div>


    <table class="table">
        <tr>
            <th>Date</th>
            <th>Number of Neurons</th>
            <th>Number of Electrodes</th>
            <th>Duration</th>
            <th>Description</th>
        </tr>
        %for s in simulations:
        <tr>
            <td>
                <a href="/cstmd/simulation/{{s['_id']}}">
                    {{s['date']}}
                </a>
            </td>
            <td>
                <a href="/cstmd/simulation/{{s['_id']}}">
                    {{s['num_neurons']}}
                </a>
            </td>
            <td>
                <a href="/cstmd/simulation/{{s['_id']}}">
                    {{s['num_electrodes']}}
                </a>
            </td>
            <td>
                <a href="/cstmd/simulation/{{s['_id']}}">
                    {{s['duration']}}
                </a>
            </td>
            <td>
                <a href="/cstmd/simulation/{{s['_id']}}">
                    {{s['description']}}
                </a>
            </td>
        </tr>
        %end
    </table>
</div>
</body>
</html>