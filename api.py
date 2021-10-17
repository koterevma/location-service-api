#!/usr/bin/env python3
import db
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

