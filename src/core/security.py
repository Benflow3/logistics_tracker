from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from core.config import settings


class SecurityUtil:
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12)).decode("ascii")

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            return False
        return bcrypt.checkpw(password_bytes, stored_hash.encode("ascii"))

    @staticmethod
    def create_access_token(subject: Any, expire_delta: timedelta) -> str:
        if expire_delta:
            expire = datetime.now(UTC) + timedelta(expire_delta)
        else:
            expire = datetime.now(UTC) + timedelta(
                settings.JWT_EXPIRE_TIME_IN_MINUTE
            )

        _to_encode = {"exp": expire, "sub": subject}
        jwt_encode = jwt.encode(
            _to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return jwt_encode
