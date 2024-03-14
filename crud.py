from typing import Union
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from security import get_password_hash, verify_password
from . import models, schemas

def get_replies(db: Session, post_id: int):
    return db.query(models.Reply).filter(models.Reply.post_id == post_id).order_by(desc(models.Reply.created_at)).all()

def create_reply(db: Session, post_id: int, user_id: Union[int, None], reply: schemas.ReplyCreate):
    db_reply = models.Reply(content=reply.content, post_id=post_id, user_id=user_id)
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Post).order_by(desc(models.Post.created_at)).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(models.User.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user