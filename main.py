from fastapi import FastAPI
from sqlalchemy import MetaData, create_engine
from models import Post, posts, engine

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/posts/")
async def create_post(post: Post):
    pass

@app.get("/posts/")
async def read_posts():
    pass