"""Analytics-related Pydantic schemas."""

from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    """Schema for analytics summary response."""
    
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    overdue_tasks: int
    completed_this_week: int
    high_priority_pending: int
    completion_rate: float

