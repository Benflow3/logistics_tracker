import bcrypt


class SecurityUtil:
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            raise ValueError("Password must be at most 72 bytes")
            return bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12)).decode(
                "ascii"
            )

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            return False
        return bcrypt.checkpw(password_bytes, stored_hash.encode("ascii"))
