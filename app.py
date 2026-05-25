from flask import Flask, render_template
from controllers.patient_controller import PatientController
from models.database import Database

app = Flask(
    __name__,
    template_folder="views/templates"
)

@app.route("/")
def home():
    return "Home"

@app.route("/create_patient", methods=["GET", "POST"])
def create_patient():
    return PatientController.create_patient()

if __name__ == "__main__":
    Database.create_db()
    app.run(debug=True)