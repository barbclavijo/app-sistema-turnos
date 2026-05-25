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

            nombre = request.form.get("nombre").strip()
            apellido = request.form.get("apellido").strip()
            dni = request.form.get("dni").strip()
            fecha_nac = request.form.get("fecha_nac").strip()
            email = request.form.get("email").strip()
            telefono = request.form.get("telefono").strip()

            if (
                not nombre or
                not apellido or
                not dni or
                not email or
                not telefono
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
                patient = Patient(nombre, apellido, dni, fecha_nac, email, telefono)
                saved = patient.save()

                if saved:

                    message = ("Paciente registrado correctamente.")

                else:

                    message = ("Ocurrió un error al registrar el paciente.")

        return render_template(
            "create_patient.html",
            message=message
        )