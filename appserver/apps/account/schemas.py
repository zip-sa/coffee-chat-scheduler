import random
import string
from typing import Self
from pydantic import EmailStr, model_validator, AwareDatetime
from sqlmodel import SQLModel, Field


class SignupPayload(SQLModel):
    username: str = Field(min_length=4, max_length=40, description="User Account ID")
    email: EmailStr = Field(unique=True, max_length=128, description="User Email Address")
    display_name: str = Field(min_length=4, max_length=40, description="User Display Name")
    password: str = Field(min_length=8, max_length=128, description="User Password")
    password_again: str = Field(min_length=8, max_length=128, description="Password Confirmation")

    @model_validator(mode="after")
    def verify_password(self) -> Self:
        if self.password != self.password_again:
            raise ValueError("Passwords do not match")
        return self
    
    @model_validator(mode="before")
    @classmethod
    def generate_display_name(cls, data: dict):
        if not data.get("display_name"):
            data["display_name"] = "".join(random.choices(string.ascii_letters+string.digits, k=8))
        return data
    

class UserOut(SQLModel):
    username: str
    display_name: str
    is_host: bool


class LoginPayload(SQLModel):
    username: str = Field(min_length=4, max_length=40)
    password: str = Field(min_length=8, max_length=128)
    

class UserDetailOut(UserOut):
    email: EmailStr
    created_at: AwareDatetime
    updated_at: AwareDatetime
