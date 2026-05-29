-- Esquema de la base de datos (migración)
-- Se ejecuta con Database.create_db() al iniciar la app.

CREATE TABLE IF NOT EXISTS patients (
    id          TEXT PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    dni         TEXT NOT NULL UNIQUE,
    birth_date  TEXT NOT NULL,
    email       TEXT NOT NULL,
    phone       TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
