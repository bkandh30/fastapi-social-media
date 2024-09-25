from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from .schemas import Profile, FollowersList, FollowingList
from .service import (
    get_followers_service,
    get_following_service,
    follow_service,
    unfollow_service,
    check_follow_service,
    existing_user
)

from auth.service import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

#Get User Profile Route
@router.get("/user/{username}", response_model=Profile)
async def profile(username: str, db: Session = Depends(get_db)):
    db_user = await existing_user(db, username, "")
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username"
        )
    
    return db_user

#Follow User Route
@router.post("/follow/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def follow(username:str, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(db, token)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid token"
        )
    
    res = await follow_service(db, db_user.username, username)
    if res == False:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT, detail="could not follow"
        )

#Unfollow User Route
@router.post("/unfollow/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def follow(username: str, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(db,token)
    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail="invalid token"
        )
    
    res = await unfollow_service(db, db_user.username, username)
    if res == False:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT, detail="could not follow"
        )

#Get Followers Route
@router.get("/followers", response_model = FollowersList)
async def get_followers(token: str, db: Session = Depends(get_db)):
    current_user = await get_current_user(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return await get_followers_service(db, current_user.id)

#Get Following Route
@router.get("/following", response_model = FollowingList)
async def get_following(token: str, db: Session = Depends(get_db)):
    current_user = await get_current_user(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return await get_following_service(db, current_user.id)