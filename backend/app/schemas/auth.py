"""Authentication-related Pydantic schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for decoded JWT token payload."""
    
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request."""
    
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Schema for token refresh request."""
    
    refresh_token: str

