from pydantic import BaseModel
from enum import Enum
from datetime import datetime, timezone


class WeekDays(BaseModel):
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
    saturday: bool = False
    sunday: bool = False


class Session(BaseModel):
    name: str
    block_lists: list


class ScheduledSession(Session):
    start: datetime
    end: datetime


class RecurringSession(Session):
    start: datetime
    end: datetime
    days: WeekDays
