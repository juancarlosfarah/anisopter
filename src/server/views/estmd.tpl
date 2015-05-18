<!DOCTYPE html>
<html>
% include('head.tpl', title="ESTMD")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>ESTMD</h1>
            <p>
                The elementary small target motion detector (ESTMD) neuron features 
                the ability of detecting small-target motion across a moving,
                complicated background. This stage required research into
                spatio-temporal filters that approximate the function of real
                ESTMD neurons. The input of the ESTMD can either be a full
                video or a frame-by-frame stream as it is produced by the
                animation tool. The output of the ESTMD model is a time
                series of matrices of processed pixels, which can be viewed in
                a video. This output is connected to the CSTMD1 neurons by
                converting each pixel into a firing rate for a simple
                integrate-and-fire neuron and connecting the output of each of
                these neurons to the CSTMDs.
            </p>
            <a href="/estmd/simulations" class="h2">Simulations</a>
            <p>
                Your ESTMD simulations.
            </p>
        </div>
    </div>
    <div class="row">
        <div class="col-md-offset-4 col-md-4">
            <img src="/assets/images/wiederman09.png" alt="wdrmn09"
                 class="img-responsive img-rounded">
        </div>
    </div>
    <div class="row">
        <div class="col-md-12 text-center">
            <p>Outline of ESTMD implentation. </p>
        </div>
        <div class="col-md-12 text-center">
            <p> Steven Wiederman. A Neurobiological and Computational Analysis of Target Discrimination in
Visual Clutter by the Insect Visual System. (September), 2008. </p>
        </div>
    </div>
    <br />
    <br />
    <div class="row">
        <div class="col-md-12">
            <div class="row">
                <div class="col-md-12 text-center">
                    <button type="button"
                            onclick="window.location.href='/estmd/simulation/new'"
                            class="btn btn-lg btn-primary">New ESTMD Simulation</button>
                </div>
            </div>
        </div>
    </div>
</div>
% include('footer.tpl')
</body>
</html>
