-- Esquema de la base de datos (migración)
-- Se ejecuta con Database.create_db() al iniciar la app.

CREATE TABLE IF NOT EXISTS users (
    id          TEXT PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    role        TEXT NOT NULL DEFAULT 'patient',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS profiles (
    id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL UNIQUE REFERENCES users(id),
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    dni         TEXT UNIQUE,
    birth_date  TEXT,
    phone       TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS doctors (
    id          TEXT PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    specialty   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id               TEXT PRIMARY KEY,
    doctor_id        TEXT NOT NULL REFERENCES doctors(id),
    date             TEXT NOT NULL,
    time             TEXT NOT NULL,
    patient_user_id  TEXT REFERENCES users(id),
    status           TEXT NOT NULL DEFAULT 'available',
    created_at       TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS app_config (
    key    TEXT PRIMARY KEY,
    value  TEXT NOT NULL
);
