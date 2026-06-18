# app-sistema-turnos

Proyecto académico: Sistema web de gestión de turnos para una clínica médica, desarrollado con Flask, MVC y SQLAlchemy (ORM) sobre SQLite.

## Requisitos

- Python 3.13+
- Dependencias listadas en `requirements.txt` (Flask, Flask-SQLAlchemy, SQLAlchemy)

## Cómo ejecutar (Windows)

1. Crear el entorno virtual (solo la primera vez):

   ```
   python -m venv .venv
   ```

2. Activar el entorno virtual:

   ```
   .venv\Scripts\activate
   ```

   En PowerShell el comando es `.venv\Scripts\Activate.ps1`. Con el entorno
   activado, el prompt muestra `(.venv)` al inicio.

3. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

4. Iniciar la aplicación:

   ```
   python app.py
   ```

La app queda disponible en http://127.0.0.1:5000

## Base de datos

- Se usa SQLAlchemy (ORM) a través de Flask-SQLAlchemy. La conexión apunta a `database/consultorio.db` (SQLite), configurada en `app.py` mediante `SQLALCHEMY_DATABASE_URI`.
- El esquema se deriva de los modelos ORM (carpeta `models/`) y se crea con `db.create_all()`; los datos de ejemplo se cargan con `seed_data()` (idempotente). Ambos se ejecutan al arrancar desde `init_db(app)` en `models/database.py`.
- Para regenerar la base desde cero, borrá `database/consultorio.db` y volvé a iniciar la app: se recreará el esquema y se generan los datos.
