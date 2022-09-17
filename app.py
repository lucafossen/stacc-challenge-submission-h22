from tkinter import ALL
from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
# app.secret_key = "q#¤G%&2#BV¤5#¤5"

@app.route("/", methods=("GET", "POST"))
def index():
    """returns HTML template for default landing page"""

    return render_template("index.html")

ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "pdf")

@app.route("/kunde", methods=("GET", "POST"))
def kunde():
    """returns HTML template for the customer view"""

    if request.method == "POST":
        can_submit = False
        is_PEP = False
        
        now = datetime.now()
        full_name = request.form["fullname"]
        # secure the file name here so that image and json entry have the same name
        aplctn_key = secure_filename(f"{full_name}:{now}")

        # Check if the post request has the file part
        if "file" not in request.files:
            print("No file part")
        else:
            aplctn_id_img = request.files["file"]
            extension = aplctn_id_img.filename.split(".")[-1] # Get the characters after the last dot
            if aplctn_id_img and extension.lower() in ALLOWED_EXTENSIONS:
                aplctn_id_img.save(f"application_imgs/{aplctn_key}.{extension}")
                can_submit = True
            else:
                print("File not allowed")

        if can_submit:
            print("can submit")
            # Politically exposed person (PEP) check
            PEP_result = PEP_lookup(full_name)
            if is_PEP or PEP_result["numberOfHits"] > 0:
                is_PEP = True
                PEP_save_json(aplctn_key, PEP_result, now)
            return render_template("kunde_success.html", PEP=f"PEP hits: {PEP_result['numberOfHits']}")
            
        else:
            print("can not submit")
            return render_template("kunde.html",
            invalid_file=f"Beklager! Vi tillater ikke .{extension} filer.",
            supported_files=f"For øyeblikket støtter vi kun: {', '.join(ALLOWED_EXTENSIONS)}")
            
    return render_template("kunde.html")

@app.route("/ansatt")
def ansatt():
    """returns HTML template for the employee view"""
    return render_template("ansatt.html")


def PEP_lookup(name):
    """Uses Stacc's API to get information on politically exposed persons (PEPs).
    returns a tuple of the searched name, along with the API response.

    If a PEP is detected, their info will get saved to data/politically_exposed_people.json.
    TODO: hashing of info for better security 
    """

    response = json.loads(requests.get(f"https://code-challenge.stacc.dev/api/pep?name={name}").content)
    return response

# Decided to separate this from PEP_lookup in order to separate fruitful and non-fruitful functionality
def PEP_save_json(name, response, time_recorded):
    """Saves the result of a PEP lookup to file"""
    path = "data/politically_exposed_people.json"
    with open(path) as file:
        f = file.read()
        if len(f) < 1:
            pep = {} # start with an empty dict/object if file is empty
        else:
            pep = json.loads(f)
    with open(path, "w") as file:
        # PEP entries are stored as keys of format "searched name:current time"
        # Example: "Knut Arild Hareide:2022-09-17 14:44:02.361926"
        pep[f"{name}:{time_recorded}"] = response
        json.dump(pep, file)