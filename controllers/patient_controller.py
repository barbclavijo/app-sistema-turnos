from flask import (
    render_template,
    request
)

from models.patient import Patient


class PatientController:

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

            if (
                not first_name or
                not last_name or
                not dni or
                not email or
                not phone
            ):

                message = (
                    "Todos los campos obligatorios "
                    "deben completarse."
                )

            elif Patient.find_by_dni(dni):

                message = (
                    "El DNI ya se encuentra registrado."
                )

            else:
                patient = Patient(first_name, last_name, dni, birth_date, email, phone)
                saved = patient.save()

                if saved:

                    message = ("Paciente registrado correctamente.")

                else:

                    message = ("Ocurrió un error al registrar el paciente.")

        return render_template(
            "create_patient.html",
            message=message
        )
