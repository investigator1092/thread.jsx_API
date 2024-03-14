from dotenv import load_dotenv
load_dotenv() # 環境変数をインポート

from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Union
from my_fastapi_project.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

from my_fastapi_project import models, schemas, crud
from my_fastapi_project.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://thread-jsx-c8bbfb530f22.herokuapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/posts/{post_id}/replies', response_model=schemas.Reply)
def create_reply(post_id: int, reply: schemas.ReplyCreate, db: Session = Depends(get_db), user_id: Union[int, None] = None):
    return crud.create_reply(db=db, post_id=post_id, user_id=user_id, reply=reply)

@app.get('/posts/{post_id}/replies', response_model=List[schemas.Reply])
def read_replies(post_id: int, db: Session = Depends(get_db)):
    replies = crud.get_replies(db, post_id=post_id)
    if replies is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return replies


@app.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@app.get("/posts", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/token")
def login_for_accwss_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )