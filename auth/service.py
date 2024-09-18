#User Authentication and Business Logic
from fastapi import Depends
from sqlalchemy.orm import Session

from typing import Final
from dotenv import load_dotenv
import os

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone

from .models import User
from .schemas import UserCreate, UserUpdate

#Password Hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # hasing password
#OAuth Authentication Flow
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

#Load the environment
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRE_MINS = os.getenv('TOKEN_EXPIRE_MINS')

#Check for existing user
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter(User.username == username).first()
    #Checks if the user exists by its username
    if db_user:
        return db_user
    #Checks if the user exists by its email
    db_user = db.query(User).filter(User.email == email).first()
    return db_user

#Create JWT access token
async def create_access_token(username: str, id: int):
    #Payload
    encode = {"sub": username, "id": id}
    #Set expiration time
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINS)
    #Adds expiration time to the payload
    encode.update({"exp": expires})
    #Returns the JWT token
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#Get current user based on JWT access token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        #Decodes token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #Retrieves the data from the payload
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")
        #Check for token expiration
        if datetime.fromtimestamp(expires) < datetime.now(timezone.utc):
            return None
        #Check for payload data
        if username is None or id is None:
            return None
        #Retrieve the user
        return db.query(User).filter(User.id == id).first()
    #Catches user related errors
    except JWTError:
        return None
    
# Retrieve user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

#Create User
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email.lower().strip(),
        username=user.username.lower().strip(),
        hashed_password=bcrypt_context.hash(user.password),
        dob=user.dob or None,
        gender=user.gender or None,
        bio=user.bio or None,
        location=user.location or None,
        profile_pic=user.profile_pic or None,
        name=user.name or None
    )
    #Add information to database
    db.add(db_user)
    #Commit the changes
    db.commit()

    return db_user

#User Authentication
async def authenticate(db: Session, username: str, password: str):
    #Check for user
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        print("No User Found")
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    #Return true
    return db_user

#Update User
async def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.bio = user_update.bio or db_user.bio
    db_user.name = user_update.name or db_user.bio
    db_user.dob = user_update.dob or db_user.bio
    db_user.gender = user_update.gender or db_user.bio
    db_user.location = user_update.location or db_user.bio
    db_user.profile_pic = user_update.profile_pic or db_user.bio

    db.commit()