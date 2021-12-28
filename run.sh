#!/usr/bin/env bash
BOLD_RED="\e[1;31m"
CLEAR="\e[0m"

# Если переменная окружения PASSWORD не задана, напоминаем пользователю об этом
[ -z "${PASSWORD}" ] && echo -e $BOLD_RED"[WARNING] PASSWORD is not set"$CLEAR \
	|| echo 'Enviroment variable PASSWORD is set, starting wsgi server'

# Запуск продакшн-сервера gunicorn через сокет
gunicorn -w 3 --bind unix:/home/www/location-service-api/api.sock -m 777 wsgi:app

