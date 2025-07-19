from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database_old import SessionLocal
from db.models import post_model, comment_model, reply_model, user_model
from schemas import post_schemas, comment_schemas, reply_schemas
from datetime import datetime
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def post_to_response(post: post_model.Post) -> post_schemas.PostResponse:
    return post_schemas.PostResponse(
        id=post.id,
        author=post.author.username,  # 利用 SQLAlchemy relationship
        content=post.content,
        category=post.category,
        timestamp=post.created_at
    )

@router.get("/posts/{post_id}/comments", response_model=List[comment_schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(comment_model.Comment).filter_by(post_id=post_id).order_by(comment_model.Comment.created_at).all()
    result = []
    for c in comments:
        replies = db.query(reply_model.Reply).filter_by(comment_id=c.id).all()
        result.append(comment_schemas.CommentResponse(
            id=c.id,
            author=c.author.username,
            content=c.content,
            likes=c.likes,
            timestamp=c.created_at,
            replies=[r.content for r in replies]
        ))
    return result

@router.post("/comments", response_model=comment_schemas.CommentResponse)
def add_comment(comment: comment_schemas.CommentCreate, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter_by(id=comment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_comment = comment_model.Comment(
        post_id=comment.post_id,
        user_id=comment.user_id,
        content=comment.content,
        created_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return comment_schemas.CommentResponse(
        id=new_comment.id,
        author=user.username,
        content=new_comment.content,
        likes=new_comment.likes,
        timestamp=new_comment.created_at,
        replies=[]
    )

@router.post("/replies")
def add_reply(reply: reply_schemas.ReplyCreate, db: Session = Depends(get_db)):
    new_reply = reply_model.Reply(
        comment_id=reply.comment_id,
        user_id=reply.user_id,
        content=reply.content,
        created_at=datetime.utcnow()
    )
    db.add(new_reply)
    db.commit()
    return {"message": "Reply added"}