#!/usr/bin/env python3
import db
import json
from flask import Flask, render_template, request, jsonify, Response


app = Flask(__name__)


@app.route("/")
def greet() -> str:
    return "Location api. /help for help"


@app.route("/insert", methods=['POST'])
def insert() -> Response:
    try:
        data = request.get_json()
        if data is None:
            return "ERROR, no json data found in POST request", 400

        db.insert(data)
    except Exception as e:
        return "ERROR " + str(e), 400

    return "Data inserted into database"


@app.route("/get")
def get() -> Response:
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if from_date is None and to_date is None:
        try:
            return jsonify(db.get_all_data())
        except Exception as e:
            return "ERROR " + str(e), 400

    try:
        return jsonify(db.get_period_data(from_date, to_date))
    except Exception as e:
        return "ERROR " + str(e), 400


@app.route("/get/last")
def get_last() -> Response:
    count = request.args.get("count", "1")
    if not count.isdigit():
        return "ERROR count should be am integer", 400
    try:
        return jsonify(db.get_last_data(int(count)))
    except Exception as e:
        return "ERROR " + str(e), 400

'''
TODO get data for today, for last 12 hours, for last 3 hours and from date1 to date2
TODO make /insert?token=TOKEN/... or some other way of authentification
TODO make config.py where different configs are stored (such as sql_connector_config,
     or app_config, or actualy, there is a way to have ql.connector.connect(option_files='my.conf') )
TODO README.md
'''


@app.route("/help")
def help() -> Response:
    return render_template('help.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

