service nginx stop
service uwsgi stop
cd /var/www/anisopter
git pull origin master
service uwsgi start
service nginx start
