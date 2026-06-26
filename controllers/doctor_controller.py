from flask import render_template, request, redirect, url_for, flash
from models.doctor import Doctor
from models.specialty import Specialty
from models.availability import (
    Availability,
    WEEKDAY_LABELS,
    generate_upcoming_slots,
    prune_orphan_available_slots,
)
from models.database import db
import uuid


class DoctorController:

    @staticmethod
    def index():
        doctors = Doctor.query.order_by(Doctor.last_name, Doctor.first_name).all()
        return render_template('doctor/list_doctors.html', doctors=doctors)

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
                doctor = Doctor(
                    id=doc_id,
                    first_name=first_name,
                    last_name=last_name,
                    specialty=specialty_name,
                )
                try:
                    db.session.add(doctor)
                    db.session.commit()
                    flash('Médico dado de alta. Cargá su disponibilidad semanal.', 'success')
                    return redirect(url_for('doctor.edit', doctor_id=doc_id))
                except Exception as e:
                    db.session.rollback()
                    message = f'Error al crear médico: {e}'

        return render_template('doctor/create_doctor.html', specialties=specialties, message=message)

    @staticmethod
    def edit(doctor_id):
        doctor = db.session.get(Doctor, doctor_id)
        if doctor is None:
            flash('Médico no encontrado.', 'error')
            return redirect(url_for('doctor.index'))

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'specialty':
                specialty_name = request.form.get('specialty')
                if specialty_name:
                    doctor.specialty = specialty_name
                    db.session.commit()
                    flash('Especialidad actualizada.', 'success')
                else:
                    flash('Seleccione una especialidad.', 'error')

            elif action == 'add':
                weekday_raw = request.form.get('weekday')
                time = (request.form.get('time') or '').strip()
                try:
                    weekday = int(weekday_raw)
                except (TypeError, ValueError):
                    weekday = None

                if weekday is None or weekday not in WEEKDAY_LABELS or not time:
                    flash('Indicá día y horario válidos.', 'error')
                else:
                    exists = Availability.query.filter_by(
                        doctor_id=doctor_id, weekday=weekday, time=time
                    ).first()
                    if exists:
                        flash('Ese día y horario ya está cargado.', 'info')
                    else:
                        db.session.add(
                            Availability(doctor_id=doctor_id, weekday=weekday, time=time)
                        )
                        db.session.commit()
                        generate_upcoming_slots(weeks=4)
                        flash('Disponibilidad agregada.', 'success')

            elif action == 'remove':
                availability_id = request.form.get('availability_id')
                tpl = db.session.get(Availability, availability_id)
                if tpl and tpl.doctor_id == doctor_id:
                    db.session.delete(tpl)
                    db.session.commit()
                    prune_orphan_available_slots(doctor_id)
                    flash('Disponibilidad eliminada.', 'success')
                else:
                    flash('No se encontró la disponibilidad a eliminar.', 'error')

            return redirect(url_for('doctor.edit', doctor_id=doctor_id))

        specialties = Specialty.query.order_by(Specialty.name).all()
        availabilities = Availability.find_by_doctor(doctor_id)
        weekday_options = sorted(WEEKDAY_LABELS.items())
        return render_template(
            'doctor/edit_doctor.html',
            doctor=doctor,
            specialties=specialties,
            availabilities=availabilities,
            weekday_options=weekday_options,
        )
