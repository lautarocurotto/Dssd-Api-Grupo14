#!/bin/bash
# Aplica las migraciones
python manage.py migrate
python manage.py collectstatic
# Luego, levanta el servidor con gunicorn
gunicorn deposito.wsgi:application --bind 0.0.0.0:8000
