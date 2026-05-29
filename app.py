from flask import Flask, session
from controllers.profile_controller import ProfileController
from controllers.auth_controller import AuthController, login_required, role_required
from controllers.appointment_controller import AppointmentController
from models.database import Database
from models.user import User
import config

app = Flask(
    __name__,
    template_folder="views/templates"
)
app.secret_key = config.SECRET_KEY

@app.context_processor
def inject_current_user():
    user = None
    if "user_id" in session:
        user = User.with_profile(session["user_id"])
    return {"current_user": user}

@app.route("/")
@app.route("/signin", methods=["GET", "POST"])
def signin():
    return AuthController.signin()

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return AuthController.signup()

@app.route("/logout")
def logout():
    return AuthController.logout()

@app.route("/create_patient", methods=["GET", "POST"])
@role_required("admin")
def create_patient():
    return ProfileController.create_patient()

@app.route("/turnos", methods=["GET", "POST"])
@login_required
def turnos():
    return AppointmentController.select()

@app.route("/mis_turnos")
@login_required
def mis_turnos():
    return AppointmentController.my_appointments()

if __name__ == "__main__":
    Database.create_db()
    app.run(debug=True)
