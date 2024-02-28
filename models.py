from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Post

app = FastAPI()

# 依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/posts/")
def create_post(title: str, content: str, db: Session = Depends(get_db)):
    db_post = Post(title=title, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
