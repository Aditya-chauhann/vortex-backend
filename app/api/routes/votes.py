from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.vote import VoteCreate, VoteResponse
from app.services.vote import cast_vote
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/votes", tags=["Votes"])

@router.post("", response_model=VoteResponse)
def vote(
    data: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cast_vote(db, data.post_id, data.vote_type, current_user)