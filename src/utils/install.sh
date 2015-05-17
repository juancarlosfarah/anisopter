#!/bin/bash
cd $HOME/git/anisopter/src/action_selection
sudo python setup.py install
cd $HOME/git/anisopter/src/animation
sudo python setup.py install
cd $HOME/git/anisopter/src/cstmd
sudo python setup.py install
cd $HOME/git/anisopter/src/estmd
sudo python setup.py install
cd $HOME/git/anisopter/src/pattern_recognition
sudo python setup.py install
cd $HOME/git/anisopter/src/training
sudo python setup.py install
exit 0
