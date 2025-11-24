"""Follower pool toggle API routes"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ToggleResponse
from app.config import settings
from app.database import follower_engine

router = APIRouter(prefix="/api/toggle", tags=["toggle"])


@router.get("/follower", response_model=ToggleResponse)
async def get_follower_status():
    """Get current follower pool status"""
    return ToggleResponse(
        follower_pool_enabled=settings.use_follower_pool,
        message=f"Follower pool is {'enabled' if settings.use_follower_pool else 'disabled'}"
    )


@router.post("/follower", response_model=ToggleResponse)
async def toggle_follower_pool(enabled: bool = None):
    """
    Toggle follower pool usage on/off.
    
    If enabled is None, toggles current state.
    """
    if follower_engine is None:
        raise HTTPException(
            status_code=400,
            detail="Follower database is not configured. Set FOLLOWER_DATABASE_URL environment variable."
        )
    
    if enabled is None:
        # Toggle current state
        settings.use_follower_pool = not settings.use_follower_pool
    else:
        settings.use_follower_pool = enabled
    
    status = "enabled" if settings.use_follower_pool else "disabled"
    
    return ToggleResponse(
        follower_pool_enabled=settings.use_follower_pool,
        message=f"Follower pool has been {status}"
    )

