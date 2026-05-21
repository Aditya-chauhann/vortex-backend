from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.comment import Comment
from app.models.post import Post

def enrich_comment(comment):
    return {
        "id": comment.id,
        "content": comment.content,
        "post_id": comment.post_id,
        "author_id": comment.author_id,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "author_username": comment.author.username if comment.author else None,
        "author_avatar": comment.author.avatar_url if comment.author else None,
    }

def create_comment(db, data, author):
    post = db.query(Post).filter(Post.id == data.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(content=data.content, post_id=data.post_id, author_id=author.id)
    db.add(comment)
    post.comment_count += 1
    db.commit()
    db.refresh(comment)
    return enrich_comment(comment)

def get_comments(db, post_id):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at.asc()).all()
    return [enrich_comment(c) for c in comments]
