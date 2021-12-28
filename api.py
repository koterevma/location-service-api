#!/usr/bin/env python3
import db  # Импортируем файл db.py для работы с базой данных
import json  # Встроенный модуль для работы с данными в формате json

# Импортируем компоненты модуля flask
from flask import Flask, render_template, request, jsonify, Response


# Класс нашего серверного приложения
app = Flask(__name__)


'''Создаем привязку функции greet к запросам на uri /'''
@app.route("/")
def greet() -> str:
    return "Location api. /help for help"


'''Создаем привязку функции insert к запросам на uri /insert. 
Запросы принимаются только по методу POST'''
@app.route("/insert", methods=['POST'])
def insert() -> Response:
    try:
        # Принимаем данные в формате json
        data = request.get_json()
        if data is None:
            return "ERROR, no json data found in POST request", 400

        db.insert(data)
    except Exception as e:
        return "ERROR " + str(e), 400

    return "Data inserted into database"


'''Создаем привязку функции get к запросам на uri /get'''
@app.route("/get")
def get() -> Response:
    # В параметрах uri могут быть указанны параметры from и to
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    # Если пользователь не указывал параметры to, from, то в качестве ответа
    # мы вернем все имеющиеся в базе данных записи.
    if from_date is None and to_date is None:
        try:
            return jsonify(db.get_all_data())
        except Exception as e:
            return "ERROR " + str(e), 400

    # В случае, если указан хотя бы один из параметров,
    # возвращаем данные за заданный период
    try:
        return jsonify(db.get_period_data(from_date, to_date))
    except Exception as e:
        return "ERROR " + str(e), 400


'''Создаем привязку функции get_last к запросам на uri /get/last'''
@app.route("/get/last")
def get_last() -> Response:
    # Пользователь может передать количество записей
    count = request.args.get("count", "1")

    # Проверяем что пользователь указал допустимое значение
    if not count.isdigit():
        return "ERROR count should be am integer", 400
    try:
        return jsonify(db.get_last_data(int(count)))
    except Exception as e:
        return "ERROR " + str(e), 400


'''Создаем привязку функции help к запросам на uri /help'''
@app.route("/help")
def help() -> Response:
    # Отдаем статичную страницу help.html
    return render_template('help.html')


if __name__ == '__main__':
    # Если данный файл при интерпретации является основным, запускаем дебаг-сервер
    app.run(host="0.0.0.0", debug=True)

