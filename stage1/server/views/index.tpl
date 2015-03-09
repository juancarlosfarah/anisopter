<!DOCTYPE html>
<html>
% include('head.tpl', title="Simulations")
<body>
% include('header.tpl')
<div class="container">
    <p>
        Our goal in this project is to model the target selection mechanism
        of the dragonfly and implement it in a biomimetic agent. Dragonflies
        are notoriously effective at prey capture, making the neural processes
        that underlie this ability particularly interesting to investigate.
    </p>
    <p>
        The centrifugal small target motion detector neuron 1 (CSTMD1) is a
        higher order visual neuron in the brain of the dragonfly. This neuron
        reacts to the presentation of multiple visual stimuli by firing as if
        only one of the stimuli was present; this is presumably an attentional
        selection mechanism. At Professor Murray Shanahan's lab, researchers
        have simulated the large contralateral dendritic field of the CSTMD1
        neuron with a biophysical multi-compartmental Hodgkin-Huxley model.
        Along with Klaus Stiefel, they found that with certain numbers of
        inhibitory synapses and potassium conductance densities, two
        mutually-coupled CSTMD1 neurons are capable of a bistable switching
        process between two input patterns. This bistability can serve as a
        mechanism for the observed attentional selection.
    </p>
    <p>
        The high-level idea of the project is to employ the principle used by
        the CSTMD1 neuron in a biomimetic agent that behaves like a dragonfly,
        showing attention-like target selection when performing a simple
        foraging task.
    </p>
</div>
</body>
</html>