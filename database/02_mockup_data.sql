-- Datos ficticios para visualización (médicos y turnos).

INSERT OR IGNORE INTO doctors (id, first_name, last_name, specialty) VALUES
  ('doc-elena', 'Elena', 'Rivas', 'Cardiología'),
  ('doc-marcos', 'Marcos', 'Julián', 'Dermatología');

INSERT OR IGNORE INTO appointments (id, doctor_id, date, time) VALUES
  ('apt-e-01', 'doc-elena', '2026-06-02', '09:00'),
  ('apt-e-02', 'doc-elena', '2026-06-02', '09:30'),
  ('apt-e-03', 'doc-elena', '2026-06-02', '10:00'),
  ('apt-e-04', 'doc-elena', '2026-06-02', '14:00'),
  ('apt-e-05', 'doc-elena', '2026-06-03', '09:00'),
  ('apt-e-06', 'doc-elena', '2026-06-03', '09:30'),
  ('apt-e-07', 'doc-elena', '2026-06-03', '10:00'),
  ('apt-e-08', 'doc-elena', '2026-06-03', '14:00'),
  ('apt-m-01', 'doc-marcos', '2026-06-02', '09:00'),
  ('apt-m-02', 'doc-marcos', '2026-06-02', '09:30'),
  ('apt-m-03', 'doc-marcos', '2026-06-02', '10:00'),
  ('apt-m-04', 'doc-marcos', '2026-06-02', '14:00'),
  ('apt-m-05', 'doc-marcos', '2026-06-03', '09:00'),
  ('apt-m-06', 'doc-marcos', '2026-06-03', '09:30'),
  ('apt-m-07', 'doc-marcos', '2026-06-03', '10:00'),
  ('apt-m-08', 'doc-marcos', '2026-06-03', '14:00');
