from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from uuid import uuid4 as uuid

app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def index():
    """returns HTML template for default landing page"""

    return render_template("index.html")

ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "pdf")

@app.route("/kunde", methods=("GET", "POST"))
def kunde():
    """returns HTML template for the customer view.
    Does some form validation, although this can be extended.
    Perhaps also done client-side?
    """

    if request.method == "POST":
        submit_errors = []
        # Check if the post request has the file part
        id_file = request.files["file"]
        # Get the file extension (the characters after the last dot)
        extension = id_file.filename.split(".")[-1].lower()
        error_msgs = {
            "invalid_name": (
                "Feil! Du må skrive hele navnet ditt, korten!",
                "(Denne feilen kom opp siden du ikke hadde mellomrom i navnet ditt.)"
            ),
            "invalid_img": (
                f"Beklager, kjære fil-connoisseur! Vi tillater ikke .{extension} filer.",
                f"For øyeblikket støtter vi kun: {', '.join(ALLOWED_EXTENSIONS)}"
            ),
            "invalid_ssn": (
                "Beklager! Vi støtter bare undekupple fødselnummer!",
                "( altså av lengde 11 )"
            )
        }
        # secure the file name here so that image and json entry have the same name
        aplctn_key = str(uuid())
        full_name = request.form["fullname"].strip()


        # Check if name contains spaces (we (generally) don't want a single name!)
        if not " " in full_name:
            submit_errors.append(error_msgs["invalid_name"])

        # Check if ssn has 11 characters (standard for Norwegian)
        if len(request.form["ssn"]) != 11:
            submit_errors.append(error_msgs["invalid_ssn"])

        # Check if ID file is in a valid format
        if id_file and extension in ALLOWED_EXTENSIONS:
            id_file.save(f"static/application_imgs/{aplctn_key}.{extension}")
        else:
            submit_errors.append(error_msgs["invalid_img"])

        # Submit the application if form is valid
        if len(submit_errors) == 0:

            application = dict(request.form)
            application["full_name"] = full_name
            application["time"] = str(datetime.now())
            application["image_name"] = f"{aplctn_key}.{extension}"
            application["loan_amt"] = to_monetary_format(application["loan_amt"]) # convert to sexy money number format
            # Politically exposed person (PEP) check
            PEP_result = PEP_lookup(full_name)
            application["PEP_lookup_result"] = PEP_result

            # Construct feedback messages about PEP for user
            PEP_msg = ""
            PEP_funny_msg = ""
            if request.form.get("PEP_self_flag") == "yes":
                PEP_msg = f"""Merk: Du har flagget deg selv som en politisk eksponert person, og blir sendt til manuell behandling."""
            elif PEP_result["numberOfHits"] > 0:
                PEP_funny_msg = f"""Du er en liten luring, du! Selv om du prøvde å slippe unna, fikk vi {PEP_result['numberOfHits']} treff på deg i våre datasett. Du blir sendt til manuell behandling."""

            save_loan_application(aplctn_key, application)
            return render_template("kunde_success.html", PEP_msg=PEP_msg, PEP_funny_msg=PEP_funny_msg)

        # Can not submit
        else:
            return render_template("kunde.html",
            submit_errors=submit_errors,
            form_so_far=request.form)

    else:
        return render_template("kunde.html")

@app.route("/ansatt")
def ansatt():
    """returns HTML template for the employee view"""
    path = "data/loan_applications.json"
    # Loan application data is sent along, so that JavaScript can handle it
    with open(path) as file:
        f = file.read()
        if len(f) < 1:
            applications = {}
        else:
            applications = json.loads(f)
    return render_template("ansatt.html", appl_data=applications)


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
            applications = {} # start with an empty dict/object if file is empty
        else:
            applications = json.loads(f)
    with open(path, "w") as file:
        # applications are stored with keys of format "full name-current time".
        # Example: "Knut_Arild_Hareide-2022-09-18_155259.308949"
        # This is also the format used for image files names, so that images and applications can be associated with each other.
        applications[name] = data
        json.dump(applications, file)

# Convert boring non-money-looking numbers to fun money-looking numbers!
def to_monetary_format(number):
    exp = []
    for i, c in enumerate(reversed(number)):
        if i % 3 == 0:
            exp.append(' ')
        exp.append(c)

    return ''.join(reversed(exp))[0:-1]