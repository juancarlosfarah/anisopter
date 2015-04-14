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
                In order to generate input for our visual pre-processing layer,
                we developed an animation tool using Pyglet. This allows the
                user to create a video of black targets moving across a custom
                background that is either stationary or moving. The size and
                velocity vector of each target is adjustable.
            </p>
            <a href="/target_animation/animations" class="h2">Animations</a>
            <p>
                Your target animations.
            </p>
            <a href="/target_animation/backgrounds" class="h2">Backgrounds</a>
            <p>
                Backgrounds to include as input to your animations.
            </p>
        </div>
    </div>
</div>
</body>
</html>