from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status
from app.models.post import Post
from app.models.community import Community
from app.models.vote import Vote
from app.schemas.post import PostCreate
from app.models.user import User

def enrich_post(post, db, current_user=None):
    data = {
        "id": post.id, "title": post.title, "content": post.content,
        "image_url": post.image_url, "link_url": post.link_url,
        "post_type": post.post_type, "vote_count": post.vote_count,
        "comment_count": post.comment_count, "community_id": post.community_id,
        "author_id": post.author_id, "created_at": post.created_at,
        "updated_at": post.updated_at,
        "author_username": post.author.username if post.author else None,
        "community_name": post.community.name if post.community else None,
        "community_slug": post.community.slug if post.community else None,
        "user_vote": None
    }
    if current_user:
        vote = db.query(Vote).filter(Vote.post_id == post.id, Vote.user_id == current_user.id).first()
        data["user_vote"] = vote.type if vote else None
    return data

def create_post(db, data, author):
    community = db.query(Community).filter(Community.slug == data.community_slug).first()
    if not community:
        raise HTTPException(status_code=404, detail=f"Community r/{data.community_slug} not found")
    post = Post(title=data.title, content=data.content, image_url=data.image_url,
                link_url=data.link_url, post_type=data.post_type,
                community_id=community.id, author_id=author.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return enrich_post(post, db, author)

def get_post(db, post_id, current_user=None):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return enrich_post(post, db, current_user)

def get_posts_by_community(db, slug, sort="new", current_user=None):
    community = db.query(Community).filter(Community.slug == slug).first()
    if not community:
        raise HTTPException(status_code=404, detail=f"Community r/{slug} not found")
    query = db.query(Post).filter(Post.community_id == community.id)
    query = query.order_by(desc(Post.vote_count) if sort == "top" else desc(Post.created_at))
    return [enrich_post(p, db, current_user) for p in query.all()]

def get_all_posts(db, sort="new", current_user=None):
    query = db.query(Post)
    query = query.order_by(desc(Post.vote_count) if sort == "top" else desc(Post.created_at))
    return [enrich_post(p, db, current_user) for p in query.all()]
