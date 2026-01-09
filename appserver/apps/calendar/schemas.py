from typing import Annotated
from pydantic import AfterValidator, AwareDatetime, EmailStr
from sqlmodel import SQLModel, Field
from appserver.libs.collections.sort import deduplicate_and_sort


class CalendarOut(SQLModel):
    topics: list[str]
    description: str


class CalendarDetailOut(CalendarOut):
    host_id: int
    google_calendar_id: str
    created_at: AwareDatetime
    updated_at: AwareDatetime


Topics = Annotated[list[str], AfterValidator(deduplicate_and_sort)]

class CalendarCreateIn(SQLModel):
    topics: Topics = Field(min_length=1, description="Topics to share with guests")
    description: str = Field(min_length=10, description="Description shown to guests")
    google_calendar_id: EmailStr = Field(description="Google Calendar ID")


class CalendarUpdateIn(SQLModel):
    topics: Topics | None = Field(
        default=None,
        min_length=1,
        description="Topics to share with guests",
    )
    description: str | None = Field(
        default=None,
        min_length=10,
        description="Description shown to guests")
    google_calendar_id: EmailStr | None = Field(
        default=None,
        min_length=20,
        description="Google Calendar ID",
        )
    