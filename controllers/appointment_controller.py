from flask import (
    render_template,
    request,
    session
)

from services.appointment_service import AppointmentService


class AppointmentController:

    @staticmethod
    def select():

        message = ""

        if request.method == "POST":
            appointment_id = request.form.get("appointment_id")

            if AppointmentService.book(appointment_id, session["user_id"]):
                message = "Turno reservado correctamente."
            else:
                message = "No se pudo reservar el turno."

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
