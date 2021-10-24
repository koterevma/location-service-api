#!/usr/bin/env bash
BOLD_RED="\e[1;31m"
CLEAR="\e[0m"
[ -z "${PASSWORD}" ] && echo -e $BOLD_RED"[WARNING] PASSWORD is not set"$CLEAR || echo 'Enviroment variable PASSWORD is set, starting wsgi server'

gunicorn --bind unix:/home/www/api/api.sock -m 777 wsgi:app
