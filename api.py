#!/usr/bin/env python3
import db
import json
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route("/")
def greet() -> str:
    return "Location api. /help for help"


@app.route("/insert/<string:date>/<string:coords>")
def insert(date: str, coords: str) -> str:
    try:
        latitude, longitude = coords.split(',')
        db.insert(
            dict(
                date=date,
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
    try:
        data = db.get_all_data()
    except Exception as e:
        return "ERROR " + str(e)
    else:
        return json.dumps(data)


@app.route("/help")
def help() -> str:
    help_text = '''
    <p>/insert/&ltdatetime&gt/&ltcoords&gt</p>
    insert values to database<br>
    format for datetime: "YYYY-MM-DD HH:MM::SS" (space can be swapped by 'T', see examples below)<br>
    format for coords: "1.12,2.21" (precision up to 8 digits after a point)<br>
    <p>/get</p>
    returns all values from database in json format<br>
    <br>
    <h2>Examples</h2><br>
    http://localhost/api/insert/2021-10-17T15:44:00/20.12345678,30.12345678/<br>
    http://localhost/api/get/<br>'''
    return help_text


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

