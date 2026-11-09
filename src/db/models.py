import uuid
from enum import StrEnum

from sqlalchemy import UUID, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserRole(StrEnum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    DISPATCHER = "dispatcher"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(
        String(225), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), default=UserRole.CUSTOMER, nullable=False
    )
