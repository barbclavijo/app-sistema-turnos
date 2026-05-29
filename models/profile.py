import uuid
import sqlite3

from models.database import Database


class Profile:

    def __init__(self, user_id, first_name, last_name,
                 dni=None, birth_date=None, phone=None):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.birth_date = birth_date
        self.phone = phone

    @staticmethod
    def find_by_dni(dni):
        connection = None
        try:
            connection = Database.connect()
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM profiles WHERE dni = ?", (dni,))
            return cursor.fetchone()
        except Exception as error:
            print(f"Error al buscar perfil por dni: {error}")
            return None
        finally:
            if connection:
                connection.close()

    def save(self):
        connection = None
        try:
            connection = Database.connect()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO profiles (
                    id, user_id, first_name, last_name, dni, birth_date, phone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.id,
                    self.user_id,
                    self.first_name,
                    self.last_name,
                    self.dni,
                    self.birth_date,
                    self.phone
                )
            )
            connection.commit()
            return True
        except Exception as error:
            print(f"Error al guardar el perfil: {error}")
            return False
        finally:
            if connection:
                connection.close()
