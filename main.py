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
    is_found = False

    cur.execute("SELECT country_iso2, country_name_ru, base_code, instr(phone_codes.code, ?) as count FROM phone_codes where count > 0 GROUP BY country_iso2, country_name_ru", [phone])
    data_list = []
    for row in cur:
        data = {
            "code": None,
            "iso_code": row[0],
            "cntr_name": row[1],
            "base_code": row[2]
        }
        data_list.append(data)
        is_found = True
    leng = 0
    if not is_found:
        cur.execute("SELECT code, country_iso2, country_name_ru, base_code, instr(?, phone_codes.code) as count FROM phone_codes where count > 0", [phone])
        data_list = []
        for row in cur:
            data = {
                "code": row[0],
                "iso_code": row[1],
                "cntr_name": row[2],
                "base_code": row[3]
            }
            if phone[1] == "7":
                data["code"] = phone[slice(5)]
            data_list.append(data)
        for cntr in data_list:
            if len(cntr["code"]) > leng:
                leng = len(cntr["code"])
        for cntr in data_list:
            if len(cntr["code"]) != leng:
                data_list.remove(cntr)
    return jsonify(data_list)

if __name__ == '__main__':
    app.run()