from enum import Enum
from typing import Optional

from pydantic import BaseModel

class SourceType(Enum):
    WEBSITE = 'website'
    PDF = 'pdf'

class Source(BaseModel):
    url: str
    page: int
    src_type: SourceType

class WrappedFloat(BaseModel):
    value: float
    source: Source 

class ScrapeResult(BaseModel):
    scope_1: Optional[WrappedFloat] = None
    scope_2: Optional[WrappedFloat] = None
    scope_3: Optional[WrappedFloat] = None

class EmissionsData(BaseModel):
    scope_1: Optional[float]
    scope_2: Optional[float]
    scope_3: Optional[float]