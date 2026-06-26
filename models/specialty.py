import uuid

from models.database import db


class Specialty(db.Model):
    __tablename__ = 'specialties'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Specialty {self.name}>"
