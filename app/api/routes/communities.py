from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.community import CommunityCreate, CommunityResponse
from app.schemas.post import PostResponse
from app.services.community import create_community, get_all_communities, get_community_by_slug
from app.services.post import get_posts_by_community
from app.core.dependencies import get_current_user, get_optional_user
from app.models.user import User

router = APIRouter(prefix="/api/communities", tags=["Communities"])

@router.post("", response_model=CommunityResponse, status_code=201)
def create(
    data: CommunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_community(db, data, current_user)

@router.get("", response_model=List[CommunityResponse])
def list_communities(db: Session = Depends(get_db)):
    return get_all_communities(db)

@router.get("/{slug}", response_model=CommunityResponse)
def get_community(slug: str, db: Session = Depends(get_db)):
    return get_community_by_slug(db, slug)

@router.get("/{slug}/posts", response_model=List[PostResponse])
def get_community_posts(
    slug: str,
    sort: str = Query("new", enum=["new", "top"]),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    return get_posts_by_community(db, slug, sort, current_user)