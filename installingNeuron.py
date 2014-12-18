# Taken from http://www.neuron.yale.edu/neuron/download/compile_linux#otheroptions

cd $HOME
mkdir neuron
mv iv-mm.tar.gz neuron
mv nrn-nn.tar.gz neuron
cd neuron
tar xzf iv-mm.tar.gz
tar xzf nrn-nn.tar.gz
# renaming the new directories iv and nrn makes life simpler later on
mv iv-mm iv
mv nrn-nn nrn

cd iv
./configure --prefix=`pwd`
make
sudo make install


cd ..
cd nrn
./configure --prefix=`pwd` --with-iv=$HOME/neuron/iv --with-nrnpython=/usr/bin/python
make
sudo make install

cd src/nrnpython
sudo python setup.py install
