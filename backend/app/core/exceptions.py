"""Custom exceptions for the application."""

from typing import Any, Optional

from fastapi import HTTPException, status


class TaskFlowException(HTTPException):
    """Base exception for TaskFlow application."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(TaskFlowException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found"
        )


class UnauthorizedException(TaskFlowException):
    """Exception raised when authentication fails."""
    
    def __init__(self, detail: str = "Could not validate credentials") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(TaskFlowException):
    """Exception raised when access is forbidden."""
    
    def __init__(self, detail: str = "Not enough permissions") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class BadRequestException(TaskFlowException):
    """Exception raised for bad requests."""
    
    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ConflictException(TaskFlowException):
    """Exception raised when there's a conflict."""
    
    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

