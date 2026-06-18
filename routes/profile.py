from flask import Blueprint

from controllers.profile_controller import ProfileController
from controllers.auth_controller import role_required

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/create_patient", methods=["GET", "POST"])
@role_required("admin")
def create_patient():
    return ProfileController.create_patient()
