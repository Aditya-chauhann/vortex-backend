from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import re

class CommunityCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Community name must be at least 3 characters")
        if len(v) > 21:
            raise ValueError("Community name must be under 21 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Only letters, numbers and underscores allowed")
        return v

class CommunityResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    banner_url: Optional[str] = None
    icon_url: Optional[str] = None
    owner_id: int
    created_at: datetime
    post_count: Optional[int] = 0

    model_config = {"from_attributes": True}