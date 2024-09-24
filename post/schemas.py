#Database Schema
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#Hashtag model
class Hashtag(BaseModel):
    id: int
    name: str

#Post created by the user
class PostCreate(BaseModel):
    content: Optional[str] = None
    image: str
    location: Optional[str] = None

#Post details
class Post(PostCreate):
    id: int
    author_id: int
    likes_count: int
    created_date: datetime

    class Config:
        orm_mode = True
