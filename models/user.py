import uuid
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from models.database import Database


class User:

    def __init__(self, email, password, role="patient"):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    @staticmethod
    def find_one_by_email(email):
        connection = None
        try:
            connection = Database.connect()
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            return cursor.fetchone()
        except Exception as error:
            print(f"Error al buscar usuario por email: {error}")
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def find_one_with_profile(user_id):
        connection = None
        try:
            connection = Database.connect()
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT u.id, u.email, u.role, p.first_name, p.last_name
                FROM users u
                LEFT JOIN profiles p ON p.user_id = u.id
                WHERE u.id = ?
                """,
                (user_id,)
            )
            return cursor.fetchone()
        except Exception as error:
            print(f"Error al buscar usuario con perfil: {error}")
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def verify(email, password):
        user = User.find_one_by_email(email)
        if user and check_password_hash(user["password"], password):
            return user
        return None

    def save(self):
        connection = None
        try:
            connection = Database.connect()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (id, email, password, role) VALUES (?, ?, ?, ?)",
                (self.id, self.email, self.password, self.role)
            )
            connection.commit()
            return True
        except Exception as error:
            print(f"Error al guardar el usuario: {error}")
            return False
        finally:
            if connection:
                connection.close()
