#Database Schema
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from .enums import Gender

#Data provided by user
class UserBase(BaseModel):
    email: str
    username: str

#Data created by user
class UserCreate(UserBase):
    password: str

#Data Provided by user that can be updated
class UserUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    bio: Optional[Gender] = None
    location: Optional[str] = None
    profile_pic: Optional[str] = None

#Database object can create this pydantic model
class User(UserBase, UserUpdate):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True