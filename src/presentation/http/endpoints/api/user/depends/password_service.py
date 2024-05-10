from src.application.user.cases.password import UserPasswordService


def get_password_service() -> UserPasswordService:
    return UserPasswordService()
