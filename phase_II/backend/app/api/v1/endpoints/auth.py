from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta
import uuid
from ....models.user import User
from ....api.deps import get_session, get_current_user_safe
from ....core.security import create_access_token
from ....core.config import settings
from ....utils.exceptions import AuthException
from passlib.context import CryptContext
import logging

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

class ApiResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str

class LogoutResponse(BaseModel):
    success: bool
    message: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str

# router = APIRouter()
router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password (bcrypt max 72 chars)."""
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password: str) -> str:
    """Generate hash for a password."""
    return pwd_context.hash(password[:72])

@router.post("/login", response_model=ApiResponse)
async def login(
    request: LoginRequest = Body(...),
    session: AsyncSession = Depends(get_session)
):
    """Authenticate user and return access token."""
    try:
        # Find user by email
        result = await session.execute(
            select(User).where(User.email == request.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(request.password, user.hashed_password):
            raise AuthException(
                code="AUTH_INVALID_CREDENTIALS",
                message="Incorrect email or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id},
            expires_delta=access_token_expires
        )

        # For simplicity, we'll use the same token as refresh token in this implementation
        # In production, you'd want to use a separate refresh token system
        refresh_token = create_access_token(
            data={"user_id": user.id, "type": "refresh"},
            expires_delta=timedelta(days=30)  # Refresh token valid for 30 days
        )

        return {
            "success": True,
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                },
                "accessToken": access_token,
                "refreshToken": refresh_token
            },
            "message": "Login successful"
        }

    except AuthException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.post("/register", response_model=ApiResponse)
async def register(
    request: RegisterRequest = Body(...),
    session: AsyncSession = Depends(get_session)
):
    """Register a new user."""
    try:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == request.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(request.password)

        # Create new user
        user = User(
            email=request.email,
            name=request.name,
            hashed_password=hashed_password
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Create access token for the newly registered user
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id},
            expires_delta=access_token_expires
        )

        refresh_token = create_access_token(
            data={"user_id": user.id, "type": "refresh"},
            expires_delta=timedelta(days=30)
        )

        return {
            "success": True,
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                },
                "accessToken": access_token,
                "refreshToken": refresh_token
            },
            "message": "Registration successful"
        }

    except HTTPException:
        raise
    except Exception as e:
            await session.rollback()
            logger.exception("Registration failed")
            raise HTTPException(500, "An error occurred during registration")

@router.post("/logout", response_model=ApiResponse)
async def logout():
    """Logout user (client-side token removal is sufficient)."""
    return {
        "success": True,
        "data": None,
        "message": "Logged out successfully"
    }


@router.get("/me", response_model=ApiResponse)
async def get_current_user_profile(
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    """Get current user's profile information."""
    try:
        # Fetch user by ID from the token
        result = await session.execute(
            select(User).where(User.id == current_user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "success": True,
            "data": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "message": "User profile retrieved successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user profile error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user profile"
        )