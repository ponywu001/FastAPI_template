from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import models
from src.dependencies.auth import get_current_user, authenticate_user
from src.dependencies.basic import get_db

from src.schemas import basic
from src.schemas.basic import Token
from src.utils.credentials import create_access_token

from fastapi import HTTPException, status
from src.utils.credentials import hash_password


# -------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas.basic import UserCreate
from src.utils.credentials import hash_password
from src.dependencies.basic import get_db
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------- #

router = APIRouter()

@router.get('/me')
async def me(
        user: models.User = Depends(get_current_user)
):
    return user.__dict__

@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token({"sub": user.account[0].username})

    return Token(access_token=token, token_type="bearer")


# -------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
@router.post("/user_register")
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    # 檢查用戶名是否已經存在
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 創建新用戶
    hashed_password = hash_password(user_create.password)
    new_user = User(
        username=user_create.username,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------- #