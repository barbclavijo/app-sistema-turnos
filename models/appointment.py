import sqlite3

from models.database import Database


class Appointment:

    @staticmethod
    def find_all_available():
        connection = None
        try:
            connection = Database.connect()
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT a.id, a.date, a.time,
                       d.id AS doctor_id, d.first_name, d.last_name, d.specialty
                FROM appointments a
                JOIN doctors d ON d.id = a.doctor_id
                WHERE a.status = 'available'
                ORDER BY d.last_name, a.date, a.time
                """
            )
            return cursor.fetchall()
        except Exception as error:
            print(f"Error al listar turnos disponibles: {error}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def find_all_by_patient(patient_user_id):
        connection = None
        try:
            connection = Database.connect()
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT a.id, a.date, a.time,
                       d.first_name, d.last_name, d.specialty
                FROM appointments a
                JOIN doctors d ON d.id = a.doctor_id
                WHERE a.patient_user_id = ? AND a.status = 'booked'
                ORDER BY a.date, a.time
                """,
                (patient_user_id,)
            )
            return cursor.fetchall()
        except Exception as error:
            print(f"Error al listar turnos del paciente: {error}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def book(appointment_id, patient_user_id):
        connection = None
        try:
            connection = Database.connect()
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE appointments
                SET patient_user_id = ?, status = 'booked'
                WHERE id = ? AND status = 'available'
                """,
                (patient_user_id, appointment_id)
            )
            connection.commit()
            return cursor.rowcount > 0
        except Exception as error:
            print(f"Error al reservar el turno: {error}")
            return False
        finally:
            if connection:
                connection.close()
