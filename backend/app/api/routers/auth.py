"""Authentication endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import UnauthorizedException, BadRequestException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.schemas.auth import Token, LoginRequest, RefreshRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **password**: Password (min 8 characters)
    - **full_name**: Optional full name
    """
    user_service = UserService(db)
    user = user_service.create(user_data)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login to get access token"
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate user and return JWT tokens.
    
    - **email**: Registered email address
    - **password**: User password
    """
    user_service = UserService(db)
    user = user_service.authenticate(login_data.email, login_data.password)
    
    if not user:
        raise UnauthorizedException("Incorrect email or password")
    
    if not user.is_active:
        raise UnauthorizedException("User account is disabled")
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token"
)
def refresh_token(
    refresh_data: RefreshRequest,
    db: Session = Depends(get_db)
) -> Token:
    """
    Get new access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    payload = decode_token(refresh_data.refresh_token)
    
    if payload is None:
        raise UnauthorizedException("Invalid refresh token")
    
    if payload.get("type") != "refresh":
        raise BadRequestException("Invalid token type")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Invalid token payload")
    
    # Verify user still exists and is active
    user_service = UserService(db)
    user = user_service.get_by_id(int(user_id))
    
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive")
    
    access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token
    )

