"""Tests for analytics endpoints."""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User


class TestAnalyticsSummary:
    """Tests for analytics summary endpoint."""
    
    def test_get_summary_empty(self, client: TestClient, auth_headers: dict):
        """Test analytics with no tasks."""
        response = client.get("/analytics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 0
        assert data["completed_tasks"] == 0
        assert data["completion_rate"] == 0.0
    
    def test_get_summary_with_tasks(
        self, client: TestClient, auth_headers: dict, db: Session, test_user: User
    ):
        """Test analytics with various tasks."""
        now = datetime.utcnow()
        
        # Create tasks with different statuses
        tasks = [
            Task(
                title="Done Task 1",
                status=TaskStatus.DONE,
                priority=TaskPriority.HIGH,
                owner_id=test_user.id,
                updated_at=now - timedelta(days=2)  # Completed this week
            ),
            Task(
                title="Done Task 2",
                status=TaskStatus.DONE,
                priority=TaskPriority.MEDIUM,
                owner_id=test_user.id,
                updated_at=now - timedelta(days=10)  # Not this week
            ),
            Task(
                title="In Progress Task",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.MEDIUM,
                owner_id=test_user.id
            ),
            Task(
                title="Todo Task",
                status=TaskStatus.TODO,
                priority=TaskPriority.LOW,
                owner_id=test_user.id
            ),
            Task(
                title="Overdue Task",
                status=TaskStatus.TODO,
                priority=TaskPriority.HIGH,
                due_date=now - timedelta(days=1),  # Overdue
                owner_id=test_user.id
            )
        ]
        
        for task in tasks:
            db.add(task)
        db.commit()
        
        response = client.get("/analytics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 5
        assert data["completed_tasks"] == 2
        assert data["pending_tasks"] == 2  # TODO tasks
        assert data["in_progress_tasks"] == 1
        assert data["overdue_tasks"] == 1
        assert data["high_priority_pending"] == 1  # Overdue high priority task
        assert data["completion_rate"] == 40.0  # 2/5 * 100
    
    def test_get_summary_unauthorized(self, client: TestClient):
        """Test analytics without auth fails."""
        response = client.get("/analytics/summary")
        
        assert response.status_code == 403

