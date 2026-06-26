import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from models.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default="patient")
    created_at = db.Column(
        db.String, nullable=False, server_default=db.text("(datetime('now'))")
    )

    profile = db.relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __init__(self, email, password, role="patient"):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    @property
    def first_name(self):
        return self.profile.first_name if self.profile else ""

    @property
    def last_name(self):
        return self.profile.last_name if self.profile else ""

    @classmethod
    def find_one_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_one_with_profile(cls, user_id):
        return db.session.get(cls, user_id)

    @classmethod
    def verify(cls, email, password):
        user = cls.find_one_by_email(email)
        if user and check_password_hash(user.password, password):
            return user
        return None

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(f"Error al guardar el usuario: {error}")
            return False
