<!DOCTYPE html>
<html>
% include('head.tpl', title="Target Animation")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>Target Animation</h1>
            <p>
                This module represents the input to the dragonfly's retina.
                It is an animation tool developed using pyglet allows the user 
                to flexibly create videos of moving targets against a custom and 
                potentially moving background. The size and
                velocity vector of each target is adjustable.
            </p>
            <a href="/target_animation/backgrounds" class="h2">Backgrounds</a>
            <p>
                Backgrounds to include as input to your animations.
            </p>
            <a href="/target_animation/animations" class="h2">Animations</a>
            <p>
                Your target animations.
            </p>
        </div>
    </div>
    <br />
    <br />
    <div class="row">
        <div class="col-md-12">
            <div class="row">
                <div class="col-md-12 text-center">
                    <button type="button"
                            onclick="window.location.href='/target_animation/animation/new'"
                            class="btn btn-lg btn-primary">New Animation</button>
                </div>
            </div>
        </div>
    </div>
</div>
% include('footer.tpl')
</body>
</html>
