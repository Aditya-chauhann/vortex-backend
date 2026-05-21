from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.vote import Vote, VoteType
from app.models.post import Post
from app.models.user import User

def cast_vote(db, post_id, vote_type, user):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing = db.query(Vote).filter(Vote.user_id == user.id, Vote.post_id == post_id).first()
    if existing:
        if existing.type == vote_type:
            post.vote_count += -1 if vote_type == VoteType.up else 1
            db.delete(existing)
            db.commit()
            db.refresh(post)
            return {"post_id": post_id, "vote_type": None, "vote_count": post.vote_count, "message": "Vote removed"}
        else:
            post.vote_count += 2 if vote_type == VoteType.up else -2
            existing.type = vote_type
            db.commit()
            db.refresh(post)
            return {"post_id": post_id, "vote_type": vote_type, "vote_count": post.vote_count, "message": "Vote updated"}
    else:
        vote = Vote(user_id=user.id, post_id=post_id, type=vote_type)
        db.add(vote)
        post.vote_count += 1 if vote_type == VoteType.up else -1
        db.commit()
        db.refresh(post)
        return {"post_id": post_id, "vote_type": vote_type, "vote_count": post.vote_count, "message": "Vote cast"}
