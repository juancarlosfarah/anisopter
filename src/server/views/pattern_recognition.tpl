<!DOCTYPE html>
<html>
% include('head.tpl', title="Pattern Recognition")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>Pattern Recognition</h1>
            <p>
                To model the pattern recognition neurons, we initially
                replicated experiments conducted by T. Masquelier et al. [2, 3].
                A single of these neurons is able to successfully recognise a
                recurring pattern within background noise and a network of them
                is able to do so for multiple patterns. We then extended the
                module so that the neurons can be easily adapted to recognise
                input with varying properties such as average firing rate,
                number of afferents, frequency of pattern appearance,
                amongst others. This implementation is able to recognise
                patterns output from our CSTMD1 neurons and measures the
                effectiveness of the pattern recognition neurons by tracking key
                information such as true-positive, false-positive and
                true-negative spike incidences.
            </p>
            <a href="/pattern_recognition/simulations" class="h2">Simulations</a>
            <p>
                Your pattern recognition simulations.
            </p>
            <a href="/pattern_recognition/samples" class="h2">Samples</a>
            <p>
                Samples to run as input to the pattern recognition neurons.
            </p>
        </div>
    </div>
</div>
</body>
</html>