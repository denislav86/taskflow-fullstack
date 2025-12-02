"""API routers."""

from fastapi import APIRouter

from app.api.routers import auth, tasks, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

