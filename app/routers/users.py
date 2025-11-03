from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.handlers.users import (
    insert_user,
    verify_password,
    create_access_token
)
from app.dependencies import get_db
from app.models.users import User
from app.schemas.users import TokenSchema, UserOut, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/sign_up", response_model=UserOut, status_code=HTTP_201_CREATED)
async def create_user(
        payload: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    user = await insert_user(payload, db)
    return user


@router.post("/token", response_model=TokenSchema, status_code=HTTP_200_OK)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.username == form_data.username))
    user = q.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.username)
    return TokenSchema(access_token=token)
