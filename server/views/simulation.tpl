<!DOCTYPE html>
<html
<head>
<title>Simulation</title>
<script src="/static/jquery.js"></script>
<link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet"
media="screen">
<script src="/static/bootstrap/js/bootstrap.min.js"></script>
</head>
<body>
<header>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="/">
        Home
      </a>
    </div>
  </div>
</nav>
</header>

<div class="container">
<h2>Simulation Data</h2>
<table class="table">
    <tr>
        <td>Simulation ID</td>
        <td>{{simulation['_id']}}</td>
    </tr>
    <tr>
        <td>Number of Neurons</td>
        <td>{{len(simulation['neurons'])}}</td>
    </tr>
    <tr>
        <td>Number of Afferents</td>
        <td>{{simulation['num_afferents']}}</td>
    </tr>
    <tr>
        <td>Number of Patterns</td>
        <td>{{len(simulation['start_positions'])}}</td>
    </tr>
    <tr>
        <td>Pattern Duration</td>
        <td>{{simulation['pattern_duration']}} ms</td>
    </tr>
    <tr>
        <td>Duration</td>
        <td>{{simulation['duration']}} ms</td>
    </tr>
</table>

%for p_plot in simulation['potential_plots']:
<div class="row">
    <div class="col-md-12">
        {{!p_plot}}
    </div>
</div>
%end

%for wd_plot in simulation['weight_distribution_plots']:
<div class="row">
    <div class="col-md-12">
        {{!wd_plot}}
    </div>
</div>
%end

</div>
</body>
</html>