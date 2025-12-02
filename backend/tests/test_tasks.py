"""Tests for task endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User


class TestGetTasks:
    """Tests for listing tasks."""
    
    def test_get_tasks_success(
        self, client: TestClient, auth_headers: dict, test_task: Task
    ):
        """Test getting tasks list."""
        response = client.get("/tasks", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == test_task.title
    
    def test_get_tasks_unauthorized(self, client: TestClient):
        """Test getting tasks without auth fails."""
        response = client.get("/tasks")
        
        assert response.status_code == 403
    
    def test_get_tasks_with_status_filter(
        self, client: TestClient, auth_headers: dict, test_task: Task
    ):
        """Test filtering tasks by status."""
        response = client.get(
            "/tasks?status=todo",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        
        # Filter by different status
        response = client.get(
            "/tasks?status=done",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0
    
    def test_get_tasks_with_search(
        self, client: TestClient, auth_headers: dict, test_task: Task
    ):
        """Test searching tasks."""
        response = client.get(
            "/tasks?search=Test",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        
        # Search with no match
        response = client.get(
            "/tasks?search=NonExistent",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0
    
    def test_get_tasks_pagination(
        self, client: TestClient, auth_headers: dict, db: Session, test_user: User
    ):
        """Test tasks pagination."""
        # Create 15 tasks
        for i in range(15):
            task = Task(
                title=f"Task {i}",
                status=TaskStatus.TODO,
                priority=TaskPriority.MEDIUM,
                owner_id=test_user.id
            )
            db.add(task)
        db.commit()
        
        # Get first page
        response = client.get(
            "/tasks?page=1&page_size=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["total_pages"] == 2
        
        # Get second page
        response = client.get(
            "/tasks?page=2&page_size=10",
            headers=auth_headers
        )
        
        data = response.json()
        assert len(data["items"]) == 5


class TestCreateTask:
    """Tests for creating tasks."""
    
    def test_create_task_success(self, client: TestClient, auth_headers: dict):
        """Test creating a task."""
        response = client.post(
            "/tasks",
            headers=auth_headers,
            json={
                "title": "New Task",
                "description": "Task description",
                "status": "todo",
                "priority": "high"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["status"] == "todo"
        assert data["priority"] == "high"
    
    def test_create_task_minimal(self, client: TestClient, auth_headers: dict):
        """Test creating a task with minimal data."""
        response = client.post(
            "/tasks",
            headers=auth_headers,
            json={"title": "Minimal Task"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["status"] == "todo"  # Default
        assert data["priority"] == "medium"  # Default
    
    def test_create_task_empty_title(self, client: TestClient, auth_headers: dict):
        """Test creating a task with empty title fails."""
        response = client.post(
            "/tasks",
            headers=auth_headers,
            json={"title": ""}
        )
        
        assert response.status_code == 422


class TestUpdateTask:
    """Tests for updating tasks."""
    
    def test_update_task_success(
        self, client: TestClient, auth_headers: dict, test_task: Task
    ):
        """Test updating a task."""
        response = client.put(
            f"/tasks/{test_task.id}",
            headers=auth_headers,
            json={
                "title": "Updated Title",
                "status": "in_progress"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "in_progress"
    
    def test_update_task_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent task fails."""
        response = client.put(
            "/tasks/99999",
            headers=auth_headers,
            json={"title": "Updated"}
        )
        
        assert response.status_code == 404
    
    def test_update_task_partial(
        self, client: TestClient, auth_headers: dict, test_task: Task
    ):
        """Test partial update preserves other fields."""
        original_description = test_task.description
        
        response = client.put(
            f"/tasks/{test_task.id}",
            headers=auth_headers,
            json={"priority": "high"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["priority"] == "high"
        assert data["description"] == original_description


class TestDeleteTask:
    """Tests for deleting tasks."""
    
    def test_delete_task_success(
        self, client: TestClient, auth_headers: dict, test_task: Task
    ):
        """Test deleting a task."""
        response = client.delete(
            f"/tasks/{test_task.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify task is deleted
        response = client.get(
            f"/tasks/{test_task.id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_delete_task_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent task fails."""
        response = client.delete(
            "/tasks/99999",
            headers=auth_headers
        )
        
        assert response.status_code == 404

