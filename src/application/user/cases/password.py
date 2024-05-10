import hashlib


class UserPasswordService:

    @staticmethod
    def create_password(password: str, salt: str) -> str:
        encoded_password = (salt + password).encode("utf-8")
        h = hashlib.sha1(encoded_password)
        return h.hexdigest()
