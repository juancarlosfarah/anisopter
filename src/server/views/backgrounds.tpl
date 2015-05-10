<!DOCTYPE html>
<html>
% include('head.tpl', title="Animation Backgrounds")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <h1>Backgrounds</h1>
        </div>
        <div class="col-md-2">
            <button type="button"
                    onclick="window.location.href='/target_animation/background/new'"
                    class="btn btn-primary">Upload Background</button>
        </div>
    </div>
    <div class="row">
        %for bg in bgs:
        <div class="col-lg-2 col-md-2 col-sm-3 col-xs-4">
            <img src="/assets/backgrounds/{{bg}}"
                 alt="Background"
                 class="img-rounded img-responsive"/>
        </div>
        %end
    </div>
</div>
</body>
</html>