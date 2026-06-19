from flask import Flask, session, request, redirect, url_for
from services.setup_service import SetupService
from models.database import db, init_db
from models.user import User
from routes.auth import auth_bp
from routes.setup import setup_bp
from routes.appointment import appointment_bp
from routes.profile import profile_bp
from routes.panel import panel_bp
from routes.doctor import doctor_bp
import config

app = Flask(
    __name__,
    template_folder="views/templates"
)
app.secret_key = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + config.DB_PATH.replace("\\", "/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(setup_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(panel_bp)
app.register_blueprint(doctor_bp)

@app.context_processor
def inject_current_user():
    user = None
    if "user_id" in session:
        user = User.find_one_with_profile(session["user_id"])
    return {"current_user": user}

@app.before_request
def require_initial_setup():
    if request.endpoint == "static" or request.path == "/setup":
        return
    if not SetupService.is_done():
        return redirect(url_for("setup.setup"))

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)
