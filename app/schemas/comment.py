from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str
    post_id: int

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author_username: Optional[str] = None
    author_avatar: Optional[str] = None

    model_config = {"from_attributes": True}
