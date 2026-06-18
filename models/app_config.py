from models.database import db


class AppConfig(db.Model):
    __tablename__ = "app_config"

    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String, nullable=False)

    @classmethod
    def get(cls, key):
        try:
            row = db.session.get(cls, key)
            return row.value if row else None
        except Exception as error:
            print(f"Error al leer config: {error}")
            return None

    @classmethod
    def set(cls, key, value):
        try:
            row = db.session.get(cls, key)
            if row:
                row.value = value
            else:
                db.session.add(cls(key=key, value=value))
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(f"Error al guardar config: {error}")
            return False
