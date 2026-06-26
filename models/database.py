from flask_sqlalchemy import SQLAlchemy


# Se inicializa en app.py con db.init_app(app).
db = SQLAlchemy()


def init_db(app):
    with app.app_context():
       
        import models.user       
        import models.profile    
        import models.doctor     
        import models.specialty 
        import models.appointment  
        import models.availability

        db.create_all()
        seed_data()

        # Materializar los turnos disponibles de las próximas 4 semanas a partir de las plantillas
        from models.availability import generate_upcoming_slots
        generate_upcoming_slots(weeks=4)


def seed_data():
    from models.doctor import Doctor
    from models.specialty import Specialty
    from models.availability import Availability

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

        # Plantillas de disponibilidad semanal recurrente de ejemplo.
        # weekday: 0=Lunes ... 6=Domingo
        example_templates = {
            "doc-elena": [(0, "09:00"), (0, "09:30"), (2, "10:00"), (4, "14:00")],
            "doc-marcos": [(1, "11:00"), (3, "11:30"), (3, "15:00")],
        }
        for doctor_id, slots in example_templates.items():
            for weekday, time in slots:
                db.session.add(
                    Availability(doctor_id=doctor_id, weekday=weekday, time=time)
                )

    db.session.commit()
