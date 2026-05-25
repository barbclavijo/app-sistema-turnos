import sqlite3
import config


class Database:

    @staticmethod
    def connect():
        return sqlite3.connect(config.DB_PATH)

    @staticmethod
    def create_db():

        connection = None

        try:

            connection = Database.connect()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    dni INTEGER UNIQUE NOT NULL,
                    fecha_nac TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefono TEXT NOT NULL
                )
            """)

            connection.commit()

            print(
                "Base de datos y tabla pacientes creada exitosamente."
            )

        except sqlite3.Error as error:

            print(
                f"Error al conectar a la base de datos: {error}"
            )

        finally:

            if connection:
                connection.close()
                print("Conexión cerrada.")