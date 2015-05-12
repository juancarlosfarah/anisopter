# Allow traffic from 146.169.47.117
sudo iptables -A INPUT -s 146.169.47.117 -p tcp --destination-port 27017 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -d 146.169.47.117 -p tcp --source-port 27017 -m state --state ESTABLISHED -j ACCEPT