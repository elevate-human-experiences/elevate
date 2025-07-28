# MIT License
#
# Copyright (c) 2025 elevate-human-experiences
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test the OnlyJson class with a CalendarEvent schema."""

from datetime import datetime
from typing import Any, Optional

import pytest
from pydantic import BaseModel, ConfigDict, Field

from elevate.only_json import JsonConfig, JsonInput, JsonOutput, OnlyJson


@pytest.mark.asyncio  # type: ignore
async def test_organizing_meeting_notes(settings: Any) -> None:
    """Test organizing messy meeting notes into structured calendar events."""

    class MeetingEvent(BaseModel):
        """A scheduled meeting with key details."""

        title: str = Field(..., description="Meeting title or topic")
        date: str = Field(..., description="Meeting date in YYYY-MM-DD format")
        time: str = Field(..., description="Meeting time")
        attendees: list[str] = Field(..., description="List of attendee names")
        location: str | None = Field(None, description="Meeting location")

    class MeetingSchedule(BaseModel):
        """List of upcoming meetings extracted from notes."""

        meetings: list[MeetingEvent] = Field(..., description="Scheduled meetings")

    messy_notes = """
    Next week looks busy! Monday morning 9:30 standup with the dev team (Sarah, Mike, Alex) in conference room B.
    Then Thursday March 15th at 2pm quarterly review with Jennifer and Tom - think that's remote.
    Oh and Friday 10am coffee chat with Lisa from marketing, probably at the cafe downstairs.
    """

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(
        text=messy_notes,
        purpose="organizing my calendar for next week",
        context="I just got back from vacation and need to make sense of these meeting notes",
        schema=MeetingSchedule,
    )
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, MeetingSchedule)
    assert len(result.data.meetings) >= 2  # Should find at least 2 meetings


@pytest.mark.asyncio  # type: ignore
async def test_extracting_client_contact_from_email(settings: Any) -> None:
    """Test extracting client contact info from a business email for CRM entry."""

    class ClientContact(BaseModel):
        """Contact information for a potential client."""

        name: str = Field(..., description="Full name of the contact person")
        email: str = Field(..., description="Business email address")
        phone: str | None = Field(None, description="Phone number if provided")
        company: str | None = Field(None, description="Company name")
        role: str | None = Field(None, description="Job title or role")

    business_email = """
    Hi there,

    I'm reaching out from Acme Solutions regarding your software development services.
    I'm Maria Rodriguez, the CTO here, and we're looking for a partner for our upcoming project.

    Feel free to call me at (555) 123-4567 or just reply to this email (m.rodriguez@acmesolutions.com).

    Looking forward to hearing from you!

    Best regards,
    Maria Rodriguez
    Chief Technology Officer
    Acme Solutions Inc.
    """

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(
        text=business_email,
        purpose="adding to my CRM system",
        context="This is a potential client inquiry I received today",
        schema=ClientContact,
    )
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, ClientContact)
    assert "maria" in result.data.name.lower()
    assert "rodriguez" in result.data.name.lower()


@pytest.mark.asyncio  # type: ignore
async def test_organizing_team_feedback(settings: Any) -> None:
    """Test organizing employee feedback survey into structured departmental insights."""

    class TeamFeedback(BaseModel):
        """Feedback summary for a specific team."""

        team_name: str = Field(..., description="Name of the team")
        lead: str = Field(..., description="Team lead or manager name")
        satisfaction_score: float | None = Field(None, description="Overall satisfaction rating (1-10)")
        main_concerns: list[str] = Field(default_factory=list, description="Key issues raised by team")
        positive_highlights: list[str] = Field(default_factory=list, description="Things the team is doing well")

    class OrganizationFeedback(BaseModel):
        """Consolidated feedback across all teams."""

        teams: list[TeamFeedback] = Field(..., description="Feedback from each team")

    survey_results = """
    Here's what came back from our Q1 feedback survey:

    Engineering team (led by Sarah Chen) scored 8.2/10 overall. They love the new dev tools but are concerned about
    sprint planning being too aggressive and want better work-life balance. The team appreciated the recent hackathon event.

    Marketing team under David Park gave us 6.8/10. They're frustrated with the approval process taking too long
    and feel understaffed for current campaign load. However, they're excited about the new brand guidelines
    and collaboration with the design team has improved.

    Sales team (Manager: Lisa Wong) rated 7.5/10. Main complaint is the CRM system being slow and outdated.
    They're happy with the new commission structure and feel supported by management.
    """

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(
        text=survey_results,
        purpose="preparing executive summary for leadership team",
        context="Q1 employee satisfaction survey results just came in",
        schema=OrganizationFeedback,
    )
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, OrganizationFeedback)
    assert len(result.data.teams) == 3  # Should identify 3 teams


@pytest.mark.asyncio  # type: ignore
async def test_cyclic_relationships(settings: Any) -> None:
    """Test parsing data where an Employee may reference another Employee as a manager."""

    class Employee(BaseModel):
        """Represents an employee. The manager field references another Employee object (or None)."""

        name: str = Field(..., description="Employee's full name in string format.")
        manager: Optional["Employee"] = Field(
            None,
            description="Reference to another Employee object acting as the manager, or null if none.",
        )
        model_config = ConfigDict(arbitrary_types_allowed=True)

    text = "Employee: Jane Smith. Manager: John Wilson. Manager of John Wilson is none."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(text=text, schema=Employee)
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, Employee)
    assert result.data.name == "Jane Smith"
    assert result.data.manager is not None
    assert result.data.manager.name == "John Wilson"
    assert result.data.manager.manager is None


@pytest.mark.asyncio  # type: ignore
async def test_conversion_while_extracting(settings: Any) -> None:
    """Test converting temperature from Fahrenheit in the text to Celsius in the schema."""

    class TemperatureReading(BaseModel):
        """A temperature reading in Celsius for a specific city, possibly converted from Fahrenheit."""

        city: str = Field(..., description="City name in string format.")
        temperature_celsius: float = Field(
            ...,
            description="Temperature in Celsius (float). Convert from Fahrenheit if needed.",
        )

    text = "The temperature in Berlin is 86 degrees Fahrenheit today."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(text=text, schema=TemperatureReading)
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, TemperatureReading)
    assert 29 <= result.data.temperature_celsius <= 31


@pytest.mark.asyncio  # type: ignore
async def test_different_field_descriptions(settings: Any) -> None:
    """Test fields with custom descriptions and validations for a product."""

    class Product(BaseModel):
        """Product details, including SKU and quantity."""

        title: str = Field(..., description="Name of the product in string format.")
        sku: str = Field(..., description="Stock Keeping Unit in string format (unique identifier).")
        quantity: int = Field(..., description="Number of items in stock as an integer.")

    text = "We have a new product called UltraWidget. SKU: UW-001. We currently have 500 pieces in inventory."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(text=text, schema=Product)
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, Product)
    assert result.data.title == "UltraWidget"
    assert result.data.quantity == 500


@pytest.mark.asyncio  # type: ignore
async def test_expense_tracking_from_receipt(settings: Any) -> None:
    """Test extracting expense data from receipt text for expense reporting."""

    class ExpenseItem(BaseModel):
        """A single expense item from a receipt."""

        description: str = Field(..., description="What was purchased")
        amount: float = Field(..., description="Cost in dollars")
        category: str | None = Field(None, description="Expense category (meals, office supplies, etc.)")

    class Receipt(BaseModel):
        """Expense report data from a business receipt."""

        vendor: str = Field(..., description="Business/vendor name")
        date: str | None = Field(None, description="Date of purchase")
        items: list[ExpenseItem] = Field(..., description="Individual expense items")
        total: float = Field(..., description="Total amount spent")

    receipt_text = """
    OFFICE DEPOT
    Receipt #12345
    Date: March 15, 2024

    2x Notebooks @ $3.49 each = $6.98
    Printer paper (1 ream) = $8.50
    Blue pens (pack of 10) = $12.99
    Coffee for office = $15.75

    Subtotal: $44.22
    Tax: $3.54
    TOTAL: $47.76

    Thank you for shopping with us!
    """

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(
        text=receipt_text,
        purpose="submitting monthly expense report",
        context="Need to categorize this office supply run for accounting",
        schema=Receipt,
    )
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, Receipt)
    assert abs(result.data.total - 47.76) < 0.01
    assert len(result.data.items) >= 3  # Should identify multiple items


@pytest.mark.asyncio  # type: ignore
async def test_datetime_parsing(settings: Any) -> None:
    """Test parsing a datetime field from unstructured text."""

    class Meeting(BaseModel):
        """A meeting that has a topic and a start_time in datetime format."""

        topic: str = Field(..., description="Topic of the meeting in string format.")
        start_time: datetime = Field(..., description="Date/time of the meeting (e.g., '2025-03-10 14:30:00').")

    text = "Meeting about budget planning on March 10, 2025 at 2:30 PM."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(text=text, schema=Meeting)
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, Meeting)
    assert result.data.start_time.year == 2025
    assert result.data.start_time.month == 3
    assert result.data.start_time.day == 10
    assert result.data.start_time.hour == 14


@pytest.mark.asyncio  # type: ignore
async def test_optional_fields(settings: Any) -> None:
    """Test a schema with optional fields, ensuring that missing data is handled gracefully."""

    class Profile(BaseModel):
        """A user profile with a mandatory username and optional bio and website fields."""

        username: str = Field(..., description="Unique username in string format.")
        bio: str | None = Field(
            None,
            description="Short bio in a single sentence (optional). For example: 'Love to hike in the Alps.'",
        )
        website: str | None = Field(None, description="Website URL in string format (optional).")

    text = "Username: techguy. Bio: Loves coding in Python. (No website provided)."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(text=text, schema=Profile)
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, Profile)
    assert result.data.username == "techguy"
    assert result.data.bio == "Loves coding in Python."
    assert result.data.website is None


@pytest.mark.asyncio  # type: ignore
async def test_special_characters_and_lists(settings: Any) -> None:
    """Test parsing a list of items that includes special characters or bullets."""

    class GroceryList(BaseModel):
        """A grocery list containing multiple items in a JSON array of strings."""

        items: list[str] = Field(..., description="A list of grocery items; each item is a string.")

    text = "Today's grocery list:\n• Apples\n• 2% Milk\n• Honey\n• Eggs (a dozen)\nEnd of list."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(text=text, schema=GroceryList)
    result = await only_json.parse(input_data)
    assert isinstance(result, JsonOutput)
    assert isinstance(result.data, GroceryList)
    assert len(result.data.items) == 4
    assert "2% Milk" in result.data.items
