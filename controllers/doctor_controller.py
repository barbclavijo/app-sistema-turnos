from flask import render_template, request, redirect, url_for, flash
from models.doctor import Doctor
from models.specialty import Specialty
from models.appointment import Appointment
from models.database import db
from datetime import date, timedelta
import uuid


class DoctorController:

    @staticmethod
    def create():
        message = ""
        specialties = Specialty.query.order_by(Specialty.name).all()

        if request.method == 'POST':
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            specialty_name = request.form.get('specialty')

            if not first_name or not last_name or not specialty_name:
                message = 'Complete todos los campos.'
            else:
                doc_id = f"doc-{first_name.lower()}-{last_name.lower()[:5]}-{str(uuid.uuid4())[:6]}"
                doctor = Doctor(id=doc_id, first_name=first_name, last_name=last_name, specialty=specialty_name)
                try:
                    db.session.add(doctor)
                    times = ["09:00", "09:30", "10:00", "14:00"]
                    today = date.today()
                    slots = []
                    for offset in range(1, 8):
                        slot_date = (today + timedelta(days=offset)).isoformat()
                        for t in times:
                            slots.append((slot_date, t))
                    for idx, (d, t) in enumerate(slots, start=1):
                        appt = Appointment(id=f"apt-{doc_id}-{idx:03d}", doctor_id=doc_id, date=d, time=t)
                        db.session.add(appt)

                    db.session.commit()
                    flash('Médico dado de alta y disponibilidad asignada.', 'success')
                    return redirect(url_for('doctor.create'))
                except Exception as e:
                    db.session.rollback()
                    message = f'Error al crear médico: {e}'

        return render_template('doctor/create_doctor.html', specialties=specialties, message=message)
