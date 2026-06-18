import uuid

from models.database import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String, db.ForeignKey("users.id"), nullable=False, unique=True
    )
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    dni = db.Column(db.String, unique=True)
    birth_date = db.Column(db.String)
    phone = db.Column(db.String)
    created_at = db.Column(
        db.String, nullable=False, server_default=db.text("(datetime('now'))")
    )

    user = db.relationship("User", back_populates="profile")

    @classmethod
    def find_one_by_dni(cls, dni):
        return cls.query.filter_by(dni=dni).first()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(f"Error al guardar el perfil: {error}")
            return False
