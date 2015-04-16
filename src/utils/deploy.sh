#!/usr/bin/env bash
su root
service uwsgi stop
cd /var/www/anisopter
su www-data
git pull origin master
su root
service uwsgi start