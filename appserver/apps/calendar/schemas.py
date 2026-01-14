from typing import Annotated
from pydantic import AfterValidator, AwareDatetime, EmailStr, model_validator
from sqlmodel import SQLModel, Field
from appserver.libs.collections.sort import deduplicate_and_sort
from datetime import time, date


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

 
def validate_weekdays(weekdays: list[int]) -> list[int]:
    weekday_range = range(7)
    for weekday in weekdays:
        if weekday not in weekday_range:
            raise ValueError(f"Weekday value must be between 0 and 6. Got: {weekday}")
    return weekdays
    
Weekdays = Annotated[list[int], AfterValidator(validate_weekdays)]


class TimeSlotCreateIn(SQLModel):
    start_time: time
    end_time: time
    weekdays: Weekdays
    @model_validator(mode="after")
    def validate_time_slot(self):
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be earlier than end time.")
        return self


class TimeSlotOut(SQLModel):
    start_time: time
    end_time: time
    weekdays: Weekdays
    created_at: AwareDatetime
    updated_at: AwareDatetime


class BookingCreateIn(SQLModel):
    when: date
    topic: str
    description: str
    time_slot_id: int


class BookingOut(SQLModel):
    id: int
    when: date
    topic: str
    description: str
    time_slot: TimeSlotOut
    created_at: AwareDatetime
    updated_at: AwareDatetime
