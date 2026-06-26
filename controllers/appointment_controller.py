from flask import (
    render_template,
    request,
    session
)

from services.appointment_service import AppointmentService
from models.profile import Profile
from models.user import User
from models.availability import generate_upcoming_slots
from flask import redirect, url_for, session, flash


class AppointmentController:

    @staticmethod
    def select():

        message = ""

        try:
            generate_upcoming_slots(weeks=4)
        except Exception as error:
            print(f"Error al generar turnos disponibles: {error}")

        if request.method == "POST":
            appointment_id = request.form.get("appointment_id")
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

        # si un admin llega con un DNI, mostramos a que paciente se le está asignando el turno.
        assign_dni = request.form.get('dni') or request.args.get('dni')
        assign_patient = Profile.find_one_by_dni(assign_dni) if assign_dni else None

        return render_template(
            "appointment/select_appointment.html",
            doctors=doctors,
            specialties=specialties,
            message=message,
            assign_patient=assign_patient,
            assign_dni=assign_dni
        )

    @staticmethod
    def my_appointments():
        return render_template(
            "appointment/my_appointments.html",
            appointments=AppointmentService.find_all_by_patient(session["user_id"])
        )
