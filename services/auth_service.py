from models.database import db
from models.user import User
from models.profile import Profile


class AuthService:

    @staticmethod
    def authenticate(email, password):
        return User.verify(email, password)

    @staticmethod
    def register(first_name, last_name, email, password,role="patient", dni=None, birth_date=None, phone=None):
        if User.find_one_by_email(email):
            return False, "El email ya se encuentra registrado."
        if dni and Profile.find_one_by_dni(dni):
            return False, "El DNI ya se encuentra registrado."

        try:
            user = User(email, password, role)
            user.profile = Profile(
                first_name=first_name,
                last_name=last_name,
                dni=dni,
                birth_date=birth_date,
                phone=phone,
            )
            db.session.add(user)
            db.session.commit()
            return True, None
        except Exception as error:
            db.session.rollback()
            print(f"Error al crear la cuenta: {error}")
            return False, "Ocurrió un error al crear la cuenta."
