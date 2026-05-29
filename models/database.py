import os
import sqlite3
import config

SCHEMA_PATH = os.path.join(config.BASE_DIR, "database", "schema.sql")


class Database:

    @staticmethod
    def connect():
        return sqlite3.connect(config.DB_PATH)

    @staticmethod
    def create_db():

        connection = None

        try:

            connection = Database.connect()

            with open(SCHEMA_PATH, encoding="utf-8") as schema:
                connection.executescript(schema.read())

            connection.commit()

            print("Esquema aplicado correctamente.")

        except (sqlite3.Error, OSError) as error:

            print(
                f"Error al aplicar el esquema: {error}"
            )

        finally:

            if connection:
                connection.close()
                print("Conexión cerrada.")
