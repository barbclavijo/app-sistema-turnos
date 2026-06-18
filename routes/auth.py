from flask import Blueprint

from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
@auth_bp.route("/signin", methods=["GET", "POST"])
def signin():
    return AuthController.signin()


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    return AuthController.signup()


@auth_bp.route("/logout")
def logout():
    return AuthController.logout()
