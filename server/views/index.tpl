<!DOCTYPE html>
<html>
<head>
    <title>Anisopter</title>
    <script src="/static/jquery.js"></script>
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet"
          media="screen">
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
    <script>
        (function(i,s,o,g,r,a,m) {
            i['GoogleAnalyticsObject']=r;
            i[r]=i[r]||function() {
                (i[r].q=i[r].q||[]).push(arguments)
            }, i[r].l=1*new Date();
            a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];
            a.async=1;
            a.src=g;
            m.parentNode.insertBefore(a,m)
        })(window, document,
           'script','//www.google-analytics.com/analytics.js','ga');
        ga('create', 'UA-60448221-1', 'auto');
        ga('send', 'pageview');
    </script>
</head>
<body>
<header>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">
        Home
      </a>
    </div>
  </div>
</nav>
</header>
<div class="container">
<h1>Simulations</h1>
<table class="table">
    <tr>
        <th>Date</th>
        <th>Description</th>
        <th>Number of Neurons</th>
        <th>Number of Afferents</th>
        <th>Duration</th>
    </tr>
    %for s in simulations:
    <tr>
        <td><a href="/simulation/{{s['_id']}}">{{s['date']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['description']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['num_neurons']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['num_afferents']}}</a></td>
        <td><a href="/simulation/{{s['_id']}}">{{s['duration']}}</a></td>
    </tr>
    %end
</table>

</div>
</body>
</html>