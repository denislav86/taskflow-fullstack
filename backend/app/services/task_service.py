"""Task service for handling task-related business logic."""

from typing import List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Service class for task operations."""
    
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_user_task(self, task_id: int, user_id: int) -> Task:
        """Get a task by ID, ensuring it belongs to the user."""
        task = self.get_by_id(task_id)
        
        if not task:
            raise NotFoundException("Task")
        
        if task.owner_id != user_id:
            raise ForbiddenException("You don't have access to this task")
        
        return task
    
    def get_tasks(
        self,
        user_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Task], int]:
        """Get paginated list of tasks with optional filters."""
        query = self.db.query(Task).filter(Task.owner_id == user_id)
        
        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_filter),
                    Task.description.ilike(search_filter)
                )
            )
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        offset = (page - 1) * page_size
        tasks = (
            query
            .order_by(Task.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        
        return tasks, total
    
    def create(self, task_data: TaskCreate, user_id: int) -> Task:
        """Create a new task."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            due_date=task_data.due_date,
            owner_id=user_id
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def update(self, task_id: int, task_data: TaskUpdate, user_id: int) -> Task:
        """Update an existing task."""
        task = self.get_user_task(task_id, user_id)
        
        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def delete(self, task_id: int, user_id: int) -> None:
        """Delete a task."""
        task = self.get_user_task(task_id, user_id)
        
        self.db.delete(task)
        self.db.commit()

