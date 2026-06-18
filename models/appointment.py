import uuid

from models.database import db
from models.doctor import Doctor


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"), nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    patient_user_id = db.Column(db.String, db.ForeignKey("users.id"))
    status = db.Column(db.String, nullable=False, default="available")
    created_at = db.Column(
        db.String, nullable=False, server_default=db.text("(datetime('now'))")
    )

    doctor = db.relationship("Doctor", back_populates="appointments")
    patient = db.relationship("User")

    @classmethod
    def find_all_available(cls):
        return (
            cls.query
            .join(Doctor)
            .filter(cls.status == "available")
            .order_by(Doctor.last_name, cls.date, cls.time)
            .all()
        )

    @classmethod
    def find_all_by_patient(cls, patient_user_id):
        return (
            cls.query
            .filter_by(patient_user_id=patient_user_id, status="booked")
            .order_by(cls.date, cls.time)
            .all()
        )

    @classmethod
    def book(cls, appointment_id, patient_user_id):
        try:
            appointment = cls.query.filter_by(
                id=appointment_id, status="available"
            ).first()
            if appointment is None:
                return False
            appointment.patient_user_id = patient_user_id
            appointment.status = "booked"
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(f"Error al reservar el turno: {error}")
            return False
