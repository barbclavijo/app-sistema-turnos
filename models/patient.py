from models.database import Database


class Patient:

    def __init__(self, nombre, apellido, dni, fecha_nac, email, telefono):

        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fecha_nac = fecha_nac
        self.email = email
        self.telefono = telefono

    @staticmethod
    def find_by_dni(dni):

        connection = None

        try:

            connection = Database.connect()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT * 
                FROM pacientes
                WHERE dni = ?
                """,
                (dni,)
            )

            patient = cursor.fetchone()

            return patient

        except Exception as error:

            print(
                f"Error al buscar paciente por dni: {error}"
            )

            return None

        finally:

            if connection:
                connection.close()

    def save(self):

        connection = None

        try:

            connection = Database.connect()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO pacientes (
                    nombre,
                    apellido,
                    dni,
                    fecha_nac,
                    email,
                    telefono
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.nombre,
                self.apellido,
                self.dni,
                self.fecha_nac,
                self.email,
                self.telefono
            ))

            connection.commit()

            return True

        except Exception as error:

            print(
                f"Error al guardar datos del paciente: {error}"
            )

            return False

        finally:

            if connection:
                connection.close()