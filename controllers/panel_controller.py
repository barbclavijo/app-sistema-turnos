from flask import render_template, request, redirect, url_for
from models.profile import Profile
from models.user import User
from models.appointment import Appointment
from datetime import date


class PanelController:
    @staticmethod
    def index():
        if request.method == 'POST':
            dni = request.form.get('dni', '').strip()
            if dni:
                return redirect(url_for('profile.patient', dni=dni))

        patients_count = 0
        todays_appointments = 0
        pending_appointments = 0
        upcoming = []
        try:
            # Contar solo perfiles de usuarios con rol 'patient'
            patients_count = (
                Profile.query.join(User, Profile.user)
                .filter(User.role == 'patient')
                .count()
            )
            today = date.today().isoformat()
            todays_appointments = Appointment.query.filter_by(date=today).count()
            pending_appointments = Appointment.query.filter_by(status='booked').count()
            upcoming = Appointment.query.filter_by(status='booked').order_by(Appointment.date, Appointment.time).limit(5).all()
        except Exception:
            pass

        stats = {
            'patients_count': patients_count,
            'todays_appointments': todays_appointments,
            'pending_appointments': pending_appointments
        }

        return render_template('panel/panel.html', stats=stats, upcoming=upcoming)
