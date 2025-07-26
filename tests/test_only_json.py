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

from elevate.only_json import JsonConfig, JsonInput, OnlyJson


@pytest.mark.asyncio  # type: ignore
async def test_calendar_event(settings: Any) -> None:
    """Test the OnlyJson class with a CalendarEvent schema for listing events."""

    class CalendarEvent(BaseModel):
        """A calendar event with relevant details (name, date, participants)."""

        name: str = Field(..., description="Name of the event in string format.")
        date: str = Field(
            ...,
            description="Date of the event in 'YYYY-MM-DD' or similar string format.",
        )
        participants: list[str] = Field(..., description="List of participants; each participant name is a string.")

    class EventsList(BaseModel):
        """A container for multiple CalendarEvent objects, stored in a list."""

        events: list[CalendarEvent] = Field(..., description="A JSON array of CalendarEvent objects.")

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(content="List 5 important events in the XIX century", schema=EventsList, system_prompt=None)
    events_list = await only_json.parse(input_data)
    assert isinstance(events_list, EventsList)


@pytest.mark.asyncio  # type: ignore
async def test_extraction_of_contact_info(settings: Any) -> None:
    """Test extracting basic contact information from unstructured text."""

    class ContactInfo(BaseModel):
        """Basic contact information with mandatory fields: name, email, phone."""

        name: str = Field(..., description="The contact's full name in string format.")
        email: str = Field(
            ...,
            description="The contact's email address in string format, e.g., 'johndoe@example.com'.",
        )
        phone: str = Field(
            ...,
            description="The contact's phone number in string format, e.g., '555-1234'.",
        )

    text = (
        "Hello, my name is John Doe. You can reach me at johndoe@example.com or call me at 555-1234."
        " I'll be available most weekdays."
    )

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(content=text, schema=ContactInfo, system_prompt=None)
    contact = await only_json.parse(input_data)
    assert isinstance(contact, ContactInfo)
    assert contact.name == "John Doe"


@pytest.mark.asyncio  # type: ignore
async def test_nested_structures(settings: Any) -> None:
    """Test parsing nested objects (Companies with multiple Departments)."""

    class Department(BaseModel):
        """Data about a single department, including its name, manager, and headcount."""

        name: str = Field(..., description="Name of the department in string format.")
        manager: str = Field(..., description="Full name of the manager in string format.")
        headcount: int = Field(..., description="Number of people in the department as an integer.")

    class Company(BaseModel):
        """Represents a single company, including a list of its departments."""

        company_name: str = Field(..., description="Name of the company in string format.")
        departments: list[Department] = Field(..., description="A JSON array of Department objects.")

    text = (
        "Acme Corp has 2 departments. The first is R&D, managed by Alice Johnson with 25 people. "
        "The second is Marketing, managed by Bob Smith with 15 people."
    )

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(content=text, schema=Company, system_prompt=None)
    company = await only_json.parse(input_data)
    assert isinstance(company, Company)
    assert len(company.departments) == 2


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
    input_data = JsonInput(content=text, schema=Employee, system_prompt=None)
    employee = await only_json.parse(input_data)
    assert isinstance(employee, Employee)
    assert employee.name == "Jane Smith"
    assert employee.manager is not None
    assert employee.manager.name == "John Wilson"
    assert employee.manager.manager is None


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
    input_data = JsonInput(content=text, schema=TemperatureReading, system_prompt=None)
    reading = await only_json.parse(input_data)
    assert isinstance(reading, TemperatureReading)
    assert 29 <= reading.temperature_celsius <= 31


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
    input_data = JsonInput(content=text, schema=Product, system_prompt=None)
    product = await only_json.parse(input_data)
    assert isinstance(product, Product)
    assert product.title == "UltraWidget"
    assert product.quantity == 500


@pytest.mark.asyncio  # type: ignore
async def test_data_formats(settings: Any) -> None:
    """Test parsing various data formats such as price in currency and converting them into the correct type (float)."""

    class StoreItem(BaseModel):
        """Represents a store item with a name, price, and available stock."""

        name: str = Field(..., description="Item name in string format.")
        price: float = Field(..., description="Item price as a float (e.g., 5.99).")
        stock: int = Field(..., description="Number of items in stock as an integer.")

    text = "Item: Fancy Pen. Price: $5.99. Stock: 100 units available."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(content=text, schema=StoreItem, system_prompt=None)
    item = await only_json.parse(input_data)
    assert isinstance(item, StoreItem)
    assert item.name == "Fancy Pen"
    assert abs(item.price - 5.99) < 0.001
    assert item.stock == 100


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
    input_data = JsonInput(content=text, schema=Meeting, system_prompt=None)
    meeting = await only_json.parse(input_data)
    assert isinstance(meeting, Meeting)
    assert meeting.start_time.year == 2025
    assert meeting.start_time.month == 3
    assert meeting.start_time.day == 10
    assert meeting.start_time.hour == 14


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
    input_data = JsonInput(content=text, schema=Profile, system_prompt=None)
    profile = await only_json.parse(input_data)
    assert isinstance(profile, Profile)
    assert profile.username == "techguy"
    assert profile.bio == "Loves coding in Python."
    assert profile.website is None


@pytest.mark.asyncio  # type: ignore
async def test_special_characters_and_lists(settings: Any) -> None:
    """Test parsing a list of items that includes special characters or bullets."""

    class GroceryList(BaseModel):
        """A grocery list containing multiple items in a JSON array of strings."""

        items: list[str] = Field(..., description="A list of grocery items; each item is a string.")

    text = "Today's grocery list:\n• Apples\n• 2% Milk\n• Honey\n• Eggs (a dozen)\nEnd of list."

    config = JsonConfig(model=settings.with_model)
    only_json = OnlyJson(config=config)
    input_data = JsonInput(content=text, schema=GroceryList, system_prompt=None)
    grocery_list = await only_json.parse(input_data)
    assert isinstance(grocery_list, GroceryList)
    assert len(grocery_list.items) == 4
    assert "2% Milk" in grocery_list.items
