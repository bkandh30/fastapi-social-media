#Post Logic
from sqlalchemy.orm import Session
import re
from sqlalchemy import desc

from datetime import datetime
from schemas import PostCreate, Post as PostSchema, Hashtag as HashtagSchema
from models import Post, Hashtag, post_hashtags
from auth.models import User
from auth.schemas import User as UserSchema

#Create Hashtag from post
async def create_hashtag_service(db: Session, post: Post):
    regex= r"#\w+"
    matches = re.findall(regex, post.content)

    for match in matches:
        name = matches[1:]

        hashtag = db.query(Hashtag).filter(Hashtag.name == name).first()
        if not hashtag:
            hashtag = Hashtag(name=name)
            db.add(hashtag)
            db.commit()
        post.hashtags.append(hashtag)

#Create post
async def create_post_service(db:Session, post: PostCreate, user_id: int):
    db_post = Post(
        content = post.content,
        image = post.image,
        location = post.location,
        author_id = user_id
    )

    db.add(db_post)
    db.commit()
    return db_post

#Get posts of a single user
async def get_user_posts_service(db: Session, user_id: int) -> list[PostSchema]:
    posts = (
        db.query(Post).filter(Post.author_id == user_id).order_by(desc(Post.created_date)).all()
    )
    return posts

#Get posts from a hashtag
async def get_posts_from_hashtag_service(db: Session, hashtag_name:str):
    hashtag = db.query(Hashtag).filter_by(name=hashtag_name).first()
    if not hashtag:
        return None
    return hashtag.posts

#Get random posts for user feed by returning the latest posts of all users
async def get_random_posts_service(
    db: Session, page: int = 1, limit: int = 10, hashtag: str = None
):
    total_posts = db.query(Post).count()

    offset = (page - 1) * limit
    if offset >= total_posts:
        return []

    posts = db.query(Post, User.username).join(User).order_by(desc(Post.created_dt))

    if hashtag:
        posts = posts.join(post_hashtags).join(Hashtag).filter(Hashtag.name == hashtag)

    posts = posts.offset(offset).limit(limit).all()

    result = []
    for post, username in posts:
        post_dict = post.__dict__
        post_dict["username"] = username
        result.append(post_dict)

    return result

#Get post by post id
async def get_post_from_post_id_service(db:Session, post_id:int) -> PostSchema:
    return db.query(Post).filter(Post.id==post_id).first()

#Delete post service
async def delete_post_service(db:Session, post_id: int):
    post = await get_post_from_post_id_service(db, post_id)
    db.delete(post)
    db.commit()

#Like post
async def like_post_service(db: Session, post_id: int, username: str):
    post = await get_post_from_post_id_service(db, post_id)
    if not post:
        return False, "invalid post_id"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False, "invalid username"

    if user in post.liked_by_users:
        return False, "already liked"

    # increase like count of post
    post.liked_by_users.append(user)
    post.likes_count = len(post.liked_by_users)

    db.commit()
    return True, "done"

#Unlike post
async def unlike_post_service(db: Session, post_id: int, username: str):
    post = await get_post_from_post_id_service(db, post_id)
    if not post:
        return False, "invalid post_id"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False, "invalid username"

    if not user in post.liked_by_users:
        return False, "already not liked"

    post.liked_by_users.remove(user)
    post.likes_count = len(post.liked_by_users)

    db.commit()
    return True, "done"

# Users who liked post
async def liked_users_post_service(db: Session, post_id: int) -> list[UserSchema]:
    post = await get_post_from_post_id_service(db, post_id)
    if not post:
        return []
    liked_users = post.liked_by_users
    return liked_users