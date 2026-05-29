# app-sistema-turnos

Proyecto académico: Sistema web de gestión de turnos para una clínica médica, desarrollado con Flask, MVC y SQLITE.

## Requisitos

- Python 3.13+
- Flask (ya instalado en el entorno virtual `.venv`)

## Cómo ejecutar (Windows)

1. Activar el entorno virtual:

   ```
   .venv\Scripts\activate
   ```

2. (solo si Flask no está instalado) instalarlo:

   ```
   pip install flask
   ```

3. Generar la base de datos y crear las tablas (aplica `database/schema.sql`):

   ```
   python -c "from models.database import Database; Database.create_db()"
   ```

4. Iniciar la aplicación (si la DB no existe, también la genera):
   ```
   python app.py
   ```

La app queda disponible en http://127.0.0.1:5000

## Base de datos

- El archivo `database/consultorio.db` (SQLite) se crea automáticamente al conectarse; no se define en una query (SQLite no usa `CREATE DATABASE`).
- El esquema de tablas vive en `database/schema.sql` y se aplica con `Database.create_db()`.
