#!/bin/bash


echo "Checking migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate


echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000