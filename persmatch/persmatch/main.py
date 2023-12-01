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


from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, send_file, make_response, jsonify
from werkzeug.utils import secure_filename
import socket
import time
import sqlite3
import json
import random
import string
import os
import os.path
from collections import Counter
from imdb import IMDb as MovieAPI
import spotipy.util as util
import spotipy
from os import path



conn = sqlite3.connect("database.db",  check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = 'infoeducatie e cool'  # a se schimba pentru more security
ALLOWED_EXTENSIONS = ['png', 'jpg', 'bmp', 'gif']
app.config["IMAGE_UPLOADS"] = "user_data/"


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
looking = []
spotify_objects = []

'''
FUNCTII NON-FLASK
'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def QueryToAray(query):
    lista_rezultanta = (query.rstrip().split('\n'))
    ln = []
    for element in lista_rezultanta:
        ela = element
        ela.replace("\r", "")
        print(ela)
        ln.append(ela)
    return ln

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def GetUserToken(Username, RedirectLink):
    Scope = "user-top-read"
    ClientID = 'f33ea24085634624b58c3622dedf563c'
    ClientSecret = 'af327494a245416baeb06580cf584350'
    RedirectURL = 'https://dexter0-0.github.io/'

    File = open("RedirectLink.txt", "w+")
    File.write(RedirectLink)
    File.close()

    Spotify = spotipy.Spotify(auth=util.prompt_for_user_token(Username, Scope, ClientID, ClientSecret, RedirectURL))
    return Spotify


def GetMusicCompatibility(SpotifyUserOne, SpotifyUserTwo):
    MusicScore = 0
    GenresOne = ""
    GenresTwo = ""
    TopArtistsOne = SpotifyUserOne.current_user_top_artists()
    TopArtistsTwo = SpotifyUserTwo.current_user_top_artists()

    for i in range(len(TopArtistsOne)):
        for j in range(len(TopArtistsOne["items"][i]["genres"])):
            GenresOne = GenresOne + TopArtistsOne["items"][i]["genres"][j] + ","

    for i in range(len(TopArtistsTwo)):
        for j in range(len(TopArtistsTwo["items"][i]["genres"])):
            GenresTwo = GenresTwo + TopArtistsTwo["items"][i]["genres"][j] + ","

    GenresOne = GenresOne.split(",")
    GenresTwo = GenresTwo.split(",")

    for i in range(len(GenresOne)):
        for j in range(len(GenresTwo)):
            if GenresOne[i] == GenresTwo[j]:
                MusicScore = MusicScore + 1

    MusicScore = MusicScore / max(len(GenresOne), len(GenresTwo))
    return MusicScore

###############################################################

def GetMovieCompatibility(MoviesUserOne, MoviesUserTwo):
    MovieScore = 0
    GenresOne = ""
    GenresTwo = ""

    for i in MoviesUserOne:
        MovieID = MovieAPI().search_movie(i)[0].movieID
        GenresMovie = MovieAPI().get_movie(MovieID)["genres"]
        for j in range(len(GenresMovie)):
            GenresOne = GenresOne + GenresMovie[j] + ","

    for i in MoviesUserTwo:
        MovieID = MovieAPI().search_movie(i)[0].movieID
        GenresMovie = MovieAPI().get_movie(MovieID)["genres"]
        for j in range(len(GenresMovie)):
            GenresTwo = GenresTwo + GenresMovie[j] + ","

    GenresOne = GenresOne.split(",")
    GenresTwo = GenresTwo.split(",")

    for i in range(len(GenresOne)):
        for j in range(len(GenresTwo)):
            if GenresOne[i] == GenresTwo[j]:
                MovieScore = MovieScore + 1

    MovieScore = MovieScore / max(len(GenresOne), len(GenresTwo))
    return MovieScore

###############################################################

def GetHobbyCompatibility(HobbiesOne, HobbiesTwo):
    HobbyScore = 0

    for i in range(len(HobbiesOne)):
        for j in range(len(HobbiesTwo)):
            if HobbiesOne[i].lower() == HobbiesTwo[j].lower():
                HobbyScore = HobbyScore + 1.5

    return HobbyScore

###############################################################

def GetPersonalityTypeMatch(PersonalityTypeOne, PersonalityTypeTwo):
    PersonalityScore = 0

    if PersonalityTypeOne == PersonalityTypeTwo:
        PersonalityScore = PersonalityScore + 1

    OppositePersonality = True

    # for i in range(len(PersonalityTypeOne)):
    #     if PersonalityTypeOne[i] == PersonalityTypeTwo[i]:
    #         OppositePersonality = False

    # if OppositePersonality is True:
    #     PersonalityScore = PersonalityScore + 1

    # INTJ
    if PersonalityTypeOne == "INTJ":
        if "N" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo or PersonalityTypeTwo == "INTP":
            PersonalityScore = PersonalityScore + 1
        if "P" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # INTP
    if PersonalityTypeOne == "INTP":
        if "NT" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo or PersonalityTypeTwo == "INTJ" or PersonalityTypeTwo == "INFP":
            PersonalityScore = PersonalityScore + 1
        if "FP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "IN" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ENTJ
    if PersonalityTypeOne == "ENTJ":
        if "TP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "I" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ":
            PersonalityScore = PersonalityScore + 1

    # ENTP
    if PersonalityTypeOne == "ENTP":
        if "IN" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ" or PersonalityTypeTwo == "ESFJ":
            PersonalityScore = PersonalityScore + 1
        if "SP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "N" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # INFJ
    if PersonalityTypeOne == "INFJ":
        if PersonalityTypeTwo == "ENTP" or PersonalityTypeTwo == "ENFP":
            PersonalityScore = PersonalityScore + 1
        if "ESF" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "N" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # INFP
    if PersonalityTypeOne == "INFP":
        if PersonalityTypeTwo == "ENFJ" or PersonalityTypeTwo == "ESFJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ENTJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "INFJ" or PersonalityTypeTwo == "ISFP":
            PersonalityScore = PersonalityScore + 1

    # ENFJ
    if PersonalityTypeOne == "ENFJ":
        if "INF" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "NFP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ENFP
    if PersonalityTypeOne == "ENFP":
        if PersonalityTypeOne == "INTJ" or PersonalityTypeTwo == "INFJ":
            PersonalityScore = PersonalityScore + 1
        if "S" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "NJ" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ISTJ
    if PersonalityTypeOne == "ISTJ":
        if PersonalityTypeTwo == "ESFP" or PersonalityTypeTwo == "ESTP":
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "S" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ISFJ
    if PersonalityTypeOne == "ISFJ":
        if PersonalityTypeTwo == "ENTJ" or PersonalityTypeTwo == "ESPF" or PersonalityTypeTwo == "ESTP":
            PersonalityScore = PersonalityScore + 1
        if "E" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if "IS" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ESTJ
    if PersonalityTypeOne == "ESTJ":
        if PersonalityTypeTwo == "ISTP" or PersonalityTypeTwo == "INTP" or PersonalityTypeTwo == "ISFP":
            PersonalityScore = PersonalityScore + 1
        if "I" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ESFJ
    if PersonalityTypeOne == "ESFJ":
        if PersonalityTypeTwo == "ISTJ" or PersonalityTypeTwo == "ESTJ":
            PersonalityScore = PersonalityScore + 1
        if "TP" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1

    # ISTP
    if PersonalityTypeOne == "ISTP":
        if PersonalityTypeTwo == "ESFJ"	or PersonalityTypeTwo == "ISTJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ" or PersonalityTypeTwo == "INTP":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ESTJ" or PersonalityTypeTwo == "ESFP":
            PersonalityScore = PersonalityScore + 1

    # ISFP
    if PersonalityTypeOne == "ISFP":
        if PersonalityTypeTwo == "ISFP":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ENFP" or PersonalityTypeTwo == "INFP":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "INFJ":
            PersonalityScore = PersonalityScore + 1

    # ESTP
    if PersonalityTypeOne == "ESTP":
        if PersonalityTypeTwo == "INFJ" or PersonalityTypeTwo == "ESTJ":
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ISFJ" or PersonalityTypeTwo == "ISTP":
            PersonalityScore = PersonalityScore + 1

    # ESFP
    if PersonalityTypeOne == "ESFP":
        if PersonalityTypeTwo == "ISTJ" or PersonalityTypeTwo == "ISFJ":
            PersonalityScore = PersonalityScore + 1
        if "S" or "J" in PersonalityTypeTwo:
            PersonalityScore = PersonalityScore + 1
        if PersonalityTypeTwo == "ENFP":
            PersonalityScore = PersonalityScore + 1

    return PersonalityScore

@app.errorhandler(404)
def page_not_found(e):
    # asta naspa ca e doar pentru 404
    return render_template('404NotFound.html'), 404


@app.route('/')
def mainpage():
    return render_template("SignUp.html")

@app.route('/login')
def logi(): #logi ca login nu e cool
    return render_template("index.html")

@app.route("/personalityform")
def trimite_personalityform():
    id_sesiune = str(request.args.get('ids'))
    # print(type(id_sesiune))
    if id_sesiune==None:
        return render_template("404NotFound.html")
    #aici se verifica assignnarea unui session id 
    else:
        cursor.execute('SELECT * FROM userdata WHERE id_sesiune = ?', (id_sesiune, ))
        if not cursor.fetchall():
            return render_template("404NotFound.html")
    #aici este continuarea
    #nvm is prost nu e

    # print(id_sesiune)
    return render_template("PersonalityForm.html")

@app.route("/home")
def redirecthome():
    id_sesiune = str(request.args.get('ids'))
    # print(type(id_sesiune))
    if id_sesiune==None:
        return render_template("404NotFound.html")
    #aici se verifica assignnarea unui session id 
    else:
        cursor.execute('SELECT * FROM userdata WHERE id_sesiune = ?', (id_sesiune, ))
        if not cursor.fetchall():
            return render_template("404NotFound.html")
    #aici este continuarea
    #nvm is prost V2 nu e 

    # print(id_sesiune)
    return render_template("HomePage.html")

@app.route("/incarca-photo", methods=['GET', 'POST'])
def incarcapoze():
    if request.method == 'POST':
        if request.files:
            image = request.files["image"]
            extension = image.filename[len(image.filename)-4:]
            id_sesiune = str(request.args.get('ids'))
            # print(id_sesiune)
            cursor.execute("SELECT username FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))  # execute a simple SQL select query
            user = (cursor.fetchall()[0][0])
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], user + extension))
            return "ok"

@app.route("/incarca-form", methods=['GET', 'POST'])
def confiramareform():
    id_sesiune = str(request.args.get('ids'))
    try:
        age = int(request.args.get("Age"))
    except:
        return "agenotint"

    agecategory = request.args.get("AgeCategory")
    gender = request.args.get("Gender")
    gendercategory = request.args.get("GenderCategory")
    personality = request.args.get("Personality")
    insta = request.args.get("InstagramUser")
    personalitytype = request.args.get("PersonalityType")
    spotifylink = request.args.get("SpotifyLink")

    #querry catre array
    filme = request.args.get("FilmeSeriale")
    filme = filme.split("\r")
    hobby = request.args.get("Hobby")
    hobby = QueryToAray(hobby)
    # print(filme)
    print("spo "+spotifylink)
    cursor.execute("SELECT username FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))  # execute a simple SQL select query
    user = (cursor.fetchall()[0][0])
    spotify_objects.append(GetUserToken(user, spotifylink))

    data = {
        "Age": age,
        "AgeCategory": agecategory,
        "Gender": gender,
        "GenderCategory": gendercategory,
        "Personality": personality,
        "PersonalityType": personalitytype,
        "SpotifyPos": len(spotify_objects) - 1,
        "InstagramUser": insta,
        "filme": filme,
        "hobby": hobby,
        "isMatched": "false",
        "MatchedID": "None"
    }
    data = json.dumps(data)
    cursor.execute("UPDATE userdata SET data = ? WHERE id_sesiune = ?", (data, id_sesiune))
    conn.commit()
    time.sleep(3)


    return "OK"

@app.route("/match")
def match():
    id_sesiune = str(request.args.get('ids'))
    # print(type(id_sesiune))
    if id_sesiune==None:
        return render_template("404NotFound.html")
    #aici se verifica assignnarea unui session id 
    else:
        cursor.execute('SELECT * FROM userdata WHERE id_sesiune = ?', (id_sesiune, ))
        if not cursor.fetchall():
            return render_template("404NotFound.html")
    #aici este continuarea
    #nvm is prost nu e

    # print(id_sesiune)
    return render_template("matching.html")


@app.route("/matchfound")
def matchf():
    id_sesiune = str(request.args.get('ids'))
    # print(type(id_sesiune))
    if id_sesiune==None:
        return render_template("404NotFound.html")
    #aici se verifica assignnarea unui session id 
    else:
        cursor.execute('SELECT * FROM userdata WHERE id_sesiune = ?', (id_sesiune, ))
        if not cursor.fetchall():
            return render_template("404NotFound.html")
    #aici este continuarea
    #nvm is prost nu e

    # print(id_sesiune)
    return render_template("MatchFound.html")

@app.route("/searchmatch", methods=["GET", "POST"])
def searchmatch():
    id_sesiune = str(request.args.get('ids'))
    if id_sesiune==None:
        return render_template("404NotFound.html")
    #aici se verifica assignnarea unui session id 
    else:
        cursor.execute('SELECT * FROM userdata WHERE id_sesiune = ?', (id_sesiune, ))
        if not cursor.fetchall():
            return render_template("404NotFound.html")
    cursor.execute("SELECT data FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))  # execute a simple SQL select query
    try:
        data = str(cursor.fetchall()[0][0])
        if json.loads(data)["isMatched"] == "true":
            return ("deja gasit")
    except:
        return("Eroare json")
    
    cursor.execute("SELECT username FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))
    local_user = str(cursor.fetchall()[0][0])
    looking.append(local_user)
    score = 0
    best = {}
    # print(looking)

    for user in looking:
        print(user)
        if user != local_user:
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (local_user, ))
            # print(cursor.fetchall()[1][0])
            RedirectUserOne = int(json.loads(cursor.fetchall()[0][0])["SpotifyPos"])
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (user, ))
            RedirectUserTwo = int(json.loads(cursor.fetchall()[0][0])["SpotifyPos"])
            try:
                score = score + GetMusicCompatibility(spotify_objects[RedirectUserOne], spotify_objects[RedirectUserTwo])
            except:
                score = score + 0
            
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (local_user, ))
            Moviearray1 = json.loads(cursor.fetchall()[0][0])["filme"]
            print(Moviearray1)
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (user, ))
            Moviearray2 = json.loads(cursor.fetchall()[0][0])["filme"]
            print(Moviearray2)
            
            try:
                score = score + GetMovieCompatibility(Moviearray1, Moviearray2)
            except:
                score = score + 0
            
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (local_user, ))
            hobbyarray1 = json.loads(cursor.fetchall()[0][0])["hobby"]
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (user, ))
            hobbyarray2 = json.loads(cursor.fetchall()[0][0])["hobby"]
            score = score + GetHobbyCompatibility(hobbyarray1, hobbyarray2)
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (local_user, ))
            persoarray1 = json.loads(cursor.fetchall()[0][0])["Personality"]
            print(persoarray1)
            cursor.execute("SELECT data FROM userdata WHERE username = ?", (user, ))
            persoarray2 = json.loads(cursor.fetchall()[0][0])["Personality"]
            score = score + GetPersonalityTypeMatch(persoarray1, persoarray2)
            best.update(user = score)
            
        cursor.execute("SELECT id_sesiune FROM userdata WHERE username = ?", (local_user, ))
        otherIDS = cursor.fetchall()[0][0]
        
        data = {
            "user": user,
            "myUser": local_user,
            "score": score,
            "otherIDS": otherIDS

        }

        return jsonify(data)
    

@app.route("/avatar", methods=["GET", "POST"])
def damiavarul():
    id_sesiune = str(request.args.get('ids'))
    cursor.execute("SELECT username FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))  # execute a simple SQL select query
    user = str(cursor.fetchall()[0][0])
    if path.exists("user_data/" + user + ".png"):
        return send_file("user_data/" + user + ".png")

    if path.exists("user_data/" + user + ".jpg"):
        return send_file("user_data/" + user + ".jpg")

    if path.exists("user_data/" + user + ".bmp"):
        return send_file("user_data/" + user + ".bmp")

@app.route("/nume", methods=["GET", "POST"])
def daminumele():
    id_sesiune = str(request.args.get('ids'))
    cursor.execute("SELECT username FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))  # execute a simple SQL select query
    try:
        user = str(cursor.fetchall()[0][0])
        response = make_response(user, 200)
        response.mimetype = "text/plain" #FACEM ASTA PE VIITOR CA SA NU NE ATACE HECERI

        return user
    except:
        return "404"

@app.route("/instagram", methods=["GET", "POST"])
def gibinsta():
    id_sesiune = str(request.args.get('ids'))
    cursor.execute("SELECT data FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))  # execute a simple SQL select query
    try:
        data = str(cursor.fetchall()[0][0])
        instagram = json.loads(data)["InstagramUser"]
        return instagram
    except:
        return "404"

@app.route("/varsta", methods=["GET", "POST"])
def gibvarsta():
    id_sesiune = str(request.args.get('ids'))
    cursor.execute("SELECT data FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))
    try:
        data = str(cursor.fetchall()[0][0])
        ange = json.loads(data)["Age"]
        return str(ange)
    except:
        return "404"

@app.route("/isMatched", methods=["GET", "POST"])
def gibmatched():
    id_sesiune = str(request.args.get('ids'))
    cursor.execute("SELECT data FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))
    try:
        data = str(cursor.fetchall()[0][0])
        ange = json.loads(data)["isMatched"]
        # print(ange)
        return str(ange)
    except:
        return "404"

@app.route("/matchedWith", methods=["GET", "POST"])
def matchedWith():
    id_sesiune = str(request.args.get('ids'))
    cursor.execute("SELECT data FROM userdata WHERE id_sesiune = ?", (id_sesiune, ))
    try:
        data = str(cursor.fetchall()[0][0])
        ange = json.loads(data)["MatchedID"]
        # print(ange)
        return str(ange)
    except:
        return "404"

    
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
        cursor.execute("INSERT INTO userdata(id, id_sesiune) VALUES (?,?)", (local_id, id_sesiune)) # de rezolvat pe viitor
        conn.commit()
        ids = local_id
        return redirect(url_for("redirecthome", ids=id_sesiune))
    else:
        # e destul de rau 
        return render_template("user_negasit.html")

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
        return redirect(url_for("trimite_personalityform", ids=id_sesiune))
    else:
        return render_template("combinatie_gresita.html")

cursor = conn.cursor()
app.run(debug=True, host="0.0.0.0")