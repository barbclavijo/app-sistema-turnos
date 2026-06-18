from models.database import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)

    appointments = db.relationship("Appointment", back_populates="doctor")
