"""Analytics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.analytics import AnalyticsSummary
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get(
    "/summary",
    response_model=AnalyticsSummary,
    summary="Get task analytics summary"
)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AnalyticsSummary:
    """
    Get analytics summary for the authenticated user's tasks.
    
    Returns:
    - Total tasks count
    - Tasks by status (completed, pending, in progress)
    - Overdue tasks count
    - Tasks completed this week
    - High priority pending tasks
    - Overall completion rate
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_summary(current_user.id)

