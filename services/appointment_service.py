from models.appointment import Appointment


class AppointmentService:

    @staticmethod
    def book(appointment_id, patient_user_id):
        return bool(appointment_id) and Appointment.book(appointment_id, patient_user_id)

    @staticmethod
    def find_all_by_patient(patient_user_id):
        return Appointment.find_all_by_patient(patient_user_id)

    @staticmethod
    def find_available():
        by_id = {}
        for r in Appointment.find_all_available():
            doctor = by_id.setdefault(r["doctor_id"], {
                "id": r["doctor_id"],
                "name": f"{r['first_name']} {r['last_name']}",
                "specialty": r["specialty"],
                "dates": {}
            })
            doctor["dates"].setdefault(r["date"], []).append(
                {"id": r["id"], "time": r["time"]}
            )

        doctors = []
        for doctor in by_id.values():
            doctor["dates"] = [
                {"date": date, "slots": slots}
                for date, slots in sorted(doctor["dates"].items())
            ]
            doctors.append(doctor)

        specialties = sorted({d["specialty"] for d in doctors})
        return doctors, specialties
