from flask import (
    render_template,
    request,
    session
)

from services.appointment_service import AppointmentService
from models.profile import Profile
from models.user import User
from flask import redirect, url_for, session, flash


class AppointmentController:

    @staticmethod
    def select():

        message = ""

        if request.method == "POST":
            appointment_id = request.form.get("appointment_id")
            # if admin is assigning a slot to a patient, a hidden 'dni' may be provided
            dni = request.form.get('dni') or request.args.get('dni')

            if dni:
                patient = Profile.find_one_by_dni(dni)
                if not patient:
                    message = "No existe un paciente con ese DNI. Cree el paciente antes de asignar el turno."
                    flash(message, 'error')
                    doctors, specialties = AppointmentService.find_available()
                    return render_template(
                        "appointment/select_appointment.html",
                        doctors=doctors,
                        specialties=specialties,
                        message=message
                    )
                patient_user_id = patient.user_id
            else:
                patient_user_id = session.get('user_id')
            if AppointmentService.book(appointment_id, patient_user_id):
                try:
                    current_user = User.find_one_with_profile(session.get('user_id'))
                except Exception:
                    current_user = None

                if dni and current_user and current_user.role == 'admin':
                    flash("Turno reservado correctamente.", 'success')
                    return redirect(url_for('profile.patient', dni=dni))
                flash("Turno reservado correctamente.", 'success')
            else:
                flash("No se pudo reservar el turno.", 'error')

        doctors, specialties = AppointmentService.find_available()

        return render_template(
            "appointment/select_appointment.html",
            doctors=doctors,
            specialties=specialties,
            message=message
        )

    @staticmethod
    def my_appointments():
        return render_template(
            "appointment/my_appointments.html",
            appointments=AppointmentService.find_all_by_patient(session["user_id"])
        )
