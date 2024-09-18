#Data Models
from sqlalchemy import Column, Date, DateTime, Integer, String, Enum, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from database import Base
from .enums import Gender

#User Class
class User(Base):
    __tablename__ = "users"

    #Basic Login details
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    #Profile Details
    dob = Column(Date)
    gender = Column(Enum(Gender))
    profile_pic = Column(String) #Link of user display picture
    bio = Column(String)
    location = Column(String)
