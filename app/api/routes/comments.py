from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment import create_comment, get_comments
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post

router = APIRouter(prefix="/api/comments", tags=["Comments"])

@router.post("", response_model=CommentResponse, status_code=201)
def add_comment(data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_comment(db, data, current_user)

@router.get("/post/{post_id}", response_model=List[CommentResponse])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return get_comments(db, post_id)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your comment")
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if post:
        post.comment_count = max(0, post.comment_count - 1)
    db.delete(comment)
    db.commit()
    return None
