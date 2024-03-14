import datetime
from pydantic import BaseModel, StringConstraints
from typing import Annotated, Union

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class ReplyBase(BaseModel):
    content: str

class ReplyCreate(ReplyBase):
    content: Annotated[str, StringConstraints(min_length=1)]

class Reply(ReplyBase):
    id: int
    created_at: datetime.datetime
    user_id: Union[int, None]
    post_id: int

    class Config:
        orm_mode = True