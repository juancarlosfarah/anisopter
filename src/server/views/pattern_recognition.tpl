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
                The purpose of the Pattern Recognition module is to discern 
                recurring spike patterns within the output from the CSTMD1 
                module, with each pattern recognition neuron becoming selective 
                to one pattern. Given the expected behaviour of CSTMD1 neurons, 
                we hypothesised that any patterns found in the output of the 
                CSTMD1 module would encode information about the velocity and 
                direction of targets observed in the visual field of the 
                dragonfly.
            </p>
            <p>
                To model the pattern recognition neurons, we initially
                replicated experiments conducted by T. Masquelier et al.
                A single of these neurons is able to successfully recognise a
                recurring pattern within background noise and a network of them
                is able to do so for multiple patterns. This behaviour is 
                achieved by modulating the weights of the pattern recognition 
                neuron's synaptic connections to its afferents using 
                spike-timing-dependent plasticity (STDP). STDP uses long term 
                synaptic potentiation (LTP) to reinforce connections 
                with afferents that fired shortly before the post-synaptic 
                neuron, and long term depression (LTD) to weaken those with 
                afferents that fired shortly after. 
            </p>
            <p>
                We then extended the module so that the neurons can be easily 
                adapted to recognise input with varying properties such as 
                average firing rate, number of afferents, frequency of pattern 
                appearance, amongst others. This implementation is able to 
                recognise patterns output from our CSTMD1 neurons and measures 
                the effectiveness of the pattern recognition neurons by 
                tracking key information such as true-positive, false-positive 
                and true-negative spike incidences.
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
    <div class="row">
      <div class="col-md-offset-3 col-md-6">
	<img src="/assets/images/stdp.png" alt="STDP" class="img-responsive img-rounded">
      </div>
    </div>
    <div class="row">
        <div class="col-md-12 text-center">
            <p>Sample caption.</p>
        </div>
    </div>
    <br />
    <br />
    <div class="row">
        <div class="col-md-12">
            <div class="row">
                <div class="col-md-12 text-center">
                    <button type="button"
                            onclick="window.location.href='/pattern_recognition/simulation/new'"
                            class="btn btn-lg btn-primary">New Pattern Recognition Simulation</button>
                </div>
            </div>
        </div>
    </div>
</div>
% include('footer.tpl')
</body>
</html>
