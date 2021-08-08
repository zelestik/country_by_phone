#! /usr/bin/env python3
import sqlite3
from flask import Flask, jsonify, request, send_file


app = Flask(__name__)
application = app
wsgi_app = app.wsgi_app

@app.route('/')
def main():
    return send_file("index.html")


@app.route('/get_country/<string:phone>')
def get_country(phone):
    con = sqlite3.connect('phonecodes.sqlite')
    cur = con.cursor()
    cur.execute("SELECT code, country_iso2, country_name_ru, instr('"+ phone +"', phone_codes.code) as count FROM phone_codes where count > 0")
    data_list = []
    for row in cur:
        data = {
            "code": row[0],
            "iso_code": row[1],
            "cntr_name": row[2]
        }
        data_list.append(data)
    return jsonify(data_list)

if __name__ == '__main__':
    app.run()