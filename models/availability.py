import uuid
from datetime import date, timedelta

from models.database import db


WEEKDAY_LABELS = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}


class Availability(db.Model):
    """
    Plantilla de disponibilidad semanal recurrente de un médico.
    Cada fila representa "este médico atiende los <weekday> a las <time>",
    y se repite todas las semanas. Los turnos concretos reservables se
    materializan en la tabla 'appointments' mediante generate_upcoming_slots().
    """

    __tablename__ = "availabilities"
    __table_args__ = (
        db.UniqueConstraint(
            "doctor_id", "weekday", "time", name="uq_availability_slot"
        ),
    )

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"), nullable=False)
    weekday = db.Column(db.Integer, nullable=False)  # 0=Lunes ... 6=Domingo
    time = db.Column(db.String, nullable=False)      # "HH:MM"

    doctor = db.relationship("Doctor", back_populates="availabilities")

    @property
    def weekday_label(self):
        return WEEKDAY_LABELS.get(self.weekday, str(self.weekday))

    @classmethod
    def find_by_doctor(cls, doctor_id):
        return (
            cls.query
            .filter_by(doctor_id=doctor_id)
            .order_by(cls.weekday, cls.time)
            .all()
        )


def upcoming_dates_for_weekday(weekday, weeks=4, start=None):
    """
    Devuelve la lista de fechas (ISO 'YYYY-MM-DD') correspondientes al
    'weekday' indicado para las próximas 'weeks' semanas, contando desde
    hoy (incluido si hoy coincide con ese weekday).
    """
    today = start or date.today()
    days_ahead = (weekday - today.weekday()) % 7
    first = today + timedelta(days=days_ahead)
    return [(first + timedelta(weeks=w)).isoformat() for w in range(weeks)]


def generate_upcoming_slots(weeks=4):
    """
    Materializa turnos disponibles ('available') para las próximas 'weeks'
    semanas a partir de las plantillas de disponibilidad de todos los médicos.

    Es idempotente: no crea un turno si ya existe un Appointment para el mismo
    doctor_id + date + time en CUALQUIER estado, por lo que no duplica ni pisa
    turnos reservados/cancelados.

    Devuelve la cantidad de turnos nuevos creados.
    """
    # Importación diferida para evitar import circular con appointment.py
    from models.appointment import Appointment

    created = 0
    templates = Availability.query.all()

    for tpl in templates:
        for slot_date in upcoming_dates_for_weekday(tpl.weekday, weeks=weeks):
            exists = (
                Appointment.query
                .filter_by(doctor_id=tpl.doctor_id, date=slot_date, time=tpl.time)
                .first()
            )
            if exists is None:
                db.session.add(
                    Appointment(
                        doctor_id=tpl.doctor_id,
                        date=slot_date,
                        time=tpl.time,
                        status="available",
                    )
                )
                created += 1

    if created:
        db.session.commit()
    return created


def prune_orphan_available_slots(doctor_id):
    """
    Elimina los turnos FUTUROS con status='available' de un médico que ya no
    se corresponden con ninguna de sus plantillas de disponibilidad vigentes.

    No toca turnos reservados/asistidos/cancelados (historial) ni turnos con
    fecha pasada. Devuelve la cantidad de turnos eliminados.
    """
    from models.appointment import Appointment

    valid = {
        (tpl.weekday, tpl.time)
        for tpl in Availability.query.filter_by(doctor_id=doctor_id).all()
    }
    today_iso = date.today().isoformat()

    future_available = (
        Appointment.query
        .filter_by(doctor_id=doctor_id, status="available")
        .filter(Appointment.date >= today_iso)
        .all()
    )

    removed = 0
    for appt in future_available:
        try:
            appt_weekday = date.fromisoformat(appt.date).weekday()
        except ValueError:
            continue
        if (appt_weekday, appt.time) not in valid:
            db.session.delete(appt)
            removed += 1

    if removed:
        db.session.commit()
    return removed
