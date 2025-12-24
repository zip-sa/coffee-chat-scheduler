from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from pydantic import AwareDatetime, EmailStr
from sqlalchemy import UniqueConstraint
from sqlalchemy_utc import UtcDateTime
from sqlalchemy.sql import func

class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_email"),
    )

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=40, description="User Account ID")
    email: EmailStr = Field(max_length=128, description="User Email Address")
    display_name: str = Field(max_length=40, description="User Display Name")
    password: str = Field(max_length=128, description="User Password")
    is_host: bool = Field(default=False, description="Check Host")
    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
