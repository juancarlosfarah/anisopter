__author__ = 'eg1114'

import subprocess

command1 = "python setup.py install --user"
command2 = "python -m coverage run test_training.py"
command3 = "python -m coverage report training/training.py"

commands = [command1, command2, command3]

for c in commands:
    subprocess.call(c.split(" "))