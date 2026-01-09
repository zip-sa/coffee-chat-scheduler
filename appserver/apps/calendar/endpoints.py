import calendar
from fastapi import APIRouter, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from appserver.apps.account.models import User
from appserver.apps.calendar.models import Calendar
from appserver.db import DbSessionDep
from appserver.apps.account.deps import CurrentUserDep, CurrentUserOptionalDep
from .schemas import CalendarCreateIn, CalendarDetailOut, CalendarOut, CalendarUpdateIn
from .exceptions import CalendarNotFoundError, HostNotFoundError, CalendarAlreadyExistsError, GuestPermissionError


router = APIRouter()
@router.get("/calendar/{host_username}", status_code=status.HTTP_200_OK)

async def host_calendar_detail(
        host_username: str,
        user: CurrentUserOptionalDep,
        session: DbSessionDep
) -> CalendarOut | CalendarDetailOut:
    
    stmt = select(User).where(User.username == host_username)
    result = await session.execute(stmt)
    host = result.scalar_one_or_none()
    if host is None:
        raise HostNotFoundError()

    stmt = select(Calendar).where(Calendar.host_id == host.id)
    result = await session.execute(stmt)
    calendar = result.scalar_one_or_none()
    if calendar is None:
        raise CalendarNotFoundError()
    if user is not None and user.id == host.id:
        return CalendarDetailOut.model_validate(calendar)
    
    return CalendarOut.model_validate(calendar)


@router.post(
    "/calendar",
    status_code=status.HTTP_201_CREATED,
    response_model=CalendarDetailOut,
)
async def create_calendar(
    user: CurrentUserDep,
    session: DbSessionDep,
    payload: CalendarCreateIn
) -> CalendarDetailOut:
    if not user.is_host:
        raise GuestPermissionError()
    calendar = Calendar(
        host_id=user.id,
        topics=payload.topics,
        description=payload.description,
        google_calendar_id=payload.google_calendar_id,
    )
    session.add(calendar)
    try:
        await session.commit()
    except IntegrityError as exc:
        raise CalendarAlreadyExistsError() from exc
    return calendar


@router.patch(
    "/calendar",
    status_code=status.HTTP_200_OK,
    response_model=CalendarDetailOut,
)
async def update_calendar(
    user: CurrentUserDep,
    session: DbSessionDep,
    payload: CalendarUpdateIn
) -> CalendarDetailOut:
    if not user.is_host:
        raise GuestPermissionError()
    
    if user.calendar is None:
        raise CalendarNotFoundError()
    
    if payload.topics is not None:
        user.calendar.topics = payload.topics

    if payload.description is not None:
        user.calendar.description = payload.description

    if payload.google_calendar_id is not None:
        user.calendar.google_calendar_id = payload.google_calendar_id

    await session.commit()

    return user.calendar
