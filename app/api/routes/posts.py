from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.post import PostCreate, PostResponse
from app.services.post import create_post, get_post, get_posts_by_community, get_all_posts
from app.core.dependencies import get_current_user, get_optional_user
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.vote import Vote

router = APIRouter(prefix="/api/posts", tags=["Posts"])

@router.post("", response_model=PostResponse, status_code=201)
def create(data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_post(db, data, current_user)

@router.get("", response_model=List[PostResponse])
def list_all(sort: str = Query("new", enum=["new", "top"]), db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    return get_all_posts(db, sort, current_user)

@router.get("/{post_id}", response_model=PostResponse)
def get_single(post_id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    return get_post(db, post_id, current_user)

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    db.query(Comment).filter(Comment.post_id == post_id).delete()
    db.query(Vote).filter(Vote.post_id == post_id).delete()
    db.delete(post)
    db.commit()
    return None
