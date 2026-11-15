from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import UserCreate,UserResponse,Token
from db.base import get_db_session
from db.models import User
from core.security import SecurityUtil

auth_router = APIRouter(prefix="/api/v1/auth",tags=["Auth"])

@auth_router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register_user(payload:UserCreate,db:AsyncSession = Depends(get_db_session) ):
    query = await db.execute(select(User).where(User.email == payload.email))
    existing_user = query.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    new_user = User(
        email = payload.email,
        hashed_password = SecurityUtil.hash_password(payload.password),
        role = payload.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@auth_router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login_user(payload: UserCreate,db: AsyncSession = Depends(get_db_session)):
    query = await db.execute(select(User).where(User.email == payload.email))
    user = query.scalars().first()

    if user or not SecurityUtil.verify_password(payload.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = SecurityUtil.create_access_token(subject=user.id)
    return {"access_token":token,"token_type":"bearer"}
