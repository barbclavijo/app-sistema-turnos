import uuid

from models.database import Database


class Patient:

    def __init__(self, first_name, last_name, dni, birth_date, email, phone):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.birth_date = birth_date
        self.email = email
        self.phone = phone

    @staticmethod
    def find_by_dni(dni):
        connection = None
        try:
            connection = Database.connect()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM patients WHERE dni = ?",
                (dni,)
            )
            return cursor.fetchone()
        except Exception as error:
            print(f"Error al buscar paciente por dni: {error}")
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
                INSERT INTO patients (
                    id, first_name, last_name, dni, birth_date, email, phone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.id,
                    self.first_name,
                    self.last_name,
                    self.dni,
                    self.birth_date,
                    self.email,
                    self.phone
                )
            )
            connection.commit()
            return True
        except Exception as error:
            print(f"Error al guardar datos del paciente: {error}")
            return False
        finally:
            if connection:
                connection.close()
