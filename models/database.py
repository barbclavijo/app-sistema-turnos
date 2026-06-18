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

    if Doctor.query.first() is not None:
        return

    db.session.add_all([
        Doctor(id="doc-elena", first_name="Elena", last_name="Rivas", specialty="Cardiología"),
        Doctor(id="doc-marcos", first_name="Marcos", last_name="Julián", specialty="Dermatología"),
    ])

    slots = [
        ("2026-06-02", "09:00"),
        ("2026-06-02", "09:30"),
        ("2026-06-02", "10:00"),
        ("2026-06-02", "14:00"),
        ("2026-06-03", "09:00"),
        ("2026-06-03", "09:30"),
        ("2026-06-03", "10:00"),
        ("2026-06-03", "14:00"),
    ]
    for index, (date, time) in enumerate(slots, start=1):
        db.session.add_all([
            Appointment(id=f"apt-e-{index:02d}", doctor_id="doc-elena", date=date, time=time),
            Appointment(id=f"apt-m-{index:02d}", doctor_id="doc-marcos", date=date, time=time),
        ])

    db.session.commit()
