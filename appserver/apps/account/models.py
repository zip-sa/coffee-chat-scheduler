from datetime import datetime, timezone
from pydantic import AwareDatetime, EmailStr
from sqlmodel import SQLModel, Field, Relationship, func
from sqlalchemy import UniqueConstraint
from sqlalchemy_utc import UtcDateTime


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

    oauth_accounts: list["OAuthAccount"] = Relationship(back_populates="user")

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

class OAuthAccount(SQLModel, table=True):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_account_id",
            name="uq_provider_provider_account_id",
        ),
    )

    id: int = Field(default=None, primary_key=True)
    provider: str = Field(max_length=10, description="OAuth Provider")
    provider_account_id: str = Field(max_length=128, description="OAuth Provider Account ID")
    
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="oauth_accounts")

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

