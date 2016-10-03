#!/bin/bash

cd /application
# python manage.py migrate --noinput
echo "running collectstatic"
python manage.py collectstatic --noinput
# start supervisord
echo "starting supervisord"
supervisord -c /etc/supervisord.conf
echo "starting web service"
uwsgi /etc/uwsgi.ini
