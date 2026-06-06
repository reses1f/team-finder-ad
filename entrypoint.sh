#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py load_demo_data

exec python manage.py runserver 0.0.0.0:8000
