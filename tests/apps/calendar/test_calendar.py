from math import exp
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from appserver.apps.account.models import User
from appserver.apps.calendar.models import Calendar
from appserver.apps.calendar.schemas import CalendarDetailOut, CalendarOut
from appserver.apps.calendar.endpoints import host_calendar_detail
from appserver.apps.calendar.exceptions import HostNotFoundError, CalendarNotFoundError


@pytest.mark.parametrize("user_key, expected_type", [
    ("host_user", CalendarDetailOut),
    ("guest_user", CalendarOut),
    (None, CalendarOut),
])

async def test_get_calendar_info_from_host_user(
        user_key: str | None,
        expected_type: type[CalendarOut | CalendarDetailOut],
        host_user: User,
        host_user_calendar: Calendar,
        guest_user: User,
        db_session: AsyncSession,
):
    users = {
        "host_user": host_user,
        "guest_user": guest_user,
        None: None,
    }
    user = users[user_key]

    result = await host_calendar_detail(host_user.username, user, db_session)

    assert isinstance(result, expected_type)
    result_keys = frozenset(result.model_dump().keys())
    expected_keys = frozenset(expected_type.model_fields.keys())
    assert result_keys == expected_keys

    assert result.topics == host_user_calendar.topics
    assert result.description == host_user_calendar.description
    if isinstance(result, CalendarDetailOut):
        assert result.google_calendar_id == host_user_calendar.google_calendar_id


async def test_raise_host_not_found_error_for_nonexistent_user(
        db_session: AsyncSession,
) -> None:
    with pytest.raises(HostNotFoundError):
        await host_calendar_detail("not_exist_user", None, db_session)


async def test_raise_calendar_not_found_error_for_not_host_user(
        guest_user: User,
        db_session: AsyncSession,
) -> None:
    with pytest.raises(CalendarNotFoundError):
        await host_calendar_detail(guest_user.username, None, db_session)
        