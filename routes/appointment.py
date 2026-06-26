from flask import Blueprint

from controllers.appointment_controller import AppointmentController
from controllers.auth_controller import login_required

appointment_bp = Blueprint("appointment", __name__)


@appointment_bp.route("/turnos", methods=["GET", "POST"])
@login_required
def select():
    return AppointmentController.select()


@appointment_bp.route("/mis_turnos")
@login_required
def my_appointments():
    return AppointmentController.my_appointments()
