from flask import (
    render_template,
    request,
    redirect
)

from services.setup_service import SetupService


class SetupController:

    @staticmethod
    def setup():

        if SetupService.is_done():
            return redirect("/signin")

        message = ""

        if request.method == "POST":

            first_name = request.form.get("first_name").strip()
            last_name = request.form.get("last_name").strip()
            email = request.form.get("email").strip()
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if (
                not first_name or
                not last_name or
                not email or
                not password
            ):
                message = "Todos los campos obligatorios deben completarse."
            elif password != confirm_password:
                message = "Las contraseñas no coinciden."
            else:
                ok, error = SetupService.complete(first_name, last_name, email, password)
                if ok:
                    return redirect("/signin")
                message = error

        return render_template("setup/setup.html", message=message)
