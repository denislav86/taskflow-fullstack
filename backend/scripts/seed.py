"""Seed script to populate database with demo data."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority


def create_demo_users(db):
    """Create demo users."""
    users = [
        {
            "email": "demo@taskflow.dev",
            "password": "demo1234",
            "full_name": "Demo User"
        },
        {
            "email": "admin@taskflow.dev",
            "password": "admin1234",
            "full_name": "Admin User"
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"User {user_data['email']} already exists, skipping...")
            created_users.append(existing)
            continue
        
        user = User(
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            full_name=user_data["full_name"],
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        created_users.append(user)
        print(f"Created user: {user.email}")
    
    return created_users


def create_demo_tasks(db, user):
    """Create demo tasks for a user."""
    now = datetime.utcnow()
    
    tasks = [
        {
            "title": "Complete project documentation",
            "description": "Write comprehensive documentation for the TaskFlow API including setup instructions, API endpoints, and examples.",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": now + timedelta(days=3)
        },
        {
            "title": "Review pull requests",
            "description": "Review and merge pending pull requests from team members.",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": now + timedelta(days=1)
        },
        {
            "title": "Set up CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing and deployment.",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": now - timedelta(days=2)
        },
        {
            "title": "Design database schema",
            "description": "Create ERD and define relationships between entities.",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": now - timedelta(days=5)
        },
        {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication with access and refresh tokens.",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": now - timedelta(days=3)
        },
        {
            "title": "Write unit tests",
            "description": "Create comprehensive test suite for API endpoints.",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.MEDIUM,
            "due_date": now + timedelta(days=5)
        },
        {
            "title": "Optimize database queries",
            "description": "Review and optimize slow database queries. Add indexes where needed.",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": now + timedelta(days=7)
        },
        {
            "title": "Fix login page styling",
            "description": "Adjust CSS for better mobile responsiveness on the login page.",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": now + timedelta(days=4)
        },
        {
            "title": "Prepare sprint demo",
            "description": "Create presentation slides and demo script for upcoming sprint review.",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": now + timedelta(days=2)
        },
        {
            "title": "Update dependencies",
            "description": "Review and update project dependencies to latest stable versions.",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": now + timedelta(days=14)
        },
        {
            "title": "Code review meeting",
            "description": "Schedule and conduct code review session with the team.",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.MEDIUM,
            "due_date": now - timedelta(days=1)
        },
        {
            "title": "Bug: Fix task deletion issue",
            "description": "Investigate and fix the bug where deleted tasks still appear in the list.",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": now - timedelta(days=1)  # Overdue!
        }
    ]
    
    for task_data in tasks:
        task = Task(
            title=task_data["title"],
            description=task_data["description"],
            status=task_data["status"],
            priority=task_data["priority"],
            due_date=task_data["due_date"],
            owner_id=user.id
        )
        db.add(task)
    
    db.commit()
    print(f"Created {len(tasks)} demo tasks for {user.email}")


def main():
    """Main seed function."""
    print("=" * 50)
    print("TaskFlow Database Seeding")
    print("=" * 50)
    
    # Create tables
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create demo users
        print("\nCreating demo users...")
        users = create_demo_users(db)
        
        # Create demo tasks for first user
        print("\nCreating demo tasks...")
        if users:
            create_demo_tasks(db, users[0])
        
        print("\n" + "=" * 50)
        print("Seeding complete!")
        print("=" * 50)
        print("\nDemo accounts:")
        print("  Email: demo@taskflow.dev")
        print("  Password: demo1234")
        print("\n  Email: admin@taskflow.dev")
        print("  Password: admin1234")
        print("=" * 50)
        
    finally:
        db.close()


if __name__ == "__main__":
    main()

