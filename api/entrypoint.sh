#!/bin/sh
set -e
until cd /app
do
    echo "Wait for server volume..."
done

pg_isready -h $DB_HOST -p $DB_PORT -t 5

# робимо міграції перед запуском wsgi сервера
until python manage.py migrate
do
    echo "Waiting for postgres ready..."
done

# збираємо статику
python manage.py collectstatic

python manage.py runserver 0.0.0.0:$SERVER_PORT
