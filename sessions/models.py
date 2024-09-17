from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from datetime import date


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
    type: SessionType
    start_time: datetime = None
    end_time: datetime = None
    block_lists: list[str]
    start_date: date
    recurring_days: list[RecurringDays] = None
