from flask import Blueprint
from controllers.doctor_controller import DoctorController
from controllers.auth_controller import role_required

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/doctor/create', methods=['GET', 'POST'])
@role_required('admin')
def create():
    return DoctorController.create()
