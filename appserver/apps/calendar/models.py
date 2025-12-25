from datetime import timezone, datetime
from typing import TYPE_CHECKING
from pydantic import AwareDatetime
from sqlalchemy_utc import UtcDateTime
from sqlmodel import SQLModel, Field, Relationship, Text, JSON, func
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from appserver.apps.account.models import User

class Calendar(SQLModel, table=True):
    __tablename__ = "calendars" # type: ignore[arg-type]

    id: int = Field(default=None, primary_key=True)
    topics: list[str] = Field(sa_type=JSON().with_variant(JSONB(astext_type=Text()), "postgresql"), description="Topics for discussion with guests")
    google_calendar_id: str = Field(max_length=1024, description="Google Calendar ID")

    host_id: int = Field(foreign_key="users.id", unique=True)
    host: "User" = Relationship(back_populates="calendar")
    
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
