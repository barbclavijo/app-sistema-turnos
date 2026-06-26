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
        """Turnos activos del paciente (para la vista 'Mis Turnos')."""
        return (
            cls.query
            .filter(cls.patient_user_id == patient_user_id)
            .filter(cls.status.in_(["booked", "attended"]))
            .order_by(cls.date, cls.time)
            .all()
        )

    @classmethod
    def find_history_by_patient(cls, patient_user_id):
        """
        Historial completo de turnos del paciente, incluyendo los
        cancelados y los ya asistidos. Se usa en el panel del admin.
        """
        return (
            cls.query
            .filter(cls.patient_user_id == patient_user_id)
            .filter(cls.status.in_(["booked", "attended", "cancelled"]))
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

    @classmethod
    def update_status(cls, appointment_id, new_status_label):
        """
        Update appointment status based on Spanish label.
        Allowed labels: 'Pendiente', 'Asistió', 'Cancelado'.

        Al cancelar NO se borra el turno ni se pierde el paciente: el registro
        queda con status 'cancelled' y conserva su 'patient_user_id' para
        mantener el historial. Para que el horario vuelva a estar disponible
        se crea un nuevo slot 'available' con el mismo médico, fecha y hora.
        """
        mapping = {
            "Pendiente": "booked",
            "Asistió": "attended",
            "Cancelado": "cancelled",
        }

        if new_status_label not in mapping:
            return False, "Estado inválido."

        try:
            appointment = cls.query.filter_by(id=appointment_id).first()
            if appointment is None:
                return False, "Turno no encontrado."

            if new_status_label == "Cancelado":
                # Conservamos el turno cancelado como registro histórico
                # (no se borra patient_user_id) y liberamos el horario
                appointment.status = mapping[new_status_label]
                db.session.add(
                    cls(
                        doctor_id=appointment.doctor_id,
                        date=appointment.date,
                        time=appointment.time,
                        status="available",
                    )
                )
            else:
                appointment.status = mapping[new_status_label]

            db.session.commit()
            return True, None
        except Exception as error:
            db.session.rollback()
            print(f"Error al actualizar estado del turno: {error}")
            return False, str(error)
