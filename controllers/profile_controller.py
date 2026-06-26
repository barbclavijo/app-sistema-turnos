from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models.profile import Profile
from models.appointment import Appointment
from services.auth_service import AuthService


class ProfileController:

    @staticmethod
    def create_patient():

        message = ""

        if request.method == "POST":

            first_name = request.form.get("first_name").strip()
            last_name = request.form.get("last_name").strip()
            dni = request.form.get("dni").strip()
            birth_date = request.form.get("birth_date").strip()
            email = request.form.get("email").strip()
            phone = request.form.get("phone").strip()
            password = request.form.get("password")

            if (
                not first_name or
                not last_name or
                not dni or
                not email or
                not phone or
                not password
            ):
                message = "Todos los campos obligatorios deben completarse."
            else:
                ok, error = AuthService.register(
                    first_name, last_name, email, password,
                    dni=dni, birth_date=birth_date, phone=phone
                )
                if ok:
                    flash("Paciente registrado correctamente.", 'success')
                    return redirect(url_for('profile.patient', dni=dni))
                else:
                    message = error

        return render_template("profile/create_patient.html", message=message)

    @staticmethod
    def search_patient():

        patient = None
        message = ""
        appointments = []
        if request.method == "POST":
            dni = request.form.get("dni", "").strip()
        else:
            dni = request.args.get("dni", "").strip()
            if request.args.get("message"):
                message = request.args.get("message")

        if dni:
            patient = Profile.find_one_by_dni(dni)

            if not patient:
                message = "No existe un paciente con ese DNI."
            else:
                if patient.user_id:
                    appointments = Appointment.find_history_by_patient(patient.user_id)

        return render_template(
            "profile/patient.html",
            patient=patient,
            message=message,
            appointments=appointments
        )

    @staticmethod
    def update_appointment_status():
        message = ""
        patient = None
        appointments = []

        appointment_id = request.form.get("appointment_id")
        new_status = request.form.get("new_status")
        dni = request.form.get("dni", "").strip()

        if not appointment_id or not new_status or not dni:
            message = "Datos incompletos para actualizar el turno."
            flash(message, 'error')
            return redirect(url_for('profile.patient', dni=dni))
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if appointment:
            # Un turno ya cancelado no puede modificarse: queda como registro
            # histórico y su horario ya fue liberado.
            if appointment.status == 'cancelled':
                flash("El turno ya está cancelado y no puede modificarse.", 'error')
                return redirect(url_for('profile.patient', dni=dni))

            current_label = 'Pendiente' if appointment.status == 'booked' else ('Asistió' if appointment.status == 'attended' else 'Cancelado')
            if current_label == new_status:
                message = "El estado seleccionado es igual al actual; no se realizaron cambios."
                flash(message, 'info')
                return redirect(url_for('profile.patient', dni=dni))

        ok, error = Appointment.update_status(appointment_id, new_status)
        message = "Estado actualizado correctamente." if ok else (error or "Error al actualizar estado.")
        flash(message, 'success' if ok else 'error')
        return redirect(url_for('profile.patient', dni=dni))
