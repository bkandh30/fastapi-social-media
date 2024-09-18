#API Routes
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from .schemas import UserCreate, UserUpdate, User as UserSchema
from database import get_db
from .service import (
    existing_user,
    create_access_token,
    get_current_user,
    create_user as create_user_service,
    authenticate,
    update_user as update_user_service
)

router = APIRouter(prefix="/auth", tags=["auth"])

#User Signup
@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #Check Existing User
    db_user = await existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or Email already in use"
        )
    #Create user
    db_user = await create_user_service(db, user)
    #Create access token
    access_token = await create_access_token(user.username, db_user.id)

    #Return the information
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

#Login to generate token
@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Authenticate the user
    db_user = await authenticate(db, form_data.username, form_data.password)
    #If the user is not authenticated, raise an exception
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
        )
    #Create Access Token
    access_token = await create_access_token(db_user.username, db_user.id)
    #Return the access token
    return {"access_token": access_token, "token_type": "bearer"}

#Get Current User
@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def current_user(token: str, db: Session = Depends(get_db)):
    #Check if the user exists
    db_user = await get_current_user(db, token)
    #If it doesn't exist, raise an exception
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )
    #Return the user
    return db_user

#Update User
@router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(username: str, token: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    #Check if the user exists
    db_user = await get_current_user(db, token)
    #If the username doesn't match, raise an exception
    if db_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user",
        )
    #Update the user details
    await update_user_service(db, db_user, user_update)