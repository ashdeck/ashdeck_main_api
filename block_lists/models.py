from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone


class ListType(str, Enum):
    white_list = "white_list"
    black_list = "black_list"


class Site(BaseModel):
    site_url: str
    # comment: str = None
    created: datetime = datetime.now(timezone.utc)


class UpdateBlockList(BaseModel):
    name: str = None
    entries: List[Site] = None
    updated_at: datetime = datetime.now(timezone.utc)


class BlockList(BaseModel):
    name: str
    # comment: str = None
    type: ListType = Field(default="black_list")
    created: datetime = datetime.now(timezone.utc)
    entries: List[Site]


class SiteResponse(BaseModel):
    id: str
    site_url: str
    # comment: str = None
    created: datetime = None
    updated: Optional[datetime] = None


class BlockListResponse(BaseModel):
    id: str
    name: str
    owner: str
    type: ListType
    # comment: str = None
    entries: List[SiteResponse] = []
    created: datetime
    updated: Optional[datetime] = None
