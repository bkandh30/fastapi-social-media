#Data Models
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from database import Base

#Activity Class
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key= True)
    username = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable= False, default=lambda: datetime.now(timezone.utc))

    #Post Liking Activity
    liked_post_id = Column(Integer)
    username_like = Column(String)
    liked_post_id = Column(String)

    #Following Activity
    follower_username = Column(String)
    follower_user_pic = Column(String)