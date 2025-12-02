"""Task CRUD endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.task import TaskStatus, TaskPriority
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services.task_service import TaskService

router = APIRouter()


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Get all tasks for current user"
)
def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskListResponse:
    """
    Get paginated list of tasks for the authenticated user.
    
    Supports filtering by:
    - **status**: todo, in_progress, done
    - **priority**: low, medium, high
    - **search**: Text search in title and description
    """
    task_service = TaskService(db)
    tasks, total = task_service.get_tasks(
        user_id=current_user.id,
        status=status,
        priority=priority,
        search=search,
        page=page,
        page_size=page_size
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.
    
    - **title**: Task title (required)
    - **description**: Optional description
    - **status**: Task status (default: todo)
    - **priority**: Task priority (default: medium)
    - **due_date**: Optional due date
    """
    task_service = TaskService(db)
    task = task_service.create(task_data, current_user.id)
    return task


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    """Get a specific task by ID."""
    task_service = TaskService(db)
    task = task_service.get_user_task(task_id, current_user.id)
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task"
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    """
    Update an existing task.
    
    Only provided fields will be updated.
    """
    task_service = TaskService(db)
    task = task_service.update(task_id, task_data, current_user.id)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """Delete a task by ID."""
    task_service = TaskService(db)
    task_service.delete(task_id, current_user.id)

