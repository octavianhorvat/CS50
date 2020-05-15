import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
dbEng = scoped_session(sessionmaker(bind=engine))

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    licencePlates = LicencePlate.query.all()
    for licencePlate in licencePlates:
        print(licencePlate)
    complaints = Complaint.query.all()
    return render_template("index.html", licencePlates=licencePlates, complaints=complaints)


@app.route("/plate/<string:plate>")
def getTemplate(plate):
    plate = plate.capitalize()
    return render_template("index.html", licencePlate=plate)


@app.route("/check", methods=["GET", "POST"])
def check():
    if session.get('notes') is None:
        session['notes'] = []
    if request.method == "POST":
        note = request.form.get("licencePlate")
        session['notes'].append(note)
    return render_template("check.html", name=session['notes'])


@app.route("/addLicence", methods=["POST"])
def addLicence():
    """Add a licencePlate"""

    # Get form information.
    licencePlate = request.form.get("licencePlate")
    address = request.form.get("address")
    insurance = request.form.get("insurance")

    # Validate
    try:
        #flight_id = int(request.form.get("flight_id"))
        if not licencePlate or not address or not insurance:
            return render_template("error.html", message="Invalid data supplied.")
    except ValueError:
        return render_template("error.html", message="Invalid data supplied.")
    licencePlate = LicencePlate(
        licence_plate=licencePlate, insurance=insurance, address=address)
    db.session.add(licencePlate)
    db.session.commit()
    return render_template("success.html")


def main():
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
