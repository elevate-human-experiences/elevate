"""Test the OnlyJson class with a CalendarEvent schema."""

from pydantic import BaseModel
from elevate import OnlyJson


def test_calendar_event() -> None:
    """Test the OnlyJson class with a CalendarEvent schema."""

    class CalendarEvent(BaseModel):
        """A calendar event."""

        name: str
        date: str
        participants: list[str]

    class EventsList(BaseModel):
        """A list of calendar events."""

        events: list[CalendarEvent]

    only_json = OnlyJson(with_model="gpt-4o-mini")
    events_list = only_json.parse(
        content="List 5 important events in the XIX century", schema=EventsList
    )
    assert isinstance(events_list, EventsList)
