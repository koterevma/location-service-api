#!/usr/bin/env python3
import db
import json
from flask import Flask, escape, render_template, request


app = Flask(__name__)


@app.route("/")
def greet() -> str:
    return "Location api. /help for help"


@app.route("/insert/<string:date>/<string:coords>")
def insert(date: str, coords: str) -> str:
    try:
        # print(request.args.get('token', ''))
        latitude, longitude = str(escape(coords)).split(',')
        db.insert(
            dict(
                date=str(escape(date)),
                latitude=latitude,
                longitude=longitude
            )
        )
    except Exception as e:
        return "ERROR " + str(e)
    else:
        return "Data inserted into database"


@app.route("/get")
def get() -> str:
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if from_date is None and to_date is None:
        try:
            data = db.get_all_data()
        except Exception as e:
            return "ERROR " + str(e)
        else:
            return json.dumps(data)

    try:
        data = db.get_period_data(from_date, to_date)
    except Exception as e:
        return "ERROR " + str(e)
    else:
        return data


'''
TODO get data for today, for last 12 hours, for last 3 hours and from date1 to date2
TODO make /insert?token=TOKEN/... or some other way of authentification
TODO make config.py where different configs are stored (such as sql_connector_config,
     or app_config, or actualy, there is a way to have ql.connector.connect(option_files='my.conf') )
TODO README.md
'''


@app.route("/help")
def help() -> str:
    return render_template('help.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

