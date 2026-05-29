from models.app_config import AppConfig
from services.auth_service import AuthService

SETUP_FLAG = "setup_done"


class SetupService:

    @staticmethod
    def is_done():
        return AppConfig.get(SETUP_FLAG) == "true"

    @staticmethod
    def complete(first_name, last_name, email, password):
        ok, error = AuthService.register(
            first_name, last_name, email, password, role="admin"
        )
        if ok:
            AppConfig.set(SETUP_FLAG, "true")
        return ok, error
