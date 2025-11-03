from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.settings import settings
from app.models.users import User
from app.schemas.users import UserCreate, UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: timedelta | None = None):
    to_encode = {"sub": subject}
    expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    except JWTError:
        return None


async def insert_user(payload: UserCreate, db: AsyncSession) -> UserOut:
    user = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)
