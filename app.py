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

        now = datetime.now()
        full_name = request.form["fullname"]
        # secure the file name here so that image and json entry have the same name
        aplctn_key = secure_filename(f"{full_name}-{now}")

        # Check if the post request has the file part
        if "file" not in request.files:
            print("No file part")
        else:
            id_file = request.files["file"]
            # Get the file extension (the characters after the last dot)
            extension = id_file.filename.split(".")[-1]

            # Check if ID file is in a valid format
            if id_file and extension.lower() in ALLOWED_EXTENSIONS:
                id_file.save(f"data/application_imgs/{aplctn_key}.{extension}")
                can_submit = True
            else:
                print("File not allowed")

        # Submit the application if format is valid
        if can_submit:
            application = dict(request.form)

            # Politically exposed person (PEP) check

            PEP_result = PEP_lookup(full_name)
            application['PEP_lookup_result'] = PEP_result

            # Construct feedback messages about PEP for user
            PEP_msg = ""
            PEP_funny_msg = ""
            if request.form.get("PEP_self_flag") == "yes":
                PEP_msg = f"""Merk: Du har flagget deg selv som en politisk eksponert person, og blir sendt til manuell behandling."""
            elif PEP_result["numberOfHits"] > 0:
                PEP_funny_msg = f"""Du er en liten luring, du! Selv om du prøvde å slippe unna, fant vi navnet ditt i {PEP_result['numberOfHits']} databaser. Du blir sendt til manuell behandling."""

            save_loan_application(aplctn_key, application)
            return render_template("kunde_success.html", PEP_msg=PEP_msg, PEP_funny_msg=PEP_funny_msg)

        # Can not submit
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
    simply returns the API response.
    """

    response = json.loads(requests.get(f"https://code-challenge.stacc.dev/api/pep?name={name}").content)
    return response

def save_loan_application(name, data):
    """Saves the result of a loan application to file"""
    path = "data/loan_applications.json"
    with open(path) as file:
        f = file.read()
        if len(f) < 1:
            pep = {} # start with an empty dict/object if file is empty
        else:
            pep = json.loads(f)
    with open(path, "w") as file:
        # applications are stored with keys of format "full name-current time".
        # Example: "Knut_Arild_Hareide-2022-09-18_155259.308949"
        # This is also the format used for image files names, so that images and applications can be associated with each other.
        pep[name] = data
        json.dump(pep, file)