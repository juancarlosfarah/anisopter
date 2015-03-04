<!DOCTYPE html>
<html>
<head>
    <title>Anisopter</title>
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
      <a class="navbar-brand" href="#">
        Home
      </a>
    </div>
  </div>
</nav>
</header>
<div class="container">
<h1>Simulations</h1>

%for s in simulations:
<h2><a href="/simulation/{{s['_id']}}">{{s['date']}}</a></h2>
%end
</div>
</body>
</html>