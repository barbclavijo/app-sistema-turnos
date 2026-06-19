from flask_sqlalchemy import SQLAlchemy


# Se inicializa en app.py con db.init_app(app).
db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        db.create_all()
        seed_data()


def seed_data():
    from models.doctor import Doctor
    from models.appointment import Appointment
    from models.specialty import Specialty
    from datetime import date, timedelta
    import uuid
    default_specialties = [
        'Cardiología', 'Dermatología', 'Pediatría', 'Neurología', 'Ginecología',
        'Traumatología', 'Oftalmología', 'Psiquiatría', 'Endocrinología', 'Nefrología'
    ]
    existing = {s.name for s in Specialty.query.all()}
    for name in default_specialties:
        if name not in existing:
            db.session.add(Specialty(name=name))

    if Doctor.query.first() is None:
        db.session.add_all([
            Doctor(id="doc-elena", first_name="Elena", last_name="Rivas", specialty="Cardiología"),
            Doctor(id="doc-marcos", first_name="Marcos", last_name="Julián", specialty="Dermatología"),
        ])

        times = ["09:00", "09:30", "10:00", "14:00"]
        today = date.today()
        slots = []
        for offset in range(1, 4):
            slot_date = (today + timedelta(days=offset)).isoformat()
            for t in times:
                slots.append((slot_date, t))

        for index, (d, t) in enumerate(slots, start=1):
            db.session.add_all([
                Appointment(id=f"apt-e-{index:02d}", doctor_id="doc-elena", date=d, time=t),
                Appointment(id=f"apt-m-{index:02d}", doctor_id="doc-marcos", date=d, time=t),
            ])

    db.session.commit()
