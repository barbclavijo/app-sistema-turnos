from functools import wraps

from flask import (
    render_template,
    request,
    redirect,
    session
)

from models.user import User
from services.auth_service import AuthService


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/signin")
        return view(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/signin")
            user = User.find_one_with_profile(session["user_id"])
            if not user or user["role"] != role:
                return redirect("/turnos")
            return view(*args, **kwargs)
        return wrapper
    return decorator


class AuthController:

    @staticmethod
    def signin():

        message = ""

        if request.method == "POST":

            email = request.form.get("email").strip()
            password = request.form.get("password")

            if not email or not password:
                message = "Complete email y contraseña."
            else:
                user = AuthService.authenticate(email, password)

                if user:
                    session["user_id"] = user["id"]
                    if user["role"] == "admin":
                        return redirect("/create_patient")
                    return redirect("/turnos")

                message = "Email o contraseña incorrectos."

        return render_template("auth/signin.html", message=message)

    @staticmethod
    def signup():

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
                ok, error = AuthService.register(first_name, last_name, email, password)
                message = "Cuenta creada correctamente." if ok else error

        return render_template("auth/signup.html", message=message)

    @staticmethod
    def logout():
        session.clear()
        return redirect("/signin")
