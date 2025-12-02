"""API dependencies for dependency injection."""

from typing import Generator

from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token
from app.models.user import User
from app.services.user_service import UserService

# HTTP Bearer security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token."""
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise UnauthorizedException("Invalid token")
    
    # Check if it's an access token
    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Invalid token payload")
    
    user_service = UserService(db)
    user = user_service.get_by_id(int(user_id))
    
    if user is None:
        raise UnauthorizedException("User not found")
    
    if not user.is_active:
        raise UnauthorizedException("Inactive user")
    
    return user


def get_optional_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User | None:
    """Get the current user if authenticated, otherwise None."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    
    if payload is None or payload.get("type") != "access":
        return None
    
    user_id = payload.get("sub")
    if user_id is None:
        return None
    
    user_service = UserService(db)
    return user_service.get_by_id(int(user_id))

