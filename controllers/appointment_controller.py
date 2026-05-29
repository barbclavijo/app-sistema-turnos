from flask import (
    render_template,
    request,
    session
)

from models.appointment import Appointment


class AppointmentController:

    @staticmethod
    def select():

        message = ""

        if request.method == "POST":

            appointment_id = request.form.get("appointment_id")

            if appointment_id and Appointment.book(appointment_id, session["user_id"]):
                message = "Turno reservado correctamente."
            else:
                message = "No se pudo reservar el turno."

        doctors = AppointmentController._group(Appointment.available())
        specialties = sorted({d["specialty"] for d in doctors})

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
            appointments=Appointment.for_patient(session["user_id"])
        )

    @staticmethod
    def _group(rows):
        by_id = {}
        for r in rows:
            doctor = by_id.setdefault(r["doctor_id"], {
                "id": r["doctor_id"],
                "name": f"{r['first_name']} {r['last_name']}",
                "specialty": r["specialty"],
                "dates": {}
            })
            doctor["dates"].setdefault(r["date"], []).append(
                {"id": r["id"], "time": r["time"]}
            )

        result = []
        for doctor in by_id.values():
            doctor["dates"] = [
                {"date": date, "slots": slots}
                for date, slots in sorted(doctor["dates"].items())
            ]
            result.append(doctor)
        return result
