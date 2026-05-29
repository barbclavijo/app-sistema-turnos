from models.user import User
from models.profile import Profile


class AuthService:

    @staticmethod
    def authenticate(email, password):
        return User.verify(email, password)

    @staticmethod
    def register(first_name, last_name, email, password,
                 role="patient", dni=None, birth_date=None, phone=None):
        if User.find_one_by_email(email):
            return False, "El email ya se encuentra registrado."
        if dni and Profile.find_one_by_dni(dni):
            return False, "El DNI ya se encuentra registrado."

        user = User(email, password, role)
        created = user.save() and Profile(
            user.id, first_name, last_name, dni, birth_date, phone
        ).save()

        if created:
            return True, None
        return False, "Ocurrió un error al crear la cuenta."
