from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.post import PostType

class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    post_type: PostType = PostType.text
    community_slug: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    post_type: str
    vote_count: int
    comment_count: int
    community_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    author_username: Optional[str] = None
    community_name: Optional[str] = None
    community_slug: Optional[str] = None
    user_vote: Optional[str] = None

    model_config = {"from_attributes": True}