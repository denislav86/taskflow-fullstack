"""User service for handling user-related business logic."""

from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    """Service class for user operations."""
    
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address."""
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if email already exists
        if self.get_by_email(user_data.email):
            raise ConflictException("Email already registered")
        
        # Create user with hashed password
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password."""
        user = self.get_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def is_active(self, user: User) -> bool:
        """Check if a user is active."""
        return user.is_active

