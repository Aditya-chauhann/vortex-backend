from pydantic import BaseModel
from app.models.vote import VoteType

class VoteCreate(BaseModel):
    post_id: int
    vote_type: VoteType

class VoteResponse(BaseModel):
    post_id: int
    vote_type: str | None
    vote_count: int
    message: str