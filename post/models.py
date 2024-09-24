from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from database import Base

#Many to many relationship between posts and hashtags
post_hashtags = Table(
    "post_hashtags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id")),
)

#Many to many relationship between users and the posts they like
post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("post_id", Integer, ForeignKey("posts.id")),
)

#Post Class
class Post(Base):
    __tablename__ = "posts"

    #Basic Post Details
    id = Column(Integer, primary_key= True, index=True)
    content = Column(String)
    image = Column(String)
    location = Column(String)
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    likes_count = Column(Integer, default=0)
    #Foreign key with User
    author_id = Column(Integer, ForeignKey("users.id"))

    #Many-to-many relationships
    author = relationship("auth.models.User", back_populates="posts")
    hashtags = relationship("Hashtag", secondary=post_hashtags, back_populates= "posts")

    liked_by_users = relationship("auth.models.User", secondary=post_likes, back_populates="liked_posts")

#Hashtag Class
class Hashtag(Base):
    __tablename__ = "hashtags"

    #Basic Hashtag Details
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    #Many-to-many relationship
    posts = relationship("Post", secondary=post_hashtags, back_populates="hashtags")