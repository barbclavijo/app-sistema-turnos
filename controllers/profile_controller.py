from flask import (
    render_template,
    request
)

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
                message = "Paciente registrado correctamente." if ok else error

        return render_template("profile/create_patient.html", message=message)
