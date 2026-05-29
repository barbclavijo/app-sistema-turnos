from models.database import Database


class AppConfig:

    @staticmethod
    def get(key):
        connection = None
        try:
            connection = Database.connect()
            row = connection.execute(
                "SELECT value FROM app_config WHERE key = ?", (key,)
            ).fetchone()
            return row[0] if row else None
        except Exception as error:
            print(f"Error al leer config: {error}")
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def set(key, value):
        connection = None
        try:
            connection = Database.connect()
            connection.execute(
                "INSERT INTO app_config (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value)
            )
            connection.commit()
            return True
        except Exception as error:
            print(f"Error al guardar config: {error}")
            return False
        finally:
            if connection:
                connection.close()
