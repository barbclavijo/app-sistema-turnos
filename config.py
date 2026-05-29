import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "database", "consultorio.db")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")