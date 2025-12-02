"""Task-related Pydantic schemas."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base task schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for paginated task list response."""
    
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class TaskFilters(BaseModel):
    """Schema for task filtering parameters."""
    
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    search: Optional[str] = None

