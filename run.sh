#!/usr/bin/env sh
gunicorn --bind unix:/home/www/api/api.sock -m 777 wsgi:app
