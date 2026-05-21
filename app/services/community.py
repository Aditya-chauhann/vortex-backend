from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.community import Community
from app.models.post import Post
from app.schemas.community import CommunityCreate
from app.models.user import User

def create_community(db: Session, data: CommunityCreate, owner: User) -> Community:
    slug = data.name.lower()

    if db.query(Community).filter(Community.slug == slug).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Community r/{data.name} already exists"
        )

    community = Community(
        name=data.name,
        slug=slug,
        description=data.description,
        owner_id=owner.id
    )
    db.add(community)
    db.commit()
    db.refresh(community)
    return community

def get_all_communities(db: Session) -> list:
    communities = db.query(Community).order_by(Community.created_at.desc()).all()
    result = []
    for c in communities:
        post_count = db.query(Post).filter(Post.community_id == c.id).count()
        c.post_count = post_count
        result.append(c)
    return result

def get_community_by_slug(db: Session, slug: str) -> Community:
    community = db.query(Community).filter(Community.slug == slug).first()
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Community r/{slug} not found"
        )
    post_count = db.query(Post).filter(Post.community_id == community.id).count()
    community.post_count = post_count
    return community