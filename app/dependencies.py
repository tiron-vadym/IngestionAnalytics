from typing import AsyncGenerator

from jose import jwt, JWTError
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.constants import ALGORITHM
from app.db import AsyncSessionLocal
from app.settings import settings

security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def verify_jwt(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(HTTP_401_UNAUTHORIZED, "Invalid token")
    return payload
