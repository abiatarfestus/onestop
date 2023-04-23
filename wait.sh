#!/bin/sh

while ! nc -z mysql_db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

python onestop/manage.py runserver 0.0.0.0:8000