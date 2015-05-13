import subprocess
import sys

module = str(sys.argv[1])

command1 = 'git pull'
command2 = 'git add ' + module + ' -A'
command3 = 'git commit -m "Automatic"'
command4 = 'git push'

commands = [command1, command2, command3, command4]

for c in commands:
    print c
    print "========================"
    subprocess.call(c.split(" "))