from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone


class ListType(str, Enum):
    white_list = "white_list"
    black_list = "black_list"


class Site(BaseModel):
    site_url: str
    comment: str = None
    created: datetime = datetime.now(timezone.utc)


class BlockList(BaseModel):
    name: str
    comment: str = None
    type: ListType
    created: datetime = datetime.now(timezone.utc)
    sites: List[Site] = []


class SiteResponse(BaseModel):
    id: str
    site_url: str
    comment: str = None
    created: datetime
    updated: Optional[datetime] = None


class BlockListResponse(BaseModel):
    id: str
    name: str
    owner: str
    type: ListType
    comment: str = None
    sites: List[SiteResponse] = []
    created: datetime
    updated: Optional[datetime] = None
