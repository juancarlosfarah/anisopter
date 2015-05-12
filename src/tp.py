import subprocess

command1 = 'git pull'
command2 = 'git add training -A'
command3 = 'git commit -m "Training-moarhhh"'
command4 = 'git push'

commands = [command1, command2, command3, command4]

for c in commands:
    subprocess.call(c.split(" "))