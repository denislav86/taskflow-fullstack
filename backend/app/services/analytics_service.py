"""Analytics service for generating task statistics."""

from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.analytics import AnalyticsSummary


class AnalyticsService:
    """Service class for analytics operations."""
    
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_summary(self, user_id: int) -> AnalyticsSummary:
        """Get analytics summary for a user's tasks."""
        # Base query for user's tasks
        base_query = self.db.query(Task).filter(Task.owner_id == user_id)
        
        # Total tasks
        total_tasks = base_query.count()
        
        # Tasks by status
        completed_tasks = (
            base_query
            .filter(Task.status == TaskStatus.DONE)
            .count()
        )
        
        pending_tasks = (
            base_query
            .filter(Task.status == TaskStatus.TODO)
            .count()
        )
        
        in_progress_tasks = (
            base_query
            .filter(Task.status == TaskStatus.IN_PROGRESS)
            .count()
        )
        
        # Overdue tasks (not done and past due date)
        now = datetime.utcnow()
        overdue_tasks = (
            base_query
            .filter(
                Task.status != TaskStatus.DONE,
                Task.due_date.isnot(None),
                Task.due_date < now
            )
            .count()
        )
        
        # Completed this week
        week_ago = now - timedelta(days=7)
        completed_this_week = (
            base_query
            .filter(
                Task.status == TaskStatus.DONE,
                Task.updated_at >= week_ago
            )
            .count()
        )
        
        # High priority pending tasks
        high_priority_pending = (
            base_query
            .filter(
                Task.status != TaskStatus.DONE,
                Task.priority == TaskPriority.HIGH
            )
            .count()
        )
        
        # Completion rate
        completion_rate = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        )
        
        return AnalyticsSummary(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            in_progress_tasks=in_progress_tasks,
            overdue_tasks=overdue_tasks,
            completed_this_week=completed_this_week,
            high_priority_pending=high_priority_pending,
            completion_rate=round(completion_rate, 1)
        )

