<!DOCTYPE html>
<html>
% include('head.tpl', title="CSTMD1")
<body>
% include('header.tpl')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>CSTMD1</h1>
            <p>
                The centrifugal small target motion detector neuron 1 (CSTMD1)
                is a higher order visual neuron in the brain of the dragonfly.
                This neuron reacts to the presentation of multiple visual
                stimuli by firing as if only one of the stimuli was present;
                this is presumably an attentional selection mechanism.
                At Professor Murray Shanahan's lab, researchers have simulated
                the large contralateral dendritic field of the CSTMD1 neuron
                with a biophysical multi-compartmental Hodgkin-Huxley model.
                Along with Klaus Stiefel, they found that with certain
                numbers of inhibitory synapses and potassium conductance
                densities, two mutually-coupled CSTMD1 neurons are capable of a
                bistable switching process between two input patterns. This
                bistability can serve as a mechanism for the observed
                attentional selection.
            </p>
            <a href="/cstmd/simulations" class="h2">Simulations</a>
            <p>
                Your CSTMD1 simulations. 
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
                            onclick="window.location.href='/cstmd/simulation/new'"
                            class="btn btn-lg btn-primary">New CSTMD1 Simulation</button>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
      <div class="col-md-offset-2 col-md-8">
	<img src="/assets/images/CSTMD.png" alt="CSTMD" class="img-responsive img-rounded">
      </div>
    </div>
    <div class="row">
        <div class="col-md-12 text-center">
            <p>Structure of an actual CSTMD1 neuron.</p>
        </div>
    </div>


</div>
% include('footer.tpl')
</body>
</html>
