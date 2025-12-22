from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint

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
    created_at: datetime
    updated_at: datetime
