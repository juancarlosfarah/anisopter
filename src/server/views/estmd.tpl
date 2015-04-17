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
                ESTMD can detect small-target motion across a moving,
                complicated background. This stage required research into
                spatio-temporal filters that approximate the function of real
                ESTMD neurons. The input of the ESTMD can either be a full
                video or a frame-by-frame stream as it is produced by the
                animation tool. The output of the ESTMD model is a time
                series of matrices of processed pixels, which can be viewed in
                a video. This output is connected to the CSTMD1 neurons by
                converting each pixel into a ring rate for a simple
                integrate-and-re neuron and connecting the output of each of
                these neurons to the CSTMDs.
            </p>
            <a href="/estmd/simulations" class="h2">Simulations</a>
            <p>
                Given an input, simulate the output of an ESTMD neuron.
            </p>
        </div>
    </div>
</div>
</body>
</html>