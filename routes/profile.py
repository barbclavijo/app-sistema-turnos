from flask import Blueprint

from controllers.profile_controller import ProfileController
from controllers.auth_controller import role_required

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/create_patient", methods=["GET", "POST"])
@role_required("admin")
def create_patient():
    return ProfileController.create_patient()

@profile_bp.route("/patient", methods=["GET", "POST"])
@role_required("admin")
def patient():
    return ProfileController.search_patient()


@profile_bp.route("/patient/update_status", methods=["POST"])
@role_required("admin")
def update_status():
    return ProfileController.update_appointment_status()
