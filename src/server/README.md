Anisopter Web Server
====================

To Run in Development:
----------------------

1. Start up MongoDB server.

    service mongod start

2. Start up Bottle server.

    python server.py


To Set Up for Production:
-------------------------

1. Make sure the anisopter.ini and anisopter files in this folder
are correct for your production environment. The provided files are
an example of what an environment might be like.

2. Copy it to the `uwsgi/apps-available` folder. 

    cp anisopter.ini /etc/uwsgi/apps-available/ 

3. Create a symbolic link to the `uwsgi/apps-enabled` folder.

    ln -s /etc/uwsgi/apps-available/anisopter.ini /etc/uwsgi/apps-enabled/anisopter.ini

4. 

To Run:

1. Start uWSGI.

    service uwsgi start
    
2. Start Nginx.



    nohup python server.py -p 55080 --host="146.169.47.153" -d > bottle.log &
