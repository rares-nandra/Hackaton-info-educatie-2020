#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from flask import Flask, render_template, send_from_directory, request, redirect
import socket
import sqlite3
import json
import random
import string



conn = sqlite3.connect("database.db",  check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = 'infoeducatie e cool'  # a se schimba pentru more security


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() pe UDP nu trimite pachete no scuze no
local_ip_address = s.getsockname()[0]
local_ip_address = "http://" + str(local_ip_address) + ":5000/"
print("Adresa locala pe care te conectezi: " + local_ip_address)


cursor.execute("""CREATE TABLE IF NOT EXISTS userdata
                  (username text, password text, id int, 
                   id_sesiune text, data json) 
               """)


ids=0


@app.route('/')
def mainpage():
    return render_template("index.html")

@app.route("/autentificare")
def autentificare():
    return render_template("SignUp.html")

@app.route("/statice/<path:path>") #pentru servire fisiere statice
def trimite_statice(path):
    return send_from_directory('statice', path)

@app.route("/ruta-login", methods=['POST'])
def login():
    global ids
    username = request.form['username']
    password = request.form['password']
    cursor.execute('SELECT * FROM userdata WHERE username = ? AND password = ?', (username, password))
    # daca execute rezulta nimic atunci da pass spre else
    # to-do fix
    if cursor.fetchall():
        local_id = ids + 1
        id_sesiune = ''.join(random.choice(string.ascii_letters) for x in range(15))
        cursor.execute("INSERT INTO userdata(id, id_sesiune) VALUES (?,?)", (local_id, id_sesiune))
        conn.commit()
        ids = local_id
    else:
        print('Login failed')

@app.route("/ruta-auth", methods=["POST"])
def authme():
    global ids
    local_id = ids + 1
    username = request.form['username']
    password = request.form['password']
    confirm = request.form["ConfirmPassword"]
    if password == confirm:
        id_sesiune = ''.join(random.choice(string.ascii_letters) for x in range(15))
        cursor.execute("INSERT INTO userdata(username, password, id, id_sesiune) VALUES (?,?,?,?)", (username, password, local_id, id_sesiune))
        conn.commit()
        ids = local_id
    else:
        return "te drec nu e buna parola"
cursor = conn.cursor()
app.run(debug=True, host="0.0.0.0")