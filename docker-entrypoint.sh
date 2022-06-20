#!/usr/bin/env bash

set -ex
set -o allexport

#echo "Running migrations"
#while ! python3 ./manage.py makemigrations --noinput 2>&1; do
#  echo "Creating migration files"
#  sleep 3
#done

# Run db migraiton
while ! python3 manage.py migrate 2>&1; do
   echo "Performing database migration"
   sleep 3
done

echo 'Starting application'
python3 ./manage.py runserver 0.0.0.0:8080
