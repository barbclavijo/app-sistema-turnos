import os
import glob
import sqlite3
import config

SQL_DIR = os.path.join(config.BASE_DIR, "database")


class Database:

    @staticmethod
    def connect():
        return sqlite3.connect(config.DB_PATH)

    @staticmethod
    def create_db():

        connection = None

        try:

            connection = Database.connect()

            for path in sorted(glob.glob(os.path.join(SQL_DIR, "*.sql"))):
                with open(path, encoding="utf-8") as sql_file:
                    connection.executescript(sql_file.read())

            connection.commit()

            print("Esquema y datos aplicados correctamente.")

        except (sqlite3.Error, OSError) as error:

            print(
                f"Error al aplicar el esquema: {error}"
            )

        finally:

            if connection:
                connection.close()
                print("Conexión cerrada.")
