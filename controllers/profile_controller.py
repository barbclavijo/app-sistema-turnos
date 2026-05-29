from flask import (
    render_template,
    request
)

from models.user import User
from models.profile import Profile


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
            elif User.find_by_email(email):
                message = "El email ya se encuentra registrado."
            elif Profile.find_by_dni(dni):
                message = "El DNI ya se encuentra registrado."
            else:
                user = User(email, password)

                if user.save() and Profile(
                    user.id, first_name, last_name, dni, birth_date, phone
                ).save():
                    message = "Paciente registrado correctamente."
                else:
                    message = "Ocurrió un error al registrar el paciente."

        return render_template("profile/create_patient.html", message=message)
