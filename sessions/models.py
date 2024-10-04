from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class SessionType(str, Enum):
    start_now = "start_now"
    start_later = "start_later"
    recurring = "recurring"


class RecurringDays(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class WeekDays(BaseModel):
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
    saturday: bool = False
    sunday: bool = False


class Session(BaseModel):
    device_id: str = None
    name: str = "New Session"
    type: SessionType
    start_time: datetime = None
    end_time: datetime = None
    block_lists: list[str]
    start_date: str = None
    notes: str = None
    paused: bool = False
    recurring_days: list[RecurringDays] = None
