from flask import Blueprint

from controllers.setup_controller import SetupController

setup_bp = Blueprint("setup", __name__)


@setup_bp.route("/setup", methods=["GET", "POST"])
def setup():
    return SetupController.setup()
